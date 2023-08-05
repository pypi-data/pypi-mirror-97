# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on MAY 21, 2018
@author: zlh
"""
import pyarrow as pa
import re, os
from pyutils.time import dates


# 关于python操作hdfs的API可以查看官网:
# https://hdfscli.readthedocs.io/en/latest/api.html
class HDFSCli(object):
    def __init__(self, host="default", port=0, user=None):
        self.fs = pa.hdfs.connect(host, port, user=user)

    # 创建目录
    def mkdirs(self, hdfs_path):
        self.fs.mkdir(hdfs_path)

    # 删除hdfs文件
    def delete_hdfs_file(self, hdfs_path):
        self.fs.delete(hdfs_path)

    # 判断文档存在
    def is_exist_file(self, hdfs_path) -> bool:
        return self.fs.exists(hdfs_path)

    # 移动或者修改文件
    def move_or_rename(self, hdfs_src_path, hdfs_dst_path) -> bool:
        return self.fs.rename(hdfs_src_path, hdfs_dst_path)

    # 从hdfs获取文件到本地
    def get_from_hdfs(self, local_path, hdfs_path):
        self.fs.download(hdfs_path, local_path)

    # 上传文件到hdfs
    def put_to_hdfs(self, file_stream, hdfs_path):
        self.fs.upload(hdfs_path, file_stream)

    # 返回目录下的文件
    def list(self, hdfs_path):
        return self.fs.ls(hdfs_path)

    def rm_file_by_date(self, hdfs_path, date_len=30):
        thr_date = dates.get_before_date(date_len).strftime("%Y-%m-%d")
        for x in self.list(hdfs_path):
            file_date = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})", x)
            if file_date and dates.get_date_compare(thr_date, file_date[0]):
                self.delete_hdfs_file(os.path.join(hdfs_path, x))

    def rm_file_all(self, hdfs_path):
        for x in self.list(hdfs_path):
            self.delete_hdfs_file(os.path.join(hdfs_path, x))


if __name__ == '__main__':
    fs = HDFSCli()
    print("root ls", fs.list("/"))
