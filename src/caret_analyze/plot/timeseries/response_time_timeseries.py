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

from collections.abc import Sequence

import pandas as pd

from ..metrics_base import MetricsBase
from ...record import ColumnValue, RecordsFactory, RecordsInterface, ResponseTime
from ...runtime import Path


class ResponsetimeTimeSeries(MetricsBase):
    """Class that provides latency timeseries data."""

    def __init__(
        self,
        target_objects: Sequence[Path],
        case: str,
    ) -> None:
        super().__init__(target_objects)
        self._case = case

    def to_dataframe(self, xaxis_type: str = 'system_time') -> pd.DataFrame:
        timeseries_records_list = self.to_timeseries_records_list(xaxis_type)
        all_df = pd.DataFrame()
        for to, response_records in zip(self._target_objects, timeseries_records_list):
            response_df = response_records.to_dataframe()
            response_df[response_df.columns[-1]] *= 10**(-6)
            response_df.rename(
                columns={
                    response_df.columns[0]: 'path_start_timestamp [ns]',
                    response_df.columns[1]: 'response_time [ms]',
                },
                inplace=True
            )
            # TODO: Multi-column DataFrame are difficult for users to handle,
            #       so it should be a single-column DataFrame.
            response_df = self._add_top_level_column(response_df, to)
            all_df = pd.concat([all_df, response_df], axis=1)

        return all_df.sort_index(level=0, axis=1, sort_remaining=False)

    def to_timeseries_records_list(
        self,
        xaxis_type: str = 'system_time'
    ) -> list[RecordsInterface]:

        timeseries_records_list: list[RecordsInterface] = [
            _.to_records() for _ in self._target_objects
        ]

        if xaxis_type == 'sim_time':
            timeseries_records_list = \
                self._convert_timeseries_records_to_sim_time(timeseries_records_list)

        response_timeseries_list: list[RecordsInterface] = []
        for records in timeseries_records_list:
            response = ResponseTime(records)
            if self._case == 'best':
                response_timeseries_list.append(response.to_best_case_records())
            elif self._case == 'worst':
                response_timeseries_list.append(response.to_worst_case_records())
            elif self._case == 'all':
                response_timeseries_list.append(response.to_all_records())
           
        return response_timeseries_list

    # def _create_empty_records(
    #     self
    # ) -> RecordsInterface:
    #     return RecordsFactory.create_instance(columns=[
    #         ColumnValue(self._start_column), ColumnValue('response_time')
    #     ])

    # def _calcu_response_time(
    #         self,
    #         records: RecordsInterface,
    # ) -> RecordsInterface:
    #     start_column = records.columns[0]
    #     end_column = records.columns[-1]
    #     start_timestamps: list[int] = []
    #     end_timestamps: list[int] = []

    #     for record in records:
    #         if (start_column not in record.columns or
    #                 end_column not in record.columns):
    #             continue
    #         start_ts = record.get(start_column)
    #         end_ts = record.get(end_column)

    #         start_timestamps.append(start_ts)
    #         end_timestamps.append(end_ts)

    #     new_records = self._create_empty_records()
    #     for start_ts, end_ts in zip(start_timestamps, end_timestamps):
    #         record = {
    #             self._start_column: start_ts,
    #             'response_time': end_ts - start_ts
    #         }
    #         new_records.append(record)

    #     return new_records