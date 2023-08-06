import os
import platform
import unittest
import warnings
from csv import DictReader

from metatab.rowgenerators import TextRowGenerator
from rowgenerators import get_generator, parse_app_url
from rowgenerators.exceptions import DownloadError, RowGeneratorError
from tabulate import tabulate

from metapack import (Downloader, MetapackDoc, MetapackPackageUrl, MetapackUrl,
                      ResourceError)
from metapack.cli.core import cli_init
from metapack.constants import PACKAGE_PREFIX
from metapack_build.build import (make_csv_package, make_excel_package,
                                  make_filesystem_package, make_zip_package)
from support import open_package, test_data

warnings.filterwarnings("ignore", category=DeprecationWarning)

downloader = Downloader()


def ds_hash(r):
    import hashlib

    m = hashlib.md5()

    for row in r:
        for col in row:
            m.update(str(col).encode('utf8'))

    return m.hexdigest()


class TestPackages(unittest.TestCase):

    @unittest.skip("Urls are broken")
    def test_resolve_resource_urls(self):
        """Test how resources are resolved in packages.
            - A name, for excel and CSV packages
            - a path, for ZIP and filesystem packages
            - a web url, for any kind of package
        """
        with open(test_data('packages.csv')) as f:
            for i, l in enumerate(DictReader(f), 2):

                # print(i, l['url'], l['target_file'])

                u = MetapackPackageUrl(l['url'], downloader=Downloader())

                try:
                    t = u.resolve_url(l['target_file'])
                    self.assertFalse(bool(l['resolve_error']))
                except ResourceError:
                    self.assertTrue(bool(l['resolve_error']))
                    continue
                except DownloadError:
                    raise

                # Testing containment because t can have path in local filesystem, which changes depending on where
                # test is run

                # print("   ", t)
                self.assertTrue(l['resolved_url'] in str(t), (i, l['resolved_url'], str(t)))

                try:
                    g = get_generator(t.get_resource().get_target())

                    self.assertEqual(101, len(list(g)))
                    self.assertFalse(bool(l['generate_error']))
                except DownloadError:
                    raise
                except RowGeneratorError:
                    self.assertTrue(bool(l['generate_error']))
                    continue

    def test_build_package(self):

        try:
            cli_init()

            m = MetapackUrl(test_data('packages/example.com/example.com-full-2017-us/metadata.csv'),
                            downloader=downloader)

            package_dir = m.package_url.join_dir(PACKAGE_PREFIX)

            cache = Downloader().cache

            _, fs_url, created = make_filesystem_package(m, package_dir, cache, {}, False)
        except ImportError as e:
            unittest.skip(str(e))
            return

        print(created)

    @unittest.skip("needs local file")
    def test_build_s3_package(self):
        from metapack_build.build import make_s3_csv_package

        cache = Downloader().cache

        fs_url = MetapackUrl('/Volumes/Storage/proj/virt-proj/metapack/metapack/test-data/packages/example.com/'
                             'example-package/_packages/example.com-example_data_package-2017-us-1/metadata.csv',
                             downloader=downloader)

        # _, url, created =  make_excel_package(fs_url,package_dir,get_cache(), {}, False)

        # _, url, created = make_zip_package(fs_url, package_dir, get_cache(), {}, False)

        # _, url, created = make_csv_package(fs_url, package_dir, get_cache(), {}, False)

        package_dir = parse_app_url('s3://test.library.civicknowledge.com/metatab', downloader=downloader)

        _, url, created = make_s3_csv_package(fs_url, package_dir, cache, {}, False)

        print(url)
        print(created)

    def test_build_simple_package(self):

        cli_init()

        cache = Downloader().cache

        m = MetapackUrl(test_data('packages/example.com/example.com-simple_example-2017-us'), downloader=downloader)

        package_dir = m.package_url.join_dir(PACKAGE_PREFIX)
        package_dir = package_dir

        _, fs_url, created = make_filesystem_package(m, package_dir, cache, {}, False)

        fs_doc = MetapackDoc(fs_url, cache=downloader.cache)

        fs_doc.resource('random-names')

        # Excel

        _, url, created = make_excel_package(fs_url, package_dir, cache, {}, False)

        self.assertEqual(['random-names', 'renter_cost', 'unicode-latin1'], [r.name for r in url.doc.resources()])

        self.assertEqual(['random-names', 'renter_cost', 'unicode-latin1'], [r.url for r in url.doc.resources()])

        # ZIP

        _, url, created = make_zip_package(fs_url, package_dir, cache, {}, False)

        self.assertEqual(['random-names', 'renter_cost', 'unicode-latin1'], [r.name for r in url.doc.resources()])

        self.assertEqual(['data/random-names.csv', 'data/renter_cost.csv', 'data/unicode-latin1.csv'],
                         [r.url for r in url.doc.resources()])

        #  CSV

        _, url, created = make_csv_package(fs_url, package_dir, cache, {}, False)

        self.assertEqual(['random-names', 'renter_cost', 'unicode-latin1'], [r.name for r in url.doc.resources()])

        self.assertEqual(
            ['com-simple_example-2017-us-2/data/random-names.csv',
             '.com-simple_example-2017-us-2/data/renter_cost.csv',
             'm-simple_example-2017-us-2/data/unicode-latin1.csv'],
            [str(r.url)[-50:] for r in url.doc.resources()])

    def test_sync_csv_package(self):

        from metapack_build.package import CsvPackageBuilder

        package_root = MetapackPackageUrl(
            test_data('packages/example.com/example.com-simple_example-2017-us/_packages'), downloader=downloader)

        source_url = 'http://library.metatab.org/example.com-simple_example-2017-us-2/metadata.csv'

        u = MetapackUrl(source_url, downloader=downloader)

        u.get_resource().get_target()

        p = CsvPackageBuilder(u, package_root, resource_root=u.dirname().as_type(MetapackPackageUrl))

        csv_url = p.save()

        doc = csv_url.metadata_url.doc

        for r in doc.resources():
            print(r.name, r.url)

            # with open(csv_url.path, mode='rb') as f:
            #    print (f.read())
            #    #urls.append(('csv', s3.write(f.read(), csv_url.target_file, acl)))

    @unittest.skip('References non existen url')
    def test_build_geo_package(self):

        from rowgenerators.valuetype import ShapeValue

        m = MetapackUrl(test_data('packages/sangis.org/sangis.org-census_regions/metadata.csv'), downloader=downloader)

        package_dir = m.package_url.join_dir(PACKAGE_PREFIX)

        _, fs_url, created = make_filesystem_package(m, package_dir, downloader.cache, {}, True)

        print(fs_url)

        doc = MetapackDoc(fs_url)

        r = doc.resource('sra')

        rows = list(r.iterdict)

        self.assertEqual(41, len(rows))

        self.assertIsInstance(rows[1]['geometry'], ShapeValue)

    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_build_transform_package(self):

        m = MetapackUrl(test_data('packages/example.com/example.com-transforms/metadata.csv'), downloader=downloader)

        package_dir = m.package_url.join_dir(PACKAGE_PREFIX)

        _, fs_url, created = make_filesystem_package(m, package_dir, downloader.cache, {}, False)

        print(fs_url)

    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_read_geo_packages(self):

        import warnings
        from requests.exceptions import HTTPError

        warnings.simplefilter("ignore")

        try:
            from publicdata.census.dataframe import CensusDataFrame
        except ImportError:
            return unittest.skip("Public data isn't installed")

        with open(test_data('line', 'line-oriented-doc.txt')) as f:
            text = f.read()

        doc = MetapackDoc(TextRowGenerator("Declare: metatab-latest\n" + text))

        r = doc.reference('B09020')

        try:
            df = r.dataframe()
        except HTTPError:  # The Census reporter URLs fail sometimes.
            return unittest.skip("Census Reporter vanished")

        self.assertIsInstance(df, CensusDataFrame)

        r = doc.reference('sra_geo')

        gf = r.geoframe()

        self.assertEqual(41, len(gf.geometry.geom_type))

        self.assertEqual({'Polygon'}, set(gf.geometry.geom_type))

        r = doc.reference('ri_tracts')

        gf = r.geoframe()

        self.assertEqual(244, len(gf.geometry.geom_type))

        print(sorted(list(set(gf.geometry.geom_type))))

        self.assertEqual(['MultiPolygon', 'Polygon'], sorted(list(set(gf.geometry.geom_type))))

        print(gf.head())

    @unittest.skipIf(platform.system() == 'Windows', 'Program generators do not work on windows')
    def test_program_resource(self):

        return  # Actually, completely broken right now

        m = MetapackUrl(test_data('packages/example.com/example.com-full-2017-us/metadata.csv'), downloader=downloader)

        doc = MetapackDoc(m)

        r = doc.resource('rowgen')

        self.assertEqual('program+file:scripts/rowgen.py', str(r.url))

        print(r.resolved_url)

        g = r.row_generator

        print(type(g))

        for row in r:
            print(row)

    def test_fixed_resource(self):
        from itertools import islice
        from rowgenerators.generator.fixed import FixedSource

        m = MetapackUrl(test_data('packages/example.com/example.com-full-2017-us/metadata.csv'), downloader=downloader)

        doc = MetapackDoc(m)

        r = doc.resource('simple-fixed')

        self.assertEqual('fixed+http://public.source.civicknowledge.com/example.com/sources/simple-example.txt',
                         str(r.url))
        self.assertEqual('fixed+http://public.source.civicknowledge.com/example.com/sources/simple-example.txt',
                         str(r.resolved_url))

        g = r.row_generator

        print(r.row_processor_table())

        self.assertIsInstance(g, FixedSource)

        rows = list(islice(r, 10))

        print('----')
        for row in rows:
            print(row)

        self.assertEqual('f02d53a3-6bbc-4095-a889-c4dde0ccf5', rows[5][1])

    def test_petl(self):
        from petl import look

        m = MetapackUrl(test_data('packages/example.com/example.com-full-2017-us/metadata.csv'), downloader=downloader)

        doc = MetapackDoc(m)

        r = doc.resource('simple-example')

        r.resolved_url.get_resource().get_target()

        p = r.petl()

        print(look(p))

    @unittest.skip('Package no longer exists')
    def test_metapack_resources(self):

        cli_init()

        p = test_data('packages/example.com/example.com-metab_reuse/metadata.csv')

        m = MetapackUrl(p, downloader=downloader)

        print(m.doc.resources())

        print(m.get_resource().get_target().exists())

    def test_colmaps(self):

        from rowgenerators.source import ReorderRowGenerator

        # Direct check of ReorderRowGenerator

        class Source(object):
            headers = 'Z X Y'.split()

            def __iter__(self):
                yield self.headers
                for i in range(5):
                    yield ('c' + str(i), 'ae' + str(i), 'b' + str(i))

        cm = dict(a='X', b='Y', c='Z', d=None, e='X')

        rrg = ReorderRowGenerator(Source(), cm)

        self.assertEqual('fd601216d848a8b874e782724ed9cc0c', ds_hash(rrg), tabulate(rrg))

        # Test in a package

        pkg = open_package('example.com/example.com-colmaps')

        r = pkg.reference('gap_map')

        rrg = ReorderRowGenerator(r, r.header_map)

        self.assertEqual('b31c0b696d1d8553562dc382b35e0a2b', ds_hash(rrg), tabulate(rrg))

        # Test in a package

        pkg = open_package('example.com/example.com-colmaps')

        r = pkg.reference('foobar')

        rrg = ReorderRowGenerator(r, r.header_map)

        print(tabulate(rrg))

        # self.assertEqual('b31c0b696d1d8553562dc382b35e0a2b', ds_hash(rrg), tabulate(rrg))


if __name__ == '__main__':
    unittest.main()
