# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on MAY 21, 2018
@author: zlh
"""
import datetime
import time


def decode_strings_from_buf(addrs, lens):
  """ get string at index by addrs and lens
    """
  strings = list()
  assert len(addrs) == len(lens)
  for i in range(len(lens)):
    if lens[i] > 0:
      strings.append("".join(map(chr, addrs[i, 0:lens[i]])))
  return strings

def str_to_timestamp(s, format='%Y%m%d%H%M%S', accuracy='us'):
  t = datetime.strptime(s, format)
  ts = int(time.mktime(t.timetuple()))
  if accuracy == 's':
    return ts
  elif accuracy == 'ms':
    return ts * 1000
  elif accuracy == 'us':
    return ts * 1000 * 1000
  else:
    raise RuntimeError('unknown accuracy %s' % accuracy)

def timestamp_to_str(ts, format='%Y%m%d%H%M%S', accuracy='us'):
  if accuracy == 'us':
    ts = ts / 1000 / 1000
  elif accuracy == 'ms':
    ts = ts / 1000
  t = datetime.fromtimestamp(ts)
  return datetime.strftime(t, format)


def get_before_date(days=1):
    if days >= 0:
        today = datetime.date.today()
        oneday = datetime.timedelta(days=days)
        yesterday = today - oneday
        return yesterday
    else:
        return None


def get_after_date(days=1):
    if days >= 0:
        today = datetime.date.today()
        oneday = datetime.timedelta(days=days)
        yesterday = today + oneday
        return yesterday
    else:
        return None


def getYesterday():
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    return yesterday


def today_time_d():
    return time.strftime("%Y-%m-%d", time.localtime())


def today_time_s():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_date_from_timstamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def get_date_from_str(dtstr, format="%Y-%m-%d"):
    return datetime.datetime.strptime(dtstr, format)


def get_date_compare(dtstr1=None, dtstr2=None, format='%Y-%m-%d'):
    if dtstr1 and dtstr2:
        date1 = get_date_from_str(dtstr1, format).date()
        date2 = get_date_from_str(dtstr2, format).date()
        return date1 > date2
    return None


# 定义时间差函数
def get_date_diff(start_date: str, end_date: str):
    startTime = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    endTime = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    diff = endTime - startTime
    return diff


def str_to_timestamp(str_time=None, format='%Y-%m-%d %H:%M:%S'):
    if str_time:
        time_tuple = time.strptime(str_time, format)  # 把格式化好的时间转换成元祖
        result = time.mktime(time_tuple)  # 把时间元祖转换成时间戳
        return int(result)
    return int(time.time())


if __name__ == "__main__":
    print(get_after_date(1))
    print(get_before_date(1))
    print(today_time_s())
    date1 = "2017-06-07"
    date2 = "2017-06-09"
    print(get_date_compare(date1, date2))
