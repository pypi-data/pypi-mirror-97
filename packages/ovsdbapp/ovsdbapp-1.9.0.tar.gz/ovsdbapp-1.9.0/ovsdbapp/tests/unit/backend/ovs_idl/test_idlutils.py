# Copyright 2016, Mirantis Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from unittest import mock

from ovsdbapp import api
from ovsdbapp.backend.ovs_idl import idlutils
from ovsdbapp.tests import base


class MockColumn(object):
    def __init__(self, name, type, is_optional=False, test_value=None):
        self.name = name
        self.type = mock.MagicMock(
            **{"key.type.name": type,
               "is_optional": mock.Mock(return_value=is_optional),
               })
        # for test purposes only to operate with some values in condition_match
        # testcase
        self.test_value = test_value


class MockTable(object):
    def __init__(self, name, *columns):
        # columns is a list of tuples (col_name, col_type)
        self.name = name
        self.columns = {c.name: c for c in columns}


class MockRow(object):
    def __init__(self, table):
        self._table = table

    def __getattr__(self, attr):
        if attr in self._table.columns:
            return self._table.columns[attr].test_value
        return super(MockRow, self).__getattr__(attr)


class MockCommand(api.Command):
    def __init__(self, result):
        self.result = result

    def execute(self, **kwargs):
        pass


class TestIdlUtils(base.TestCase):
    def test_condition_match(self):
        """Make sure that the function respects the following:

        * if column type is_optional and value is a single element, value is
          transformed to a length-1-list
        * any other value is returned as it is, no type conversions
        """

        table = MockTable("SomeTable",
                          MockColumn("tag", "integer", is_optional=True,
                                     test_value=[42]),
                          MockColumn("num", "integer", is_optional=True,
                                     test_value=[]),
                          MockColumn("ids", "integer", is_optional=False,
                                     test_value=42),
                          MockColumn("comments", "string",
                                     test_value=["a", "b", "c"]),
                          MockColumn("status", "string",
                                     test_value="sorry for inconvenience"))
        row = MockRow(table=table)
        self.assertTrue(idlutils.condition_match(row, ("tag", "=", 42)))
        # optional types can be compared only as single elements
        self.assertRaises(ValueError,
                          idlutils.condition_match, row, ("tag", "!=", [42]))
        # empty list comparison is ok for optional types though
        self.assertTrue(idlutils.condition_match(row, ("tag", "!=", [])))
        self.assertTrue(idlutils.condition_match(row, ("num", "=", [])))
        # value = [] may be compared to a single elem if optional column type
        self.assertTrue(idlutils.condition_match(row, ("num", "!=", 42)))
        # no type conversion for non optional types
        self.assertTrue(idlutils.condition_match(row, ("ids", "=", 42)))
        self.assertTrue(idlutils.condition_match(
            row, ("status", "=", "sorry for inconvenience")))
        self.assertFalse(idlutils.condition_match(
            row, ("status", "=", "sorry")))
        # bad types
        self.assertRaises(ValueError,
                          idlutils.condition_match, row, ("ids", "=", "42"))
        self.assertRaises(ValueError,
                          idlutils.condition_match, row, ("ids", "!=", "42"))
        self.assertRaises(ValueError,
                          idlutils.condition_match, row,
                          ("ids", "!=", {"a": "b"}))
        # non optional list types are kept as they are
        self.assertTrue(idlutils.condition_match(
            row, ("comments", "=", ["c", "b", "a"])))
        # also true because list comparison is relaxed
        self.assertTrue(idlutils.condition_match(
            row, ("comments", "=", ["c", "b"])))
        self.assertTrue(idlutils.condition_match(
            row, ("comments", "!=", ["d"])))

    def test_db_replace_record_dict(self):
        obj = {'a': 1, 'b': 2}
        self.assertIs(obj, idlutils.db_replace_record(obj))

    def test_db_replace_record_dict_cmd(self):
        obj = {'a': 1, 'b': MockCommand(2)}
        res = {'a': 1, 'b': 2}
        self.assertEqual(res, idlutils.db_replace_record(obj))

    def test_db_replace_record_list(self):
        obj = [1, 2, 3]
        self.assertIs(obj, idlutils.db_replace_record(obj))

    def test_db_replace_record_list_cmd(self):
        obj = [1, MockCommand(2), 3]
        res = [1, 2, 3]
        self.assertEqual(res, idlutils.db_replace_record(obj))

    def test_db_replace_record_tuple(self):
        obj = (1, 2, 3)
        self.assertIs(obj, idlutils.db_replace_record(obj))

    def test_db_replace_record_tuple_cmd(self):
        obj = (1, MockCommand(2), 3)
        res = (1, 2, 3)
        self.assertEqual(res, idlutils.db_replace_record(obj))

    def test_db_replace_record(self):
        obj = "test"
        self.assertIs(obj, idlutils.db_replace_record(obj))

    def test_db_replace_record_cmd(self):
        obj = MockCommand("test")
        self.assertEqual("test", idlutils.db_replace_record(obj))

    @mock.patch('sys.platform', 'linux2')
    def test_row_by_record_linux(self):
        FAKE_RECORD = 'fake_record'
        mock_idl_ = mock.MagicMock()
        mock_table = mock.MagicMock(
            rows={mock.sentinel.row: mock.sentinel.row_value})
        mock_idl_.tables = {mock.sentinel.table_name: mock_table}

        res = idlutils.row_by_record(mock_idl_,
                                     mock.sentinel.table_name,
                                     FAKE_RECORD)
        self.assertEqual(mock.sentinel.row_value, res)

    @mock.patch('sys.platform', 'win32')
    def test_row_by_record_win(self):
        FAKE_RECORD_GUID = '7b0f349d-5524-4d36-afff-5222b9fdee8c'
        mock_idl_ = mock.MagicMock()
        mock_table = mock.MagicMock(
            rows={mock.sentinel.row: mock.sentinel.row_value})
        mock_idl_.tables = {mock.sentinel.table_name: mock_table}

        res = idlutils.row_by_record(mock_idl_,
                                     mock.sentinel.table_name,
                                     FAKE_RECORD_GUID)
        self.assertEqual(mock.sentinel.row_value, res)

    def test_index_name(self):
        expected = {
            ('one',): 'one',
            ('abc', 'def'): 'abc_def',
            ('def', 'abc'): 'abc_def',
            ('one', 'two', 'three'): 'one_three_two',
        }
        for args, result in expected.items():
            self.assertEqual(result, idlutils.index_name(*args))

        self.assertRaises(AssertionError, idlutils.index_name)


class TestMergeIntersection(base.TestCase):
    def test_no_args(self):
        result = idlutils.merge_intersection()
        # This should really be StopIteration, but there is some bug with
        # testtools where it freaks out at getting the expected StopIteration
        self.assertRaises((StopIteration, RuntimeError), next, result)

    def test_single_empty_iterator(self):
        result = idlutils.merge_intersection(iter([]))
        self.assertRaises(StopIteration, next, result)

    def test_multiple_empty_iterator(self):
        result = idlutils.merge_intersection(iter([]), iter([]))
        self.assertRaises(StopIteration, next, result)

    def test_single_value_iterator(self):
        values = [1]
        result = idlutils.merge_intersection(iter(values))
        self.assertEqual(values[0], next(result))
        self.assertRaises(StopIteration, next, result)

    def test_single_matching_value(self):
        values = [[1], [1]]
        result = idlutils.merge_intersection(*(iter(v) for v in values))
        self.assertEqual(values[0][0], next(result))
        self.assertRaises(StopIteration, next, result)

    def test_two_matching_values(self):
        values = [[1, 2], [1, 2]]
        result = idlutils.merge_intersection(*(iter(v) for v in values))
        self.assertEqual(values[0][0], next(result))
        self.assertEqual(values[0][1], next(result))
        self.assertRaises(StopIteration, next, result)

    def test_no_overlapping_values(self):
        values = [[0, 1], [2, 3], [4, 5]]
        result = idlutils.merge_intersection(*(iter(v) for v in values))
        self.assertRaises(StopIteration, next, result)

    def test_proper_subset(self):
        values = [[0, 1, 2, 3, 4], [2, 3]]
        result = idlutils.merge_intersection(*(iter(v) for v in values))
        self.assertEqual(2, next(result))
        self.assertEqual(3, next(result))
        self.assertRaises(StopIteration, next, result)

    def test_intersecting_three(self):
        values = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
        result = idlutils.merge_intersection(*(iter(v) for v in values))
        self.assertEqual(3, next(result))
        self.assertRaises(StopIteration, next, result)
