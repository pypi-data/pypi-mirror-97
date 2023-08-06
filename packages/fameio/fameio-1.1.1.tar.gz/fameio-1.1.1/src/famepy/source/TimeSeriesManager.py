# !/usr/bin/env python
# -*- coding:utf-8 -*-

import pandas as pd

from .FameTime import FameTime, START_IN_REAL_TIME


class TimeSeriesManager:
    """Manages matching of files to time series ids and their protobuf representation"""
    ids_of_time_series = {}
    id_count = -1
    already_registered = "file already registered"

    def get_time_series_id(self, file_name):
        """Returns the id assigned to the given file name"""
        return self.ids_of_time_series.get(file_name)

    def time_series_is_registered(self, file_name):
        """Returns True if the file is already registered"""
        return file_name in self.ids_of_time_series.keys()

    def register_time_series(self, file_name):
        """Assigns an id to the given file or raises an Exception if the file is already registered"""
        if not self.time_series_is_registered(file_name):
            self.id_count += 1
            self.ids_of_time_series[file_name] = self.id_count
        else:
            raise Exception(TimeSeriesManager.already_registered)

    def save_get_time_series_id(self, file_name):
        """Returns the id of the time series - if the file is not yet registered, assigns an id"""
        if not self.time_series_is_registered(file_name):
            self.register_time_series(file_name)
        return self.get_time_series_id(file_name)

    def add_time_series_to_proto_buffer(self, proto_buffer):
        """Adds all registered files to given protobuf time series"""
        for identifier, unique_id in self.ids_of_time_series.items():
            series = proto_buffer.timeSeries.add()
            series.seriesId = unique_id
            if isinstance(identifier, str):
                series.seriesName = identifier
                data_frame = pd.read_csv(identifier, sep=';', header=None)
                TimeSeriesManager.add_rows_to_series(series, data_frame)
            else:
                series.seriesName = "Constant value: {}".format(identifier)
                data_frame = pd.DataFrame({'time': [START_IN_REAL_TIME],
                                           'value': [identifier],
                                           })
                TimeSeriesManager.add_rows_to_series(series, data_frame)

    @staticmethod
    def add_rows_to_series(series, data_frame):
        for (datetime_string, value) in data_frame.itertuples(index=False):
            row = series.row.add()
            row.timeStep = int(FameTime.convert_time_string_to_fame_time_step(datetime_string))
            row.value = value
