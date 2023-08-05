# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on MAY 21, 2018
@author: zlh
"""
# 以下两个模块可以通过 pip install thrift 安装获得
import pprint

from thrift.protocol import TBinaryProtocol
from thrift.transport import THttpClient

# 下面的模块通过 thrift --gen py hbase.thrift 来生成
from pyutils.bigdata.hbases.thrift2.hbase import THBaseService
from pyutils.bigdata.hbases.thrift2.hbase.ttypes import TColumn, TTableName, TTableDescriptor, TColumnFamilyDescriptor, \
    TNamespaceDescriptor, TGet, TColumnValue


class HBaseCli(object):

    def __init__(self, url, headers=None):
        """
        create connection to hive server2
        headers = {}
        # 用户名
        headers["ACCESSKEYID"] = "root";
        # 密码
        headers["ACCESSSIGNATURE"] = "root"
        """
        try:
            # 连接地址
            # url = "http://ld-bp17y8n3j6f45p944-proxy-hbaseue.hbaseue.rds.aliyuncs.com:30020"
            transport = THttpClient.THttpClient(url)
            transport.setCustomHeaders(headers)
            protocol = TBinaryProtocol.TBinaryProtocolAccelerated(transport)
            self.client = THBaseService.Client(protocol)
            transport.open()
        except Exception as e:
            raise e

    def createNamespace(self, ns):
        self.client.createNamespace(TNamespaceDescriptor(name=ns))

    def createTable(self, ns, qualifier, family):
        # create table
        # 必须要先创建namespace
        tableName = TTableName(ns=ns, qualifier=qualifier)
        self.client.createTable(TTableDescriptor(tableName=tableName, columns=[
            TColumnFamilyDescriptor(name=family)
        ]), None)

    @staticmethod
    def _decode_from_result(result):
        def get_key(family, qualifier):
            return "{}:{}".format(family, qualifier)

        return {get_key(x.family.decode('utf-8'), x.qualifier.decode('utf-8')): x.value.decode('utf-8') for x in result}

    @staticmethod
    def _decode_from_results(result):
        def get_key(family, qualifier):
            return "{}:{}".format(family, qualifier)

        return [{get_key(xx.family.decode('utf-8'), xx.qualifier.decode('utf-8')): xx.value.decode('utf-8') for xx in
                 x.columnValues} for x in result]

    def get(self, ns, tableName, row):
        # 单行查询数据
        tableInbytes = "{ns}:{tableName}".format(ns=ns, tableName=tableName).encode("utf8")
        result = self.client.get(tableInbytes, TGet(row=row.encode("utf8")))
        return self._decode_from_result(result.columnValues)

    def getCols(self, ns, tableName, row, col):
        # 单行查询数据
        tableInbytes = "{ns}:{tableName}".format(ns=ns, tableName=tableName).encode("utf8")
        result = self.client.get(tableInbytes, TGet(row=row.encode("utf8"), columns=col))
        return self._decode_from_result(result.columnValues)

    def getMultiple(self, ns, tableName, rows):
        # 批量单行查询
        tableInbytes = "{ns}:{tableName}".format(ns=ns, tableName=tableName).encode("utf8")
        gets = [TGet(row=row.encode("utf8")) for row in rows]
        results = self.client.getMultiple(tableInbytes, gets)
        return self._decode_from_results(results)

    def getMultipleCols(self, ns, tableName, rows, col):
        # 批量单行查询
        tableInbytes = "{ns}:{tableName}".format(ns=ns, tableName=tableName).encode("utf8")
        gets = [TGet(row=row.encode("utf8"), columns=col) for row in rows]
        results = self.client.getMultiple(tableInbytes, gets)
        return self._decode_from_results(results)


if __name__ == "__main__":
    xx = HBaseCli(url="http://ld-bp17y8n3j6f45p944-proxy-hbaseue.hbaseue.rds.aliyuncs.com:9190",
                  headers={"ACCESSKEYID": "root", "ACCESSSIGNATURE": "root"})
    # xx.createNamespace("ddd")
    # xx.createTable(ns="ddd", qualifier="dd", family="pp")
    # print(xx.get(ns="recommend_samh", tableName="item_base", row="100012:comic"))
    # print(xx.get_col(ns="recommend_samh", tableName="item_base", row="100012:comic",
    #                  col=[TColumn(family="info", qualifier="content_size"),
    #                       TColumn(family="info", qualifier="copyright_type")]))
    # pprint.pprint(xx.getMultiple(ns="recommend_samh", tableName="item_base", rows=["100012:comic"]))
    pprint.pprint(xx.getMultipleCols(ns="recommend_samh", tableName="item_base", rows=["100012:comic","10140:comic"],
                                 col=[TColumn(family="info", qualifier="content_size"),
                                      TColumn(family="info", qualifier="copyright_type")]))
