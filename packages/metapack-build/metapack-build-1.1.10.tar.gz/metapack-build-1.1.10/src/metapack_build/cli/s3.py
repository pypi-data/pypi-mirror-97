# Copyright (c) 2017 Civic Knowledge. This file is licensed under the terms of the
# Revised BSD License, included in this distribution as LICENSE

"""
CLI program for storing pacakges in CKAN
"""

import os
from os import getcwd, getenv
from os.path import basename
from pathlib import Path

import yaml
from botocore.exceptions import NoCredentialsError
from tabulate import tabulate

from metapack import MetapackDoc, MetapackPackageUrl, MetapackUrl, open_package
from metapack.cli.core import err, prt
from metapack.constants import PACKAGE_PREFIX
from metapack.index import SearchIndex, search_index_file
from metapack.package import Downloader
from metapack.util import datetime_now
from metapack_build.build import create_s3_csv_package, generate_packages
from metapack_build.cli.build import last_dist_marker_path
from metapack_build.package import S3CsvPackageBuilder
from metapack_build.package.s3 import S3Bucket
from metatab import DEFAULT_METATAB_FILE
from rowgenerators import parse_app_url
from rowgenerators.util import fs_join as join

downloader = Downloader.get_instance()


class MetapackCliMemo(object):

    def __init__(self, args):

        self.cwd = getcwd()

        self.args = args

        self.downloader = Downloader.get_instance()

        self.cache = self.downloader.cache

        self.mtfile_arg = self.args.metatabfile if self.args.metatabfile else join(self.cwd, DEFAULT_METATAB_FILE)

        self.mtfile_url = MetapackUrl(self.mtfile_arg, downloader=self.downloader)

        self.resource = self.mtfile_url.target_file

        self.package_url = self.mtfile_url.package_url
        self.mt_file = self.mtfile_url.metadata_url

        self.package_root = self.package_url.join(PACKAGE_PREFIX)

        if not self.args.s3:
            doc = MetapackDoc(self.mt_file)
            self.args.s3 = doc['Root'].find_first_value('Root.S3')

        self.s3_url = parse_app_url(self.args.s3)

        if self.s3_url and not self.s3_url.scheme == 's3':
            self.s3_url = parse_app_url("s3://{}".format(self.args.s3))

        self.doc = MetapackDoc(self.mt_file)

        access_value = self.doc.find_first_value('Root.Access')

        self.acl = 'private' if access_value == 'private' else 'public-read'

        self.bucket = S3Bucket(self.s3_url, acl=self.acl, profile=self.args.profile) if self.s3_url else None


def s3(subparsers):
    parser = subparsers.add_parser(
        's3',
        help='Create packages and store them in s3 buckets',
    )

    parser.set_defaults(run_command=run_s3)

    parser.add_argument('-p', '--profile', help="Name of a BOTO or AWS credentials profile", required=False)

    parser.add_argument('-s', '--s3', help="URL to S3 where packages will be stored", required=False)

    parser.add_argument('-r', '--result', action='store_true', default=False,
                        help="If mp -q flag set, still report results")

    parser.add_argument('-F', '--force', default=False, action='store_true',
                        help='Force write for all files')

    parser.add_argument('-C', '--credentials', help="Show S3 Credentials and exit. "
                                                    "Eval this string to setup credentials in other shells.",
                        action='store_true', default=False)

    parser.add_argument('metatabfile', nargs='?', help='Path to a Metatab file')


def run_s3(args):
    m = MetapackCliMemo(args)

    if m.args.credentials:
        show_credentials(m.args.profile)
        exit(0)

    # upload packages uploads the FS ( individual files )  and XLSX packages,
    # but does not create the CSV package file
    dist_urls, fs_p = upload_packages(m)

    writes = 0
    csv_url = None
    if dist_urls:

        # Create the CSV package, with links into the filesystem package
        if fs_p:
            access_url, dist_urls, csv_url = create_s3_csv_package(m, dist_urls, fs_p)
        else:
            # If this happens, then no packages were created, because an FS package
            # is always built first
            prt("Not creating CSV package; no FS package was uploaded")

        add_to_index(open_package(access_url))
    else:
        access_url = None

    if dist_urls:

        rows = [[path, url, reason] for what, reason, url, path in fs_p.files_processed if what != 'skip']
        if rows:
            prt("\nWrote these files:")
            writes = len(rows)
            prt(tabulate(rows, headers='path url reason'.split()))

        rows = [[path, url, reason] for what, reason, url, path in fs_p.files_processed if what == 'skip']
        if rows:
            prt("\nSkipped these files:")
            prt(tabulate(rows, headers='path url reason'.split()))

        prt("\nSynchronized these Package Urls")
        prt("-------------------------------")
        for au in dist_urls:
            prt(au)
        prt("-------------------------------")

    else:
        prt("⚠️ Did not find any packages to upload to S3")

    m.doc['Root'].get_or_new_term('Root.Issued').value = datetime_now()

    if fs_p:
        clear_cache(m, fs_p.files_processed)

    csv_pkg = open_package(csv_url)

    # Write the last distribution marker
    dist_info = {
        'name': m.doc.name,
        'version': m.doc.version,
        'access_url': access_url,
        'path': csv_pkg.path,
        'issued': datetime_now(),
        'distributions': {}
    }

    for d in csv_pkg['Distributions'].find('Root.Distribution'):
        dist_info['distributions'][d.type] = str(d.metadata_url)

    Path(last_dist_marker_path(m)).write_text(yaml.safe_dump(dist_info))

    if m.args.result:
        if writes > 0:
            print(f"✅ Wrote {writes} files to {args.s3}")
        else:
            print(f"🚫 Did not write anything to {args.s3}")


def clear_cache(m, files_processed):
    """Remove any files we may have uploaded from the cache. """

    for what, reason, url, path in files_processed:
        cp = m.doc.downloader.cache_path(url)

        if m.cache.exists(cp):
            m.cache.remove(cp)


def add_to_index(p):
    idx = SearchIndex(search_index_file())

    idx.add_package(p, format='web')

    idx.write()


def upload_packages(m):
    """"""
    dist_urls = []
    fs_p = None

    files_processed = []

    # For each package in _packages with the same name as this document...
    for ptype, purl, cache_path in generate_packages(m):

        au = m.bucket.access_url(cache_path)

        # Just copy the Excel and Zip files directly to S3
        if ptype in ('xlsx', 'zip'):
            with open(purl.path, mode='rb') as f:
                access_url = m.bucket.write(f.read(), basename(purl.path), m.acl)

                if m.bucket.last_reason:
                    files_processed.append([*m.bucket.last_reason, access_url, '/'.join(purl.path.split(os.sep)[-2:])])

                prt("Added {} distribution: {} ".format(ptype, au))
                dist_urls.append(au)

        elif ptype == 'fs':
            # Write all of the FS package files to S3

            try:
                s3_package_root = MetapackPackageUrl(str(m.s3_url), downloader=m.downloader)

                # fake-out: it's not actually an S3 CSV package; it's a FS package on S3.
                fs_p = S3CsvPackageBuilder(purl.metadata_url, s3_package_root, callback=prt, env={}, acl='public-read')

                url = fs_p.save()

                prt("Packaged saved to: {}".format(url))

                # fs_url = MetapackUrl(url, downloader=purl.metadata_url.downloader)

            except NoCredentialsError:
                print(getenv('AWS_SECRET_ACCESS_KEY'))
                err("Failed to find boto credentials for S3. "
                    "See http://boto3.readthedocs.io/en/latest/guide/configuration.html ")

            # A crappy hack. make_s3_package should return the correct url
            if fs_p:
                if m.acl == 'private':
                    au = fs_p.private_access_url.inner
                else:
                    au = fs_p.public_access_url.inner

                dist_urls.append(au)

    if fs_p:
        fs_p.files_processed += files_processed  # Ugly encapsulating-breaking hack.

    return dist_urls, fs_p


def show_credentials(profile):
    import boto3

    session = boto3.Session(profile_name=profile)

    if profile:
        cred_line = " 'eval $(metasync -C -p {} )'".format(profile)
    else:
        cred_line = " 'eval $(metasync -C)'"

    prt("export AWS_ACCESS_KEY_ID={} ".format(session.get_credentials().access_key))
    prt("export AWS_SECRET_ACCESS_KEY={}".format(session.get_credentials().secret_key))
    prt("# Run {} to configure credentials in a shell".format(cred_line))
