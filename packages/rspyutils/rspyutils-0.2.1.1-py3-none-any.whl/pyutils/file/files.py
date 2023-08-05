# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on MAY 21, 2018
@author: zlh
"""
import os
import re
import pandas as pd
from pyutils.time import dates

FILE_CSV = ".csv"
FILE_PKL = ".pkl"


class FilesOp(object):
    def __init__(self):
        pass

    def file_repalce(self, source, dest):
        os.replace(source, dest)

    def get_dir_path(self, file):
        return os.path.abspath(os.path.dirname(file))

    def get_updir_path(self, file):
        return os.path.dirname(self.get_dir_path(file))

    def get_upupdir_path(self, file):
        return os.path.dirname(self.get_updir_path(file))

    def get_dir_file_name(self, file_dir, suffix=None):
        files = list()
        for walker in os.walk(file_dir):
            if walker[2]:
                for w in walker[2]:
                    file_path = os.path.join(str(walker[0]), str(w))
                    if suffix and os.path.splitext(file_path)[1] == suffix:
                        files.append(file_path)
                    elif suffix is None:
                        files.append(file_path)
        return files

    def get_csv_data(self, file_path, *args, **kwargs):
        return pd.read_csv(file_path, *args, **kwargs)

    def get_pickle_data(self, file_path):
        return pd.read_pickle(file_path)

    def get_multi_csv_data(self, file_path, max_len=-1, *args, **kwargs):
        file_num = 0
        frames = []
        for f in self.get_dir_file_name(file_path, suffix=FILE_CSV):
            frames.append(pd.read_csv(f, *args, **kwargs))
            file_num += 1
            if max_len > 0 and file_num >= max_len:
                break
        result = pd.concat(frames)
        return result

    def get_multi_pickle_data(self, file_path, max_len=-1):
        file_num = 0
        frames = []
        for x in self.get_dir_file_name(file_path, suffix=FILE_PKL):
            frames.append(pd.read_pickle(x))
            file_num += 1
            if file_num >= max_len:
                break
        result = pd.concat(frames)
        return result

    def rm_file_by_date(self, file_path, date_len=30, suffix=FILE_CSV):
        thr_date = dates.get_before_date(date_len).strftime("%Y-%m-%d")
        for x in self.get_dir_file_name(file_path, suffix=suffix):
            file_date = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})", x)
            if file_date and dates.get_date_compare(thr_date, file_date[0]):
                os.remove(x)


if __name__ == "__main__":
    # print(FilesOp().get_dir_file_name("/home/zhanglanhui/recommend_workspace/jupyter/csv/csv"))
    print(FilesOp().get_multi_csv_data("/home/zhanglanhui/recommend_workspace/jupyter/csv/csv", max_len=3,
                                       sep="$"))
