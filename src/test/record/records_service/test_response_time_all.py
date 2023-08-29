# Copyright 2021 Research Institute of Systems Planning, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from caret_analyze.record import ColumnValue
from caret_analyze.record import ResponseTime
from caret_analyze.record.record_factory import RecordsFactory


def create_records(records_raw, columns):
    records = RecordsFactory.create_instance()
    for column in columns:
        records.append_column(column, [])

    for record_raw in records_raw:
        records.append(record_raw)
    return records


def to_dict(records):
    return [record.data for record in records]


class TestResponseTimeAll:

    def test_empty_case(self):
        records_raw = [
        ]
        columns = [ColumnValue('start'), ColumnValue('end')]
        records = create_records(records_raw, columns)

        response_time = ResponseTime(records)

        expect_raw = [
        ]
        result = to_dict(response_time.to_all_records())
        assert result == expect_raw

    def test_two_column_default_case(self):
        records_raw = [
            {'start': 0, 'end': 2},
            {'start': 3, 'end': 4},
            {'start': 11, 'end': 12}
        ]
        columns = [ColumnValue('start'), ColumnValue('end')]
        records = create_records(records_raw, columns)

        response_time = ResponseTime(records)

        expect_raw = [
            {'start': 0, 'response_time': 2},
            {'start': 3, 'response_time': 1},
            {'start': 11, 'response_time': 1}
        ]
        result = to_dict(response_time.to_all_records())
        assert result == expect_raw

    def test_three_column_default_case(self):
        records_raw = [
            {'start': 0, 'middle': 1, 'end': 2},
            {'start': 3, 'middle': 4, 'end': 6},
            {'start': 11, 'middle': 13, 'end': 16}
        ]
        columns = [ColumnValue('start'), ColumnValue('middle'), ColumnValue('end')]
        records = create_records(records_raw, columns)

        response_time = ResponseTime(records)

        expect_raw = [
            {'start': 0, 'response_time': 2},
            {'start': 3, 'response_time': 3},
            {'start': 11, 'response_time': 5}
        ]
        result = to_dict(response_time.to_all_records())
        assert result == expect_raw

    def test_single_input_multi_output_case(self):
        records_raw = [
            {'start': 0, 'middle': 4, 'end': 5},
            {'start': 0, 'middle': 4, 'end': 6},
            {'start': 0, 'middle': 12, 'end': 13}
        ]
        columns = [ColumnValue('start'), ColumnValue('middle'), ColumnValue('end')]
        records = create_records(records_raw, columns)

        response_time = ResponseTime(records)

        expect_raw = [
            {'start': 0, 'response_time': 5}
        ]
        result = to_dict(response_time.to_all_records())
        assert result == expect_raw

    def test_multi_input_single_output_case(self):
        records_raw = [
            {'start': 0, 'middle': 4, 'end': 13},
            {'start': 1, 'middle': 4, 'end': 13},
            {'start': 5, 'middle': 12, 'end': 13}
        ]
        columns = [ColumnValue('start'), ColumnValue('middle'), ColumnValue('end')]
        records = create_records(records_raw, columns)

        response_time = ResponseTime(records)

        expect_raw = [
            {'start': 0, 'response_time': 13},
            {'start': 1, 'response_time': 12},
            {'start': 5, 'response_time': 8}
        ]
        result = to_dict(response_time.to_all_records())
        assert result == expect_raw

    def test_drop_case(self):
        records_raw = [
            {'start': 0, 'middle': 4, 'end': 13},
            {'start': 1, 'middle': 4},
            {'start': 5, 'middle': 12, 'end': 13}
        ]
        columns = [ColumnValue('start'), ColumnValue('middle'), ColumnValue('end')]
        records = create_records(records_raw, columns)

        response_time = ResponseTime(records)

        expect_raw = [
            {'start': 0, 'response_time': 13},
            {'start': 1, 'response_time': 12},
            {'start': 5, 'response_time': 8}
        ]
        result = to_dict(response_time.to_all_records())
        assert result == expect_raw
