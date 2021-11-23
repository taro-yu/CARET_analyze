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

from __future__ import annotations

from abc import abstractmethod
from copy import deepcopy
from enum import IntEnum
import sys
from typing import Callable, Dict, List, Optional, Set

import pandas as pd


class RecordInterface:
    """
    Interface for Record class.

    This behavior is similar to the dictionary type.
    To avoid conflicts with the pybind metaclass, ABC is not used.
    """

    @abstractmethod
    def equals(self, other: RecordInterface) -> bool:
        """
        Compare record.

        Parameters
        ----------
        other : RecordInterface
            comparison target.

        Returns
        -------
        bool
            True if record data is same, otherwise false.

        """
        pass

    @abstractmethod
    def merge(self, other: RecordInterface, inplace=False) -> Optional[Record]:
        """
        Mege record.

        Parameters
        ----------
        other : RecordInterface
            merge target.
        inplace : bool
            inplace record if true, otherwise false.

        Returns
        -------
        Record
            Merged record class if inplace = false, otherwise None.

        """
        pass

    @abstractmethod
    def drop_columns(self, columns: List[str], inplace: bool = False) -> Optional[Record]:
        """
        Drop columns method.

        Parameters
        ----------
        columns : List[str]
            columns to be dropped.
        inplace : bool
            inplace record if true, otherwise false.

        Returns
        -------
        Optional[Record]
            Column dropped record class if inplace = false, otherwise None.

        """
        pass

    @abstractmethod
    def add(self, key: str, stamp: int) -> None:
        """
        Add(Update) column value.

        Parameters
        ----------
        key : str
            key name to set.
        stamp : int
            key value to set.

        """
        pass

    @abstractmethod
    def change_dict_key(self, old_key: str, new_key: str) -> None:
        """
        Change columns name.

        Parameters
        ----------
        old_key : str
            column name to be changed.
        new_key : str
            new column name.

        """
        pass

    @abstractmethod
    def get(self, key: str) -> int:
        """
        Get value for specific column.

        Parameters
        ----------
        key : str
            key name to get.

        Returns
        -------
        int
            Value for selected key.

        """
        pass

    @property
    @abstractmethod
    def data(self) -> Dict[str, int]:
        """
        Convert to dictionary.

        Returns
        -------
        data : Dict[str, int]:
            dictionary data.

        """
        pass

    @property
    @abstractmethod
    def columns(self) -> Set[str]:
        """
        Get columnnames.

        Returns
        -------
        Set[str]
            Column names.

        """
        pass


class RecordsInterface:
    """
    Interface for Record class.

    This behavior is similar to pandas.DataFrame.
    To avoid conflicts with the pybind metaclass, ABC is not used.
    """

    @abstractmethod
    def equals(self, other: RecordsInterface) -> bool:
        """
        Equals method.

        Parameters
        ----------
        other : RecordsInterface
            comparison target.

        Returns
        -------
        bool
            true if record data is same, otherwise false.

        """
        pass

    @abstractmethod
    def append(self, other: RecordInterface) -> None:
        """
        Append new record.

        Parameters
        ----------
        other : RecordInterface
            record to be added.

        """
        pass

    @abstractmethod
    def concat(self, other: RecordsInterface, inplace=False) -> Optional[RecordsInterface]:
        """
        Concat records.

        Parameters
        ----------
        other : RecordsInterface
            records to be concatenated.
        inplace : bool
            inplace original instance if true.

        Returns
        -------
        RecordsInterface
            concatenated records if inplace=False, otherwise None.

        """
        pass

    @abstractmethod
    def sort(
        self, key: str, sub_key: Optional[str] = None, inplace=False, ascending=True
    ) -> Optional[RecordsInterface]:
        """
        Sort records.

        Parameters
        ----------
        key : str
            key name to used for sort.
        sub_key : str
            second key name to used for sort.
        inplace : bool
            inplace original instance if true.
        ascending : bool
            ascending if True, descending if false.

        Returns
        -------
        RecordsInterface
            sorted records if inplace=False, otherwise None.

        """
        pass

    @abstractmethod
    def filter_if(
        self, f: Callable[[RecordInterface], bool], inplace: bool = False
    ) -> Optional[RecordsInterface]:
        """
        Get filterd records.

        Parameters
        ----------
        f : Callable[[RecordInterface], bool]
            condition function.
        inplace : bool
            inplace original instance if true.

        Returns
        -------
        Optional[RecordsInterface]
            Filterd records.

        """
        pass

    @abstractmethod
    def copy(self) -> RecordsInterface:
        """
        Get duplicated records.

        Returns
        -------
        RecordsInterface
            Deep-copyed records.

        TODO
        ----
        * this method is duplicated. remove this.

        """
        pass

    @property
    @abstractmethod
    def data(self) -> List[RecordInterface]:
        """
        Get records list.

        Returns
        -------
        List[RecordInterface]
            Records list.

        """
        pass

    @abstractmethod
    def drop_columns(
        self, columns: List[str], inplace: bool = False
    ) -> Optional[RecordsInterface]:
        """
        Drop columns.

        Parameters
        ----------
        columns : List[str]
            columns to be dropped.
        inplace : bool
            inplace record if true, otherwise false.

        Returns
        -------
        Optional[RecordsInterface]
            Column dropped record class if inplace = false, otherwise None.

        """
        pass

    @abstractmethod
    def rename_columns(
        self, columns: Dict[str, str], inplace: bool = False
    ) -> Optional[RecordsInterface]:
        """
        Rename columns.

        Parameters
        ----------
        columns : Dict[str, str]
            rename params. same as dataframe rename.
        inplace : bool
            inplace record if true, otherwise false.

        Returns
        -------
        Optional[RecordsInterface]
            Column renamed record class if inplace = false, otherwise None.

        """
        pass

    @property
    @abstractmethod
    def columns(self) -> Set[str]:
        """
        Get columnnames.

        Returns
        -------
        Set[str]
            Column names.

        """
        pass

    @abstractmethod
    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert to pandas dataframe.

        Returns
        -------
        pandas.DataFrame
            Records data.

        """
        pass

    @abstractmethod
    def to_string(self) -> str:
        """
        Convert to string.

        TODO
        ----
        * remove this method
        """
        pass

    @abstractmethod
    def merge(
        self,
        right_records: RecordInterface,
        join_key: str,
        how: str = 'inner',
        left_record_sort_key: Optional[str] = None,
        right_record_sort_key: Optional[str] = None,
        *,
        progress_label: Optional[str] = None
    ) -> Records:
        """
        Merge records by key match.

        Parameters
        ----------
        right_records : RecordInterface
            merge target.
        join_key : str
            Key to use for matching.
        how : str
            merge type. [inner/right/left/outer]
        left_record_sort_key : str
            unused [TODO: remove]
        right_record_sort_key : str
            unused [TODO: remove]
        progress_label : str
            label for progress bar. cpp impl only.

        Returns
        -------
        RecordsInterface

        Example
        -------
        >>> left_records = Records([
            Record({'join_key': 1, 'left_other': 1}),
            Record({'join_key': 2, 'left_other': 2}),
        ])
        >>> right_records = Records([
            Record({'join_key': 2, 'right_other': 3}),
            Record({'join_key': 1, 'right_other': 4}),
        ])
        >>> expected = Records([
            Record({'join_key': 1, 'left_other': 1, 'right_other': 4}),
            Record({'join_key': 2, 'left_other': 2, 'right_other': 3}),
        ])
        >>> left_records.merge(right_records, 'join_key').equals(expected)
        True

        """
        pass

    @abstractmethod
    def merge_sequencial(
        self,
        right_records: RecordsInterface,
        left_stamp_key: str,
        right_stamp_key: str,
        join_key: Optional[str],
        how: str = 'inner',
        *,
        progress_label: Optional[str] = None
    ) -> Records:
        """
        Merge chronologically contiguous records.

        Merge left_records[left_key] and the right_records[right_key]
        that occurred immediately after it.
        If join_key is set, left_records[join_key]==right_records[join_key] is added as condition.


        Parameters
        ----------
        right_records : RecordsInterface
            merge target.
        left_stamp_key : str
            left records key name to use for comparison in time series merge.
        right_stamp_key : str
            right records key name to use for comparison in time series merge.
        join_key : str
            join key name to use equal condition.
        how : str
            merge type. [inner/right/left/outer]
        progress_label : str
            label for progress bar. cpp impl only.

        Records
        -------
        RecordsInterface
            Merged records.

        Example
        -------
        >>> left_records = Records([
            Record({'join_key': 1, 'left_stamp_key': 0}),
            Record({'join_key': 2, 'left_stamp_key': 3})
        ])
        >>> right_records = Records([
            Record({'join_key': 2, 'right_stamp_key': 5}),
            Record({'join_key': 1, 'right_stamp_key': 6})
        ])
        >>> expected = Records([
            Record({'join_key': 1, 'left_stamp_key': 0, 'right_stamp_key': 6}),
            Record({'join_key': 2, 'left_stamp_key': 3, 'right_stamp_key': 5}),
        ])
        >>> left_records.merge_sequencial(
            right_records, 'left_stamp_key', 'right_stamp_key', 'join_key', 'inner'
        ).equals(expected)
        True


        """
        pass

    @abstractmethod
    def merge_sequencial_for_addr_track(
        self,
        source_stamp_key: str,
        source_key: str,
        copy_records: RecordsInterface,
        copy_stamp_key: str,
        copy_from_key: str,
        copy_to_key: str,
        sink_records: RecordsInterface,
        sink_stamp_key: str,
        sink_from_key: str,
        *,
        progress_label: Optional[str] = None
    ) -> RecordsInterface:
        """
        Merge for tracking addresses when copying occurs.

        Parameters
        ----------
        source_stamp_key : str
            key name indicating time stamp for source records
        source_key : str
            Key name indicating the address of the copy source for source records.
        copy_records : Recordsinterface
            copy records
        copy_stamp_key : str
            key name indicating time stamp for copy records
        copy_from_key : str
            Key name indicating the address of the copy source for source records.
        copy_to_key : str
            Key name indicating the address of the copy destination
        sink_records : RecordsInterface
            sink-side records
        sink_stamp_key : str
            keyname indicating time stamp for copy records
        sink_from_key : str
            Key name indicating the address of the copy destination
        progress_label : str
            label for progress bar. cpp impl only.

        Returns
        -------
        RecordsInterface
            Merged records.

        Examples
        --------
        >>> source_records = Records([
            Record({'source_key': 1, 'source_stamp': 0}),
        ])
        >>> copy_records = Records([
            Record({'copy_from_key': 1, 'copy_to_key': 11, 'copy_stamp_key': 1})
        ])
        >>> sink_records = Records([
            Record({'sink_from_key': 11, 'sink_stamp': 2}),
            Record({'sink_from_key': 1, 'sink_stamp': 3}),
        ])
        >>> expected = Records([
            Record({'source_stamp':0, 'sink_stamp':3, 'source_key':1}),
            Record({'source_stamp':0, 'sink_stamp':2, 'source_key':1}),
        ])
        >>> source_records.merge_sequencial_for_addr_track(
            'source_stamp', 'source_key', copy_records, 'copy_stamp_key', 'copy_from_key',
            'copy_to_key', sink_records, 'sink_stamp', 'sink_from_key'
        ).equals(expected)
        True

        """
        pass

    @abstractmethod
    def clone(self) -> RecordsInterface:
        """
        Get duplicated records.

        Returns
        -------
        RecordsInterface
            deep-copyed records.

        """
        pass

    @abstractmethod
    def bind_drop_as_delay(self, sort_key: str) -> None:
        """
        Convert the dropped points to records converted as delay.

        TODO
        ----
        Modify to return converted value

        """
        pass


class MergeSideInfo(IntEnum):
    LEFT = 0
    RIGHT = 1


# class Record(collections.UserDict, RecordInterface):
class Record(RecordInterface):

    def __init__(self, init: Optional[Dict] = None) -> None:
        init = init or {}
        self._data = init or {}
        self._columns = set(init.keys())

    def get(self, key: str) -> int:
        return self._data[key]

    @property
    def data(self) -> Dict[str, int]:
        return self._data

    @property
    def columns(self) -> Set[str]:
        return self._columns

    def drop_columns(self, columns: List[str], inplace=False) -> Optional[Record]:
        data: Dict[str, int]

        if inplace:
            data = self._data
        else:
            data = deepcopy(self)._data

        for column in columns:
            if column not in self.columns:
                continue
            del data[column]

        if inplace:
            self._columns -= set(columns)
            return None
        else:
            return Record(data)

    def equals(self, other: Record) -> bool:  # type: ignore
        is_columns_equal = self.columns == other.columns
        if is_columns_equal is False:
            return False
        return self.data == other.data

    def add(self, key: str, stamp: int):
        self.columns.add(key)
        self._data[key] = stamp

    def merge(self, other: Record, inplace=False) -> Optional[Record]:  # type: ignore
        if inplace:
            self._data.update(other.data)
            self._columns |= other.columns
            return None
        else:
            d = deepcopy(self.data)
            d.update(deepcopy(other.data))
            return Record(d)

    def change_dict_key(self, old_key: str, new_key: str) -> None:
        self._data[new_key] = self._data.pop(old_key, None)
        self._columns -= {old_key}
        self._columns |= {new_key}


class Records(RecordsInterface):

    def __init__(self, init: Optional[List[Record]] = None):
        self._columns: Set[str] = set()
        for record in init or []:
            self._columns |= record.columns
        self._data: List[Record] = init or []

    @property
    def columns(self) -> Set[str]:
        return self._columns

    def sort(
        self, key: str, sub_key: Optional[str] = None, inplace=False, ascending=True
    ) -> Optional[Records]:
        if inplace:
            data = self.data
        else:
            data = deepcopy(self.data)

        if ascending:
            if sub_key is None:
                data.sort(key=lambda record: record.get(key))
            else:
                data.sort(
                    key=lambda record: (record.get(
                        key), record.get(sub_key))  # type: ignore
                )
        else:
            if sub_key is None:
                data.sort(key=lambda record: -record.get(key))
            else:
                data.sort(
                    key=lambda record: (-record.get(key), -
                                        record.get(sub_key))  # type: ignore
                )

        if inplace:
            return None
        else:
            return Records(data)

    def copy(self) -> Records:
        return deepcopy(self)

    @property
    def data(self) -> List[Record]:  # type: ignore
        return self._data

    def append(self, other: Record):  # type: ignore
        assert isinstance(other, Record)
        self._data.append(other)
        self._columns |= other.columns

    def concat(self, other: Records, inplace=False) -> Optional[Records]:  # type: ignore
        if inplace:
            self._data += other._data
            self._columns |= other.columns
            return None
        else:
            d = deepcopy(self._data)
            d += deepcopy(other._data)
            return Records(d)

    def drop_columns(self, columns: List[str], inplace: bool = False) -> Optional[Records]:
        data: List[Record]

        if inplace:
            data = self._data
        else:
            data = deepcopy(self._data)

        for record in data:
            record.drop_columns(columns, inplace=True)

        if not inplace:
            return Records(data)
        else:
            self._columns -= set(columns)
            return None

    def rename_columns(self, columns: Dict[str, str], inplace: bool = False) -> Optional[Records]:
        self._columns -= set(columns.keys())
        self._columns |= set(columns.values())

        data: List[Record]
        if inplace:
            data = self._data
        else:
            data = deepcopy(self._data)

        for record in data:
            for key_from, key_to in columns.items():
                if key_from not in record.columns:
                    continue
                record.change_dict_key(key_from, key_to)

        if not inplace:
            return Records(data)
        else:
            return None

    def filter_if(self, f: Callable[[Record], bool], inplace: bool = False) -> Optional[Records]:
        records = Records()
        init_columns = self.columns
        for record in self._data:  # type: Record
            if f(record):
                records.append(record)

        if not inplace:
            records._columns = init_columns
            records._data = deepcopy(records._data)
            return records
        else:
            self._data = records._data
            return None

    def equals(self, records: Records) -> bool:  # type: ignore
        if len(self.data) != len(records.data):
            return False

        for r, r_ in zip(self.data, records.data):
            if r.equals(r_) is False:
                return False

        if self._columns != records._columns:
            return False

        return True

    def to_dataframe(self) -> pd.DataFrame:
        pd_dict = [record.data for record in self.data]
        df = pd.DataFrame.from_dict(pd_dict)
        missing_columns = set(self.columns) - set(df.columns)
        df_miss = pd.DataFrame(columns=missing_columns)
        df = pd.concat([df, df_miss])
        return df

    def to_string(self) -> str:
        return self.to_dataframe().to_string()

    def clone(self) -> Records:
        from copy import deepcopy

        return deepcopy(self)

    def bind_drop_as_delay(self, sort_key: str) -> None:
        self.sort(sort_key, sub_key=None, inplace=True, ascending=False)

        oldest_values: Dict[str, int] = {}

        for record in self.data:
            for key in self.columns:
                if key not in record.columns and key in oldest_values.keys():
                    record.add(key, oldest_values[key])
                if key in record.columns:
                    oldest_values[key] = record.data[key]

        self.sort(sort_key, sub_key=None, inplace=True, ascending=True)

    def merge(
        self,
        right_records: Records,
        join_key: str,
        how: str = 'inner',
        left_sort_key: Optional[str] = None,
        right_sort_key: Optional[str] = None,
        *,
        progress_label: Optional[str] = None  # unused
    ) -> Records:
        left_records = self

        merge_left = how in ['left', 'outer']
        merge_right = how in ['right', 'outer']

        merged_records = Records()
        assert how in ['inner', 'left', 'right', 'outer']

        for left in left_records.data:
            left.add('side', MergeSideInfo.LEFT)  # type: ignore

        for right in right_records.data:
            right.add('side', MergeSideInfo.RIGHT)  # type: ignore

        records: Records
        records = left_records.concat(right_records)  # type: ignore

        for record in records._data:
            record.add('has_valid_join_key', join_key in record.columns)
            if join_key in record.columns:
                record.add('merge_stamp', record.get(join_key))
            else:
                record.add('merge_stamp', sys.maxsize)

        records.sort(key='merge_stamp', sub_key='side', inplace=True)

        empty_records: List[Record] = []
        left_record_: Optional[Record] = None

        for record in records._data:
            if record.get('has_valid_join_key') is False:
                if record.get('side') == MergeSideInfo.LEFT and merge_left:
                    merged_records.append(record)
                elif record.get('side') == MergeSideInfo.RIGHT and merge_right:
                    merged_records.append(record)
                continue

            join_value = record.get(join_key)

            if record.get('side') == MergeSideInfo.LEFT:
                if left_record_ and left_record_.get('found_right_record') is False:
                    empty_records.append(left_record_)
                left_record_ = record
                left_record_.add('found_right_record', False)
            else:
                if (
                    left_record_
                    and join_value == left_record_.get(join_key)
                    and record.get('has_valid_join_key')
                ):
                    left_record_.add('found_right_record', True)
                    merged_record = deepcopy(record)
                    merged_record.merge(left_record_, inplace=True)
                    merged_records.append(merged_record)
                else:
                    empty_records.append(record)
        if left_record_ is not None and left_record_.get('found_right_record') is False:
            empty_records.append(left_record_)

        for record in empty_records:
            side = record.get('side')
            if side == MergeSideInfo.LEFT and merge_left:
                merged_records.append(record)
            elif side == MergeSideInfo.RIGHT and merge_right:
                merged_records.append(record)

        temporay_columns = ['side', 'merge_stamp',
                            'has_valid_join_key', 'found_right_record']
        merged_records.drop_columns(temporay_columns, inplace=True)
        left_records.drop_columns(temporay_columns, inplace=True)
        right_records.drop_columns(temporay_columns, inplace=True)

        return merged_records

    def merge_sequencial(  # type: ignore
        self,
        right_records: Records,
        left_stamp_key: str,
        right_stamp_key: str,
        join_key: Optional[str],
        how: str = 'inner',
        *,
        progress_label: Optional[str] = None  # unused
    ) -> Records:
        assert how in ['inner', 'left', 'right', 'outer']

        left_records = self

        merge_left = how in ['left', 'outer']
        merge_right = how in ['right', 'outer']

        merged_records: Records = Records()

        for left in left_records.data:
            left.add('side', MergeSideInfo.LEFT)  # type: ignore

        for right in right_records.data:
            right.add('side', MergeSideInfo.RIGHT)  # type: ignore

        records: Records
        records = left_records.concat(right_records)  # type: ignore

        for record in records._data:
            record.add('has_valid_join_key',
                       join_key is None or join_key in record.columns)
            if record.get('side') == MergeSideInfo.LEFT and left_stamp_key in record.columns:
                record.add('merge_stamp', record.get(left_stamp_key))
                record.add('has_merge_stamp', True)
            elif record.get('side') == MergeSideInfo.RIGHT and right_stamp_key in record.columns:
                record.add('has_merge_stamp', True)
                record.add('merge_stamp', record.get(right_stamp_key))
            else:
                record.add('merge_stamp', sys.maxsize)
                record.add('has_merge_stamp', False)

        records.sort(key='merge_stamp', inplace=True)

        def get_join_value(record: RecordInterface) -> Optional[int]:
            if join_key is None:
                return 0
            elif join_key in record.columns:
                return record.get(join_key)
            else:
                return None

        left_records_with_empty_sub_record: Dict[int, Record] = {}
        for record in records._data:
            if record.get('side') == MergeSideInfo.LEFT and record.get('has_merge_stamp'):
                record.add('sub_record', None)  # type: ignore

                join_value = get_join_value(record)
                if join_value is None:
                    continue
                left_records_with_empty_sub_record[join_value] = record
            elif record.get('side') == MergeSideInfo.RIGHT and record.get('has_merge_stamp'):
                join_value = get_join_value(record)
                if join_value is None:
                    continue
                if join_value in left_records_with_empty_sub_record.keys():
                    left_record_to_be_bind = left_records_with_empty_sub_record[join_value]
                    left_record_to_be_bind._data['sub_record'] = record
                    del left_records_with_empty_sub_record[join_value]

        added: Set[Record] = set()
        for i, current_record in enumerate(records._data):
            recorded = current_record in added

            if recorded:
                continue

            if not current_record.get('has_merge_stamp') or not current_record.get(
                'has_valid_join_key'
            ):
                if current_record.get('side') == MergeSideInfo.RIGHT and merge_right:
                    merged_records.append(current_record)
                    added.add(current_record)
                elif current_record.get('side') == MergeSideInfo.LEFT and merge_left:
                    merged_records.append(current_record)
                    added.add(current_record)
                continue

            if current_record.get('side') == MergeSideInfo.RIGHT:
                if merge_right:
                    merged_records.append(current_record)
                    added.add(current_record)
                continue

            sub_record: Optional[Record] = current_record._data['sub_record']

            if sub_record is None or sub_record in added:
                if merge_left:
                    merged_records.append(current_record)
                    added.add(current_record)
                continue

            merged_record = Record()
            merged_record.merge(current_record, inplace=True)
            merged_record.merge(sub_record, inplace=True)
            merged_records.append(merged_record)
            added.add(current_record)
            added.add(sub_record)

        temporay_columns = [
            'side',
            'merge_stamp',
            'has_merge_stamp',
            'has_valid_join_key',
            'sub_record',
        ]
        merged_records.drop_columns(temporay_columns, inplace=True)
        left_records.drop_columns(temporay_columns, inplace=True)
        right_records.drop_columns(temporay_columns, inplace=True)

        return merged_records

    def merge_sequencial_for_addr_track(  # type: ignore
        self,
        source_stamp_key: str,
        source_key: str,
        copy_records: Records,
        copy_stamp_key: str,
        copy_from_key: str,
        copy_to_key: str,
        sink_records: Records,
        sink_stamp_key: str,
        sink_from_key: str,
        *,
        progress_label: Optional[str] = None  # unused
    ) -> Records:

        source_records = deepcopy(self)
        copy_records = deepcopy(copy_records)
        sink_records = deepcopy(sink_records)

        merged_records: Records = Records()

        for record in source_records.data:
            record.add('type', RecordType.SOURCE)  # type: ignore
            record.add('timestamp', record.get(source_stamp_key))
        for record in copy_records.data:
            record.add('type', RecordType.COPY)  # type: ignore
            record.add('timestamp', record.get(copy_stamp_key))
        for record in sink_records.data:
            record.add('type', RecordType.SINK)  # type: ignore
            record.add('timestamp', record.get(sink_stamp_key))

        records = Records(source_records._data +
                          copy_records._data + sink_records._data)
        records.sort('timestamp', ascending=False, inplace=True)
        # Searching for records in chronological order is not good
        # because the lost records stay forever. Sort in reverse chronological order.

        #  List of records to be added by sink and removed by source
        processing_records: List[Record] = []

        def merge_processing_record_keys(processing_record: Record):
            for processing_record_ in filter(
                lambda x: x.get(sink_from_key) & processing_record.get(
                    sink_from_key)
                and x.get(sink_from_key) != processing_record.get(sink_from_key),
                processing_records,
            ):
                processing_record_keys = processing_record.get(sink_from_key)
                coresponding_record_keys = processing_record_.get(
                    sink_from_key)

                merged_set = processing_record_keys | coresponding_record_keys
                processing_record.data[sink_from_key] = merged_set
                processing_record_.data[sink_from_key] = merged_set

        for record in records.data:
            if record.get('type') == RecordType.SINK:
                record._data[sink_from_key] = {record.get(sink_from_key)}
                processing_records.append(record)

            elif record.get('type') == RecordType.COPY:
                records_need_to_merge = filter(
                    lambda x: record.get(
                        copy_to_key) in x._data[sink_from_key], processing_records
                )
                for processing_record in records_need_to_merge:
                    processing_record._data[sink_from_key].add(
                        record.get(copy_from_key))
                    merge_processing_record_keys(processing_record)
                    # No need for subsequent loops since we integrated them.
                    break

            elif record.get('type') == RecordType.SOURCE:
                for processing_record in filter(
                    lambda x: record.get(source_key) in x._data[sink_from_key],
                    processing_records[:],
                ):
                    processing_records.remove(processing_record)
                    processing_record.merge(record, inplace=True)
                    merged_records.append(processing_record)

        # Deleting an added key
        merged_records.drop_columns(
            ['type', 'timestamp', sink_from_key], inplace=True)

        return merged_records


def merge(
    left_records: RecordsInterface,
    right_records: RecordsInterface,
    join_key: str,
    how: str = 'inner',
    *,
    progress_label: Optional[str] = None
) -> Records:
    assert type(left_records) == type(right_records)

    return left_records.merge(
        right_records, join_key, how, progress_label=progress_label  # type: ignore
    )


def merge_sequencial(
    left_records: RecordsInterface,
    right_records: RecordsInterface,
    left_stamp_key: str,
    right_stamp_key: str,
    join_key: Optional[str],
    how: str = 'inner',
    *,
    progress_label: Optional[str] = None
) -> Records:
    assert type(left_records) == type(right_records)

    return left_records.merge_sequencial(
        right_records,  # type: ignore
        left_stamp_key,
        right_stamp_key,
        join_key,
        how,
        progress_label=progress_label,
    )


class RecordType(IntEnum):
    SOURCE = (0,)
    COPY = (1,)
    SINK = 2


def merge_sequencial_for_addr_track(
    source_records: RecordsInterface,
    source_stamp_key: str,
    source_key: str,
    copy_records: RecordsInterface,
    copy_stamp_key: str,
    copy_from_key: str,
    copy_to_key: str,
    sink_records: RecordsInterface,
    sink_stamp_key: str,
    sink_from_key: str,
    *,
    progress_label: Optional[str] = None
):
    assert type(source_records) == type(copy_records) and type(
        copy_records) == type(sink_records)

    return source_records.merge_sequencial_for_addr_track(
        source_stamp_key,
        source_key,
        copy_records,  # type: ignore
        copy_stamp_key,
        copy_from_key,
        copy_to_key,
        sink_records,  # type: ignore
        sink_stamp_key,
        sink_from_key,
        progress_label=progress_label,
    )
