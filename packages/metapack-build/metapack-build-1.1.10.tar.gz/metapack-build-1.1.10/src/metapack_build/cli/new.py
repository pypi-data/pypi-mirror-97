# Copyright (c) 2017 Civic Knowledge. This file is licensed under the terms of the
# Revised BSD License, included in this distribution as LICENSE

"""
Metapack CLI program for creating new metapack package directories
"""

import argparse
from pathlib import Path
from shutil import copyfile

import requests

from metapack.cli.core import MetapackCliMemo as _MetapackCliMemo
from metapack.package import Downloader
from metapack_build.support import pylib

from .update import add_missing_files

downloader = Downloader.get_instance()

TEMPLATE_NOTEBOOK = "https://raw.githubusercontent.com/Metatab/exploratory-data-analysis/master/metadata.ipynb"


class MetapackCliMemo(_MetapackCliMemo):

    def __init__(self, args, downloader):
        super().__init__(args, downloader)


def new_args(subparsers):
    """
    The `mp new` command creates source package directories
    with a proper name, a `.gitignore` file, and optionally, example data,
    entries and code. Typical usage, for creating a new package with most
    of the example options, is ::

        mp new -o metatab.org -d tutorial -T "Quickstart Example Package"

    The ``-C`` option will set a configuration file, which is a
    Metatab file that with terms that are copied into the `metadata.csv` file
    of the new package. Currently, it copies a limited number of terms,
    including:

    - Terms in the Contacts section
    - Root.Space
    - Root.Time
    - Root.Grain
    - Root.Variant
    - Root.Version

    """
    parser = subparsers.add_parser(
        'new',
        help='Create new Metatab packages',
        description=new_args.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.set_defaults(run_command=new_cmd)

    parser.add_argument('-o', '--origin', help="Dataset origin, usually a second-level domain name. Required")
    parser.add_argument('-d', '--dataset', help="Main dataset name. Required", required=True)
    parser.add_argument('-t', '--time', help="Temporal extents, usually a year, ISO8601 time, or interval. ")
    parser.add_argument('-s', '--space', help="Space, geographic extent, such as a name of a state or a Census geoid")
    parser.add_argument('-g', '--grain', help="Grain, the type of entity a row represents")
    parser.add_argument('-v', '--variant', help="Variant, any distinguishing string")
    parser.add_argument('-r', '--revision', help="Version, defaults to 1", default=1)

    parser.add_argument('-T', '--title', help="Set the title")

    parser.add_argument('-L', '--pylib', help="Configure a pylib directory for Python code extensions",
                        action='store_true')

    parser.add_argument('-E', '--example', help="Add examples of resources",
                        action='store_true')

    group = parser.add_argument_group('Alternate Format', 'Generate other types of packages')

    try:
        import metapack_jupyter  # noqa
        group.add_argument('-J', '--jupyter', help="Create a Jupyter notebook source package",
                           action='store_true')
    except ImportError:
        pass

    group.add_argument('-c', '--csv', help="Create a single-file csv source package", action='store_true')

    parser.add_argument('--template', help="Metatab file template, defaults to 'metatab' ", default='metatab')
    parser.add_argument('-C', '--config', help="Path to config file. "
                                               "Defaults to ~/.metapack-defaults.csv or value of METAPACK_DEFAULTS env var."
                                               "Sets defaults for specia root terms and the Contacts section.")
    return parser


def doc_parser():
    from metapack.cli.mp import base_parser

    return new_args(base_parser())


class EmptyTerm(object):
    value = None


et = EmptyTerm()  # For default values for terms that don't exist


def new_cmd(args):
    from metapack import MetapackDoc
    from metapack.util import make_metatab_file, datetime_now, ensure_dir
    from metapack.cli.core import write_doc, prt, err
    from os.path import exists, join, expanduser
    from metatab import DEFAULT_METATAB_FILE
    from os import getenv

    if args.config:
        config_file = args.config
    elif getenv("METAPACK_CONFIG"):
        config_file = getenv("METAPACK_DEFAULTS")
    elif expanduser('~/.metapack-default.csv'):
        config_file = expanduser('~/.metapack-defaults.csv')
    else:
        config_file = None

    if config_file and exists(config_file):
        prt(f"Using defaults file '{config_file}'")
        config = MetapackDoc(config_file)
    else:
        config = MetapackDoc()

    if args.jupyter:
        import tempfile

        with tempfile.NamedTemporaryFile(suffix='.ipynb', delete=False) as fp:

            r = requests.get(TEMPLATE_NOTEBOOK, allow_redirects=True)
            r.raise_for_status()

            fp.write(r.content)
            nb_path = Path(fp.name)

        doc = MetapackDoc(str(nb_path))

    else:

        doc = make_metatab_file(args.template)

    doc['Root']['Created'] = datetime_now()

    origin = args.origin or config.get_value('Root.Origin')

    if not origin:
        err("Must specify a value for origin, either on command line or in defaults file")

    (doc['Root'].find_first('Root.Origin') or et).value = origin
    (doc['Root'].find_first('Root.Dataset') or et).value = args.dataset
    (doc['Root'].find_first('Root.Space') or et).value = args.space or config.get_value('Root.Space')
    (doc['Root'].find_first('Root.Time') or et).value = args.time or config.get_value('Root.Time')
    (doc['Root'].find_first('Root.Grain') or et).value = args.grain or config.get_value('Root.Grain')
    (doc['Root'].find_first('Root.Variant') or et).value = args.variant or config.get_value('Root.Variant')

    v = doc['Root'].get_or_new_term('Root.Version')
    v.get_or_new_child('Version.Major').value = args.revision or config.get_value('Root.Version')
    v.get_or_new_child('Version.Minor').value = 1
    v.get_or_new_child('Version.Patch').value = 1

    # Copy contacts in
    if 'Contacts' in config:
        for c in config['Contacts']:
            doc['Contacts'].add_term(c)

    if args.title:
        doc['Root'].find_first('Root.Title').value = args.title.strip()

    nv_name = doc.as_version(None)

    if args.example:
        doc['Resources'].new_term('Root.Datafile',
                                  'http://public.source.civicknowledge.com/example.com/sources/random-names.csv',
                                  name='random_names')

        doc['Documentation'].new_term('Root.Homepage', 'http://metatab.org', title='Metatab Home Page')

    doc.ensure_identifier()
    doc.update_name(create_term=True)

    if getattr(args, 'jupyter'):  # b/c maybe metatab_jupyter is not installed

        from metapack_jupyter.convert import write_metatab_notebook
        from metapack_jupyter.core import edit_notebook, set_cell_source, get_cell_source

        new_nb_path = Path(f'{nv_name}.ipynb')

        doc['Resources'].new_term('Root.Datafile', './' + str(new_nb_path) + "#df",
                                  name='local_dataframe', description='Example of using a local Dataframe')

        if new_nb_path.exists():
            err(f"Directory {nb_path} already exists")

        copyfile(nb_path, new_nb_path)

        write_metatab_notebook(doc, new_nb_path)

        with edit_notebook(new_nb_path) as nb:
            init = get_cell_source(nb, 'init')
            init += f"\nthis_package_name = '{str(new_nb_path.name)}'"
            set_cell_source(nb, 'init', init)

        nb_path.unlink()
    else:

        doc['Documentation'].new_term('Root.Documentation', 'file:README.md', title='README')

        if exists(nv_name):
            err(f"Directory {nv_name} already exists")

        if args.csv:
            fn = doc.nonver_name + '.csv'
            write_doc(doc, fn)
            prt(f"Writing to {fn}")

        else:
            ensure_dir(nv_name)

            pylib_dir = join(nv_name, 'pylib')
            ensure_dir(pylib_dir)
            with open(join(pylib_dir, '__init__.py'), 'w') as f_out, open(pylib.__file__) as f_in:
                f_out.write(f_in.read())

            if args.example:
                doc['Resources'].new_term('Root.Datafile', 'python:pylib#row_generator', name='row_generator')

            prt(f"Writing to '{nv_name}'")

            write_doc(doc, join(nv_name, DEFAULT_METATAB_FILE))

            add_missing_files(nv_name)

            if args.title:
                readme = '# {}\n'.format(args.title)
            else:
                readme = '# {}\n'.format(doc.get_value('Root.Name'))

            with open(join(nv_name, 'README.md'), 'w') as f:
                f.write(readme)
