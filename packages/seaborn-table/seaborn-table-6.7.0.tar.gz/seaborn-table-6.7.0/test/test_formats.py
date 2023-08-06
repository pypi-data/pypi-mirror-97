import sys
import unittest

from seaborn_table.table import SeabornTable, UNICODE, BASESTRING
from test.support import BaseTest, FormatMixin


class QuoteNumbersTest(BaseTest, FormatMixin):
    def validate_test_condition(self, source):
        table = self.get_base_table()
        table.map(lambda x: UNICODE(x))
        result_file = self.get_data_path('_quote_numbers',
                                          'test_quote.%s' % source)
        table.obj_to_file(result_file, quote_numbers=False)
        expected_file = self.get_data_path('expected',
                                            'test_quote.%s' % source)
        self.assert_result_file(expected_file, result_file)
        self.remove_file(result_file)


class EvalCellsFalseTest(BaseTest, FormatMixin):
    def validate_test_condition(self, source):
        file_path = self.get_data_path('test_file.%s' % source)
        table = SeabornTable.file_to_obj(eval_cells=False, file_path=file_path)
        assert isinstance(table[0]['TU'], BASESTRING)

    def test_html(self):
        unittest.skip("uncomment after implementing html_to_obj")


class InsertPopRemoveColumnTest(BaseTest, FormatMixin):
    def validate_test_condition(self, source):
        table = self.get_base_table()
        table.insert(0, 'remove_column')
        table.insert(None, 'pop_empty_columns')
        table.remove_column('remove_column')
        table.pop_empty_columns()
        result_file = self.get_data_path('_column_results',
                                          'test_file.%s' % source)
        table.obj_to_file(result_file)
        expected_file = self.get_data_path('test_file.%s' % source)
        self.assert_result_file(expected_file, result_file)
        self.remove_file(result_file)


class MultipleSavesTests(BaseTest, FormatMixin):
    def validate_test_condition(self, source):
        table = self.get_base_table()
        answers = table.obj_to_type(source).split('\n')
        results = table.obj_to_type(source).split('\n')
        for answer, result in zip(answers, results):
            self.assertEqual(answer, result)


class HeaderOnlyTest(BaseTest, FormatMixin):
    def validate_test_condition(self, source):
        expected = SeabornTable(columns=[
            'TEST COL 1', 'TEST COL TWO', 'LAST COL'])
        text = expected.obj_to_type(source)
        result = SeabornTable.type_to_obj(source, text=text)
        expected_file = self.get_data_path('expected',
                                            'header_only.%s' % source)
        result_file = self.get_data_path('_header_only',
                                          'header_only.%s' % source)
        expected.obj_to_file(expected_file)
        result.obj_to_file(result_file)
        self.assert_result_file(expected_file, result_file)
        self.remove_file(result_file)
        self.assertEqual(expected, result)

    def test_html(self):
        unittest.skip("uncomment after implementing html_to_obj")


class SharedColumnTest(BaseTest, FormatMixin):
    SHARED_LIMIT = 0
    BASENAME = 'test_share_columns_0.%s'

    def validate_test_condition(self, source):
        tables = [SeabornTable.file_to_obj(
            file_path=self.get_data_path('test_share_columns_%s.rst' % i))
            for i in range(4)]
        for table in tables:
            table.share_column_widths(tables, self.SHARED_LIMIT)
        basename = self.BASENAME % source
        expected_file = self.get_data_path('expected', basename)
        result_file = self.get_data_path('_shared', basename)
        with open(result_file, 'w') as fn:
            for table in tables:
                text = table.obj_to_type(source) + u'\n\n'
                if sys.version_info[0] == 2:
                    text = text.encode('utf-8')
                fn.write(text)
        self.assert_result_file(expected_file, result_file)
        self.remove_file(result_file)

    def test_html(self):
        unittest.skip("Not Applicable")

    def test_json(self):
        unittest.skip("Not Applicable")


class SharedColumnLimitTest(SharedColumnTest):
    SHARED_LIMIT = 10
    BASENAME = 'test_share_columns_10.%s'


class SharedColumnLimitTestNone(SharedColumnTest):
    SHARED_LIMIT = None
    BASENAME = 'test_share_columns_0.%s'


class LineBreakTest(BaseTest, FormatMixin):
    BASENAME = 'test_line_break.%s'

    def validate_test_condition(self, source):
        data = [['cell 1, 1.0\ncell 1, 1.1',
                 'cell 1, 2',
                 'cell 1, 3'],
                ['cell 2, 1',
                 'cell 2, 2.0\ncell 2, 2.1\ncell 2, 2.2',
                 'cell 2, 3'],
                ['cell 3, 1',
                 '\ncell 3, 2',
                 'cell 3, 3.0\ncell 3, 3.1\ncell 3, 3.2\ncell 3, 3.3'],
                ['cell 4, 1.0\n               cell 4, 1.1',
                 'cell 4, 2.0\ncell 4, 2.1',
                 'cell 4, 3.0\ncell 4, 3.1\ncell 4, 3.2'],
                ['\n\ncell 5, 1',
                 'cell 5, 2',
                 'cell 5, 3']]
        table = SeabornTable(data, row_columns=['Header 1',
                                                'Header 2.0\nHeader 2.1',
                                                'Header 3'])
        basename = self.BASENAME % source
        expected_file = self.get_data_path('expected', basename)
        result_file = self.get_data_path('_shared', basename)
        table.obj_to_file(result_file, break_line=True)
        self.assert_result_file(expected_file, result_file)
        self.remove_file(result_file)
        table.close_live_table()


class LiveTableTest(BaseTest, FormatMixin):
    BASENAME = 'test_live_table'

    def validate_test_condition(self, source):
        data = [
            [1, '', 3, 'hidden'],
            [None, '2.1', 3.1, 'h'],
            [1.12, 'very long cell', 3.12, 'h2'],
            [1, 'very long cell to be clipped', 3, '']
        ]
        result_file = self.get_data_path('_live_table',
                                          self.BASENAME+'.'+source)
        expected_file = self.get_data_path('expected',
                                            self.BASENAME+'_%s.'+source)
        table = SeabornTable(
            data[:1],
            row_columns=['A', 'B', 'C', 'Hidden'],
            live_tables=[
                dict(file_path=result_file, min_widths=2,
                     max_widths={'A': 10, 'B': 10, 'C': 10},
                     clip_widths=14, recreate=True),
            ]
        )
        self.assert_result_file(expected_file%0, result_file)
        table.append(data[1])
        self.assert_result_file(expected_file%1, result_file)
        for index, row in enumerate(data[2:], start=2):
            table.append({col: row[i]
                          for i, col in enumerate(table.row_columns)})
            self.assert_result_file(expected_file%index, result_file)

        table.close_live_table()
        self.assert_result_file(expected_file % (index+1), result_file)
        self.remove_file(result_file)

    def test_html(self):
        unittest.skip("Not Applicable")

    def test_json(self):
        unittest.skip("Not Applicable")

    def test_yaml(self):
        unittest.skip("Not Applicable")



if __name__ == '__main__':
    unittest.main()
