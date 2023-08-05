# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on MAY 21, 2018
@author: zlh
"""
import json
import math
import datetime
import numpy as np
import pandas as pd
from pyutils.time import dates
from pyutils.tool.list import get_flat_list
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler


class FeaturesEncode(object):
    def __init__(self):
        pass

    def get_df_cols(self, df: pd.DataFrame):
        return set(df.columns.tolist())

    def get_nan_transform(self, df: pd.DataFrame, cols: list, type="category", value=0, method="default"):
        """
        缺省值处理，当前只支持默认值，后面需要加上其他处理方式
        :param df: DataFrame
        :param cols: 字段
        :param type: 字段数值类型
        :param method: nan处理方式
        :return:
        """
        if not set(cols).issubset(self.get_df_cols(df)):
            raise ValueError("nan transform field input not found in DataFrame!!!")

        if method == "default":
            if type == "category":
                type, value = "object", str(value)
            elif type == "numerical":
                type, value = "float32", float(value)
            elif type == "time":
                type, value = "object", "1970-01-01 00:00:00"
            else:
                raise ValueError("nan transform type input %s is not support!!!" % type)
        elif method == "linear":
            if type == "numerical":
                type, value = "float32", float(value)
                for f in cols:
                    df[f] = df[f].interpolate(method='linear', axis=0)
            else:
                raise ValueError("nan transform only support numerical when method is linear!!!")
        else:
            raise ValueError("scaler transform field input %s not found in DataFrame!!!" % str(method))

        df = df.astype({x: type for x in cols})
        df.fillna({x: value for x in cols}, inplace=True)

        return df

    def get_scaler_transform(self, df: pd.DataFrame, field, is_log=False, base=math.exp(-1), method="normalize"):
        """
        get_scaler_transform 数值型特征数据归一化
        :param df: DataFrame
        :param field: 字段
        :param is_log: 是否取log
        :param method: 归一化方式
        :return:
        """
        if field not in self.get_df_cols(df):
            raise ValueError("scaler transform field input %s not found in DataFrame!!!" % str(field))

        if is_log:
            df[field] = df[field].parallel_apply(lambda x: math.log(max(x, base)))

        if "normalize" == method:
            norm = MinMaxScaler().fit_transform(df[field].values.astype(np.float64).reshape(-1, 1))
            df[field] = norm.astype(np.float64).reshape(-1)
        elif "standard" == method:
            norm = StandardScaler().fit_transform(df[field].values.astype(np.float64).reshape(-1, 1))
            df[field] = norm.astype(np.float64).reshape(-1)
        else:
            raise ValueError("scaler transform method %s input error!!!" % str(method))
        return df

    def get_discrete_transform(self, df: pd.DataFrame, field, block=10):
        """
        get_discrete_transform 连续值离散化
        :param df: DataFrame
        :param field: 字段
        :param block: 分段
        :return: 
        """
        if field not in self.get_df_cols(df):
            raise ValueError("discrete transform field input %s not found in DataFrame!!!" % str(field))

        df[field] = df[field].multiply(block).map(int).map(str)
        return df

    def get_time2category_transform(self, df: pd.DataFrame, field, method="timestamp", dim="day"):
        """
        get_time2category_transform 时间特征处理
        :param df: DataFrame
        :param field: 字段
        :param method: 数据分析方式
        :param dim: 维度
        :return: 
        """
        if field not in self.get_df_cols(df):
            raise ValueError("time transform field input %s not found in DataFrame!!!" % str(field))

        if method == "timestamp":
            if dim == "sec":
                df[field] = df[field].parallel_apply(lambda x: dates.str_to_timestamp(x))
            elif dim == "day":
                df[field] = df[field].parallel_apply(lambda x: dates.get_date_from_str(x).day)
            elif dim == "month":
                df[field] = df[field].parallel_apply(lambda x: dates.get_date_from_str(x).month)
            else:
                raise ValueError("time transform dim input %s error!!!" % str(dim))
        elif method == "timediff":
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if dim == "sec":
                df[field] = df[field].parallel_apply(lambda x: dates.get_date_diff(start_date=str(x),
                                                                                   end_date=now_time).seconds)
            elif dim == "day":
                df[field] = df[field].parallel_apply(lambda x: dates.get_date_diff(start_date=str(x),
                                                                                   end_date=now_time).days)
            elif dim == "month":
                df[field] = df[field].parallel_apply(lambda x: int(dates.get_date_diff(start_date=str(x),
                                                                                       end_date=now_time).days / 30.0))
            else:
                raise ValueError("time transform method input %s error!!!" % str(method))
        else:
            raise ValueError("time2category transform method input error!!!")
        return df

    def get_singular_truncation_transform(self, df: pd.DataFrame, field, thr=None, method="min"):
        """
        get_singular_truncation_transform 浮点值奇异值校正
        :param df: DataFrame
        :param field: 字段
        :param thr: 阈值
        :param method: 方式
        :return:
        """
        if field not in self.get_df_cols(df):
            raise ValueError("singular transform field input %s not found in DataFrame!!!" % str(field))

        if not thr:
            return df

        if method == "min":
            df[field] = df[field].parallel_apply(lambda x: min(x, thr))
        else:
            df[field] = df[field].parallel_apply(lambda x: max(x, thr))

        return df

    def get_category_type_transform(self, df: pd.DataFrame, field, is_int: False):
        """
        get_category_type_transform
        :param df: DataFrame
        :param field: 字段
        :param is_int: 是否需要转成int
        :return:
        """
        if field not in self.get_df_cols(df):
            raise ValueError("category type transform field input %s not found in DataFrame!!!" % str(field))

        if df[field].dtype == 'float64' or df[field].dtype == 'float32' or is_int:
            df[field] = df[field].map(int).map(str)
        df[field] = df[field].astype("category")

        return df

    def get_json2category_transform(self, df: pd.DataFrame, cols: list):
        """
        json特征处理 json to category
        :param df:
        :param cols:
        :return:
        """

        def func(d):
            try:
                return "|".join(json.loads(d).keys())
            except:
                return ""

        if not cols:
            return df

        for k in cols:
            df[k] = df.parallel_apply(lambda x: func(x[k]), axis=1)

        return df

    def get_vector2category_transform(self, df: pd.DataFrame, cols: list, is_drop=True):
        """
        多维特征处理(暂时弃用)
        :param df:
        :param cols:
        :param is_drop:
        :return:
        """
        drop_features = []
        category_features_gen = []
        if not cols:
            return []
        df_vector = df
        for v in cols:
            if v in self.get_df_cols(df):
                dfTmp = df_vector[v].str.get_dummies(sep='|')
                dfTmp.rename(columns=lambda x: v + "|" + x, inplace=True)
                df_vector = df_vector.join(dfTmp)
                drop_features.append(v)
                category_features_gen.append(dfTmp.columns.tolist())
                del dfTmp
        if is_drop:
            df_vector.drop(drop_features, axis=1, inplace=True)
        return df_vector, category_features_gen

    def get_vector2value_transform(self, df: pd.DataFrame, cols: list, is_drop=True):
        """
        多维特征处理
        :param df:
        :param cols:
        :param is_drop:
        :return:
        """
        drop_features = []
        value_features_gen = []
        if not cols:
            return df, []
        df_vector = df
        for v in cols:
            if v in self.get_df_cols(df):
                val = np.array([str.split(x, ",") for x in df[v].values])
                index = [v + ":" + str(i) for i in range(1, len(val) + 1)]
                dfTmp = pd.DataFrame(val, index=index)
                df_vector = df_vector.join(dfTmp)
                drop_features.append(v)
                value_features_gen.append(dfTmp.columns.tolist())
                del dfTmp
        if is_drop:
            df_vector.drop(drop_features, axis=1, inplace=True)
        return df_vector, value_features_gen

    # 构造交叉特征
    def get_cross_transform(self, df: pd.DataFrame, field1, field2, vector_col=None):
        """
        get_cross_transform
        :param df:
        :param field1:
        :param field2:
        :param vector_col:
        :return:
        """

        def func1(df: pd.DataFrame, col1: str, col2: str):
            return '|'.join(['{}*{}'.format(x, df[col2]) for x in str.split(df[col1], "|")])

        def func2(df: pd.DataFrame, col1: str, col2: str):
            return '|'.join(['{}*{}'.format(x, y) for x in str.split(df[col1], "|")
                             for y in str.split(df[col2], "|")])

        if field1 not in self.get_df_cols(df) or field2 not in self.get_df_cols(df):
            raise ValueError("cross transform field input %s or %s not found in DataFrame!!!" % (field1, field2))

        new_field = '{}*{}'.format(field1, field2)
        if field1 in set(vector_col) and field2 in set(vector_col):
            df[new_field] = df.parallel_apply(lambda x: func2(x, field1, field2), axis=1)
        elif field1 in set(vector_col):
            df[new_field] = df.parallel_apply(lambda x: func1(x, field1, field2), axis=1)
        elif field2 in set(vector_col):
            df[new_field] = df.parallel_apply(lambda x: func1(x, field2, field1), axis=1)
        else:
            df[new_field] = df[field1].astype("object").map(str) + \
                            "*" + \
                            df[field2].astype("object").map(str)
        df[new_field] = df[new_field].astype("category")
        return df

    def gen_features_id_map(self, df: pd.DataFrame, feature_id: dict, vector, label="label"):
        """
        gen_features_id_map
        :param df:
        :param feature_id:
        :param vector:
        :param label:
        :return:
        """
        cols = self.get_df_cols(df)
        cols.remove(label)
        feature_id_list = []
        for c in cols:
            if c in vector:
                feature_id_list.extend(["{}:{}".format(c, x) for d in df[c]
                                        for x in set(get_flat_list([str.split(d, "|")]))])
            else:
                feature_id_list.extend(["{}:{}".format(c, x) for x in list(df[c].drop_duplicates())])
        max_len = max(feature_id.values()) if feature_id else 0
        for x in feature_id_list:
            if not feature_id.get(x, None):
                max_len += 1
                feature_id[x] = max_len
        return feature_id
