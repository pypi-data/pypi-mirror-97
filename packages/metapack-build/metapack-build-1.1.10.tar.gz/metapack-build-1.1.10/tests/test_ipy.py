
import logging
import os
import unittest

from metapack import Downloader, MetapackDoc, open_package
from metapack.cli.core import cli_init
from metatab.rowgenerators import TextRowGenerator
from metatab.util import flatten
from rowgenerators import get_generator, parse_app_url
from support import MetapackTest, test_data

logger = logging.getLogger('user')
logger_err = logging.getLogger('cli-errors')
debug_logger = logging.getLogger('debug')

downloader = Downloader()


class TestIPython(MetapackTest):
    def compare_dict(self, a, b):

        fa = set('{}={}'.format(k, v) for k, v in flatten(a))
        fb = set('{}={}'.format(k, v) for k, v in flatten(b))

        # The declare lines move around a lot, and rarely indicate an error
        fa = {e for e in fa if not e.startswith('declare=')}
        fb = {e for e in fb if not e.startswith('declare=')}

        errors = len(fa - fb) + len(fb - fa)

        if errors:
            print("=== ERRORS ===")

        if len(fa - fb):
            print("In b but not a")
            for e in sorted(fa - fb):
                print('    ', e)

        if len(fb - fa):
            print("In a but not b")
            for e in sorted(fb - fa):
                print('    ', e)

        self.assertEqual(0, errors)

    def test_html(self):

        p = open_package(test_data('packages/example.com/example.com-full-2017-us/metadata.csv'))

        self.assertTrue(len(p._repr_html_()) > 4500, len(p._repr_html_()))

        print(list(e.name for e in p.find('Root.Resource')))

        r = p.find_first('Root.Resource', name='random-names')

        self.assertTrue(len(r._repr_html_()) > 400, len(r._repr_html_()))

    def test_dataframe(self):

        try:
            p = open_package(test_data('packages/example.com/example.com-full-2017-us/metadata.csv'))

            r = p.resource('random-names')

            df = r.dataframe()

            self.assertTrue(df.describe().loc['count', 'Size'] == 100)
            self.assertTrue(df.describe().loc['mean', 'Size'].round(4) == 49.8032)

            df = r.read_csv()

            self.assertTrue(df.describe().loc['count', 'Size'] == 100)
            self.assertTrue(df.describe().loc['mean', 'Size'].round(4) == 49.8032)
        except ImportError:
            unittest.skip("Pandas not installed")
            return

    def test_build_dataframe(self):

        p = open_package(test_data('packages/example.com/example.com-python/metadata.csv'))

        df = p.resource('simple').dataframe()

        self.assertEqual(270, df.sum().sum())

        df = p.resource('explicit_dataframe_source').dataframe()

        self.assertEqual(435, df.sum().sum())

        df = p.resource('implicit_dataframe_source').dataframe()

        self.assertEqual(435, df.sum().sum())

    @unittest.skip("Requires Publicdata module")
    def test_line_doc(self):

        from os.path import splitext, basename
        import sys

        with open(test_data('line', 'line-oriented-doc.txt')) as f:
            text = f.read()

        doc = MetapackDoc(TextRowGenerator("Declare: metatab-latest\n" + text))

        # process_schemas(doc)

        r = doc.reference('tracts')

        self.assertEqual(628, len(list(r)))

        tracts = r.dataframe()

        self.assertEqual(-73427, tracts.lon.sum().astype(int))

        tracts = r.read_csv()

        self.assertEqual(-73427, tracts.lon.sum().astype(int))

        r.dataframe()

        # Test loading a Python Library from a package.

        ref = doc.reference('incv')

        self.assertIsNotNone(ref)

        ref_resource = parse_app_url(ref.url).inner.clear_fragment().get_resource()

        # The path has to be a Metatab ZIP archive, and the root directory must be the same as
        # the name of the path

        pkg_name, _ = splitext(basename(ref_resource.path))

        lib_path = ref_resource.join(pkg_name).path

        if lib_path not in sys.path:
            sys.path.insert(0, lib_path)

    def test_notebook_url(self):

        try:
            from metapack.appurl import JupyterNotebookUrl
            from metapack.jupyter.exec import execute_notebook
            from os.path import exists

            u = parse_app_url(test_data('notebooks', 'GenerateDataTest.ipynb'))

            self.assertIsInstance(u, JupyterNotebookUrl)

            execute_notebook(u.path, '/tmp/nbtest', ['dfa', 'dfb'], True)

            self.assertTrue(exists('/tmp/nbtest/dfa.csv'))
            self.assertTrue(exists('/tmp/nbtest/dfb.csv'))

            g = get_generator(parse_app_url('/tmp/nbtest/dfa.csv'))

            print(list(g))
        except ImportError:
            unittest.skip("Missing pandas or jupyter client")
            return

    @unittest.skip("Broken")
    def test_nbconvert(self):

        from collections import namedtuple
        from metapack.jupyter.convert import convert_documentation

        cli_init()

        M = namedtuple('M', 'mt_file')

        fn = test_data('notebooks/ConversionTest.ipynb')

        m = M(mt_file=parse_app_url(fn))

        convert_documentation(m.mt_file.path)

    @unittest.skip('Pandoc & latex wackiness')
    def test_nbconvert_package(self):

        try:
            from collections import namedtuple
            from metapack.jupyter.convert import convert_notebook

            cli_init()

            M = namedtuple('M', 'mt_file mtfile_arg init_stage2')

            fn = test_data('notebooks/ConversionTest.ipynb')

            m = M(mt_file=parse_app_url(fn), mtfile_arg=parse_app_url(fn),
                  init_stage2=lambda x, y: None)

            convert_notebook(m.mt_file.path)
        except (ImportError, FileNotFoundError):
            unittest.skip("Pandoc is not installed")
            return

    @unittest.skip("Broken")
    def x_test_pandas(self):

        package_dir = '/Volumes/Storage/proj/virt-proj/metatab3/metatab-packages/civicknowledge.com/immigration-vs-gdp'

        doc = open_package(package_dir)

        r = doc.first_resource(name='country_gdp')

        rows = list(r)

        print(len(rows))

        df = r.dataframe()

        print(df.head())

    @unittest.skip("Broken")
    def x_test_metatab_line(self):
        from metatab.generate import TextRowGenerator
        from metatab.cli.core import process_schemas
        from metatab import MetatabDoc

        cli_init()

        doc = MetatabDoc(TextRowGenerator(test_data('simple-text.txt'), 'simple-text.txt'))

        process_schemas(doc)

        r = doc.resource('resource')

        for c in r.columns():
            print(c)

    @unittest.skip("Broken")
    def x_test_ipy(self):
        from rowgenerators import SourceSpec, Url, RowGenerator, get_cache

        urls = (
            'ipynb+file:foobar.ipynb',
            'ipynb+http://example.com/foobar.ipynb',
            'ipynb:foobar.ipynb'

        )

        for url in urls:
            u = Url(url)
            print(u, u.path, u.resource_url)

            s = SourceSpec(url)
            print(s, s.proto, s.scheme, s.resource_url, s.target_file, s.target_format)
            self.assertIn(s.scheme, ('file', 'http'))
            self.assertEquals('ipynb', s.proto)

        gen = RowGenerator(cache=get_cache(),
                           url='ipynb:scripts/Py3Notebook.ipynb#lst',
                           working_dir=test_data(),
                           generator_args={'mult': lambda x: x * 3})

        rows = gen.generator.execute()

        print(len(rows))

    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def x_test_categorical(self):

        import metapack as mp

        fn = '/Users/eric/proj/virt-proj/data-project/chis/healthpolicy.ucla.edu-chis_food/'

        pkg = mp.open_package(fn)

        print(pkg.resource)


if __name__ == '__main__':
    unittest.main()
