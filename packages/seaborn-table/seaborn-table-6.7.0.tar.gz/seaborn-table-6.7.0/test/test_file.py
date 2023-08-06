import unittest

from seaborn_table.table import main as cli_converter
from test.support import BaseTest, FormatMixin


class FileConversionMixin(FormatMixin):
    def validate_test_condition(self, source):
        dest = self.DEST
        source_file = self.get_data_path('test_file.%s' % source)
        expected_file = self.get_data_path('test_file.%s' % dest)
        result_file = self.get_data_path('_%s' % source, 'test_file.%s' % dest)
        cli_converter([source_file, result_file])
        self.assert_result_file(expected_file, result_file,
                                "Failure converting %s into %s" % (
                                    source, dest))
        self.remove_file(result_file)

    def test_html(self):
        raise unittest.SkipTest("reading html has not been implemented")


class FileConversionTestTxt(BaseTest, FileConversionMixin):
    DEST = 'txt'


class FileConversionTestCsv(BaseTest, FileConversionMixin):
    DEST = 'csv'


class FileConversionTestMd(BaseTest, FileConversionMixin):
    DEST = 'md'


class FileConversionTestHtml(BaseTest, FileConversionMixin):
    DEST = 'html'


class FileConversionTestGrid(BaseTest, FileConversionMixin):
    DEST = 'grid'


class FileConversionTestJson(BaseTest, FileConversionMixin):
    DEST = 'json'

class FileConversionTestYaml(BaseTest, FileConversionMixin):
    DEST = 'yaml'


class FileConversionTestRst(BaseTest, FileConversionMixin):
    DEST = 'rst'


class FileConversionTestPsql(BaseTest, FileConversionMixin):
    DEST = 'psql'


class ParseArgsTest(BaseTest):
    def validate_test_condition(self, name, source, dest, *columns):
        source_file = self.get_data_path('test_file.%s' % source)
        expected_file = self.get_data_path('expected', '%s.%s' % (name, dest))
        result_file = self.get_data_path('_parse_args', '%s.%s' % (name, dest))
        cli_converter([source_file, result_file] + list(columns))
        self.assert_result_file(expected_file, result_file,
                                "Failure converting %s into %s" % (
                                    source, dest))
        self.remove_file(result_file)

    def test_reorder_columns(self):
        self.validate_test_condition('test_reorder_columns', 'txt', 'grid',
                                     '--columns', 'Target', 'Action', 'Role',
                                     'Player', 'TU')

    def test_remove_columns(self):
        self.validate_test_condition('test_remove_columns', 'json', 'psql',
                                     '--columns', 'TU', 'Player', 'Action')

    def test_add_columns(self):
        self.validate_test_condition('test_add_columns', 'csv', 'md',
                                     '--columns', 'TU', 'Addition1', 'Player',
                                     'Action', 'Role', 'Player', 'TU',
                                     'Addition2')

    def test_reorder_rows(self):
        self.validate_test_condition('test_reorder_rows', 'csv', 'md',
                                     '--order-by', 'TU', 'Role')

    def test_reorder_rows_reverse(self):
        self.validate_test_condition('test_reorder_rows_reverse', 'csv', 'md',
                                     '--order-by', '~Player', 'Target')


if __name__ == '__main__':
    unittest.main()
