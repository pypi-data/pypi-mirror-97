#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @XZGUtil    : 2020-12-23 21:28
# @Site    : 
# @File    : timeUtil.py
# @Software: PyCharm
"""
时间类
"""
import datetime
import time
import json
import requests
from dateutil.relativedelta import relativedelta  # 安装 pip install python-dateutil
from retrying import retry

def datetime_toString(dt: datetime) -> str:
    """
    把datetime转成字符串
    :param dt: datetime.datetime.now
    :return: '2020-01-01'
    """
    return dt.strftime("%Y-%m-%d")

def datetime_toString_detail(dt: datetime) -> str:
    """
    把datetime转成字符串 详细版
    :param dt: datetime.datetime.now
    :return: '2020-01-01'
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def string_toDatetime(string: str) -> datetime:
    """
    把字符串转成datetime
    :param string: '2020-01-01'
    :return:
    """
    return datetime.datetime.strptime(string, "%Y-%m-%d")


def string_toTimestamp(strTime: str) -> int:
    """
    把字符串转成时间戳形式
    :param strTime:'2020-01-01'
    :return:<class 'int'> 1577808000
    """
    return int(time.mktime(string_toDatetime(strTime).timetuple()))


def timestamp_toString(stamp: int) -> str:
    """
    把时间戳转成字符串形式
    :param stamp: 1577808000
    :return: '2020-01-01'
    """
    return time.strftime("%Y-%m-%d", time.localtime(stamp))

def ts_toStr_det(stamp: int) -> str:
    """
    把时间戳转成字符串形式精确到秒
    :param stamp: 1577808000
    :return: '2020-01-01'
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp))

def datetime_toTimestamp(dateTime):
    """
    把datetime类型转外时间戳形式
    :param dateTime:datetime.datetime.now()
    :return:<class 'int'> 1608731584
    """
    return int(time.mktime(dateTime.timetuple()))


def substract_DateTime(dateStr1: str, dateStr2: str) -> datetime:
    """
    返回两个日期之间的差
    :param dateStr1:'2020-01-01'
    :param dateStr2:'2020-01-01'
    :return:<class 'datetime.timedelta'> 60 days, 0:00:00
    """
    d1 = string_toDatetime(dateStr1)
    d2 = string_toDatetime(dateStr2)
    return d2 - d1


def substract_TimeStamp(dateStr1: str, dateStr2: str) -> int:
    """
     两个日期的 timestamp 差值
    :param dateStr1: '2020-01-01'
    :param dateStr2: '2020-02-01'
    :return: <class 'int'> -5184000
    """
    ts1 = string_toTimestamp(dateStr1)
    ts2 = string_toTimestamp(dateStr2)
    return ts1 - ts2


def compare_dateTime(dateStr1: str, dateStr2: str) -> bool:
    """
    两个日期的比较, 当然也可以用timestamep方法比较,都可以实现
    :param dateStr1:'2020-01-01'
    :param dateStr2:'2020-01-02'
    :return:<class 'bool'> False
    """
    date1 = string_toDatetime(dateStr1)
    date2 = string_toDatetime(dateStr2)
    return date1.date() > date2.date()


def dateTime_Add(dateStr: str, days=0, hours=0, minutes=0) -> datetime:
    """
    指定日期加上 一个时间段，天，小时，或分钟之后的日期
    :param dateStr:'2020-01-01'
    :param days:1
    :param hours:1
    :param minutes:1
    :return:<class 'datetime.datetime'> 2020-01-02 01:01:01
    """
    date1 = string_toDatetime(dateStr)
    return date1 + datetime.timedelta(days=days, hours=hours, minutes=minutes)


def format_nowtime_millisecond() -> int:
    """
    获取毫秒级时间戳
    :return:<class 'int'> eg:1608730762129
    """
    t = time.time()
    nowTime = int(round(t * 1000))
    return nowTime


def getBetweenDay(begin_date: str, end_date: str) -> list:
    """
    返回两个时间之间的日期列表
    :param begin_date:'2020-01-01'
    :param end_date:'2020-01-05'
    :return:<class 'list'> ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04', '2020-01-05']
    """
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list

def get_month_b_e_day(month = '202001'):
        """传入月份返回当前月份的起始终止日期"""
        year = month[0:4]
        mon = month[4:]
        mon = f'{int(mon) + 1}'
        next_month = int(year+mon)
        # print(next_month)
        if (next_month % 100 == 13):
            next_month = next_month - 12 + 100
        month_end_day = (datetime.datetime(int(str(next_month)[0:4]), int(str(next_month)[4:6]), 1) - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        month_begin_day = month_end_day.rsplit('-',1)[0]+'-01'
        return month_begin_day, month_end_day

def month_datelist(start_day):
        """
        传入月份，会生成当前月份到传入月份之间的所有月份的开始终止日期
        :param start_day:'2020-01'
        :return:[['2020-01-01', '2020-01-31'], ['2020-02-01', '2020-02-29'], ['2020-03-01', '2020-03-31']]
        """
        start_day = datetime.datetime.strptime(start_day, r"%Y-%m")
        end_day = datetime.datetime.now() - relativedelta(months=1)
        months = (end_day.year - start_day.year) * 12 + end_day.month - start_day.month
        month_range = ['%s%s' % (start_day.year + mon // 12, mon % 12 + 1)
                       for mon in range(start_day.month - 1, start_day.month + months)]
        month_list = []
        for nonth in month_range:
            month_begin_day, month_end_day = get_month_b_e_day(nonth)
            month_list.append([month_begin_day, month_end_day])
        return month_list


def getdate(beforeOfDay):
    """
    获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
    :param beforeOfDay:
    :return:
    """
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')
    return re_date

def getBeforeWeekDays(weeks=1):
    """
    获取前一周的所有日期(weeks=1)，获取前N周的所有日期(weeks=N)
    :param weeks:
    :return:
    """
    # 0,1,2,3,4,5,6,分别对应周一到周日
    week = datetime.datetime.now().weekday()
    days_list = []
    start = 7 * weeks + week
    end = week
    for index in range(start, end, -1):
        day = getdate(index)
        print(day)
        days_list.append(day)
    return days_list

def monitoring_run_time(f):
    """
    装饰器
    记录方法运行时间
    :param f:
    :return:
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = f(*args, **kwargs)
        end_time = time.time()
        print("%s执行成功，用时:%.2f" % (f.__name__, end_time - start_time))
        return res
    return wrapper

@retry(stop_max_attempt_number=10)
def get_taobao_time():
    """获取在线时间{"sysTime2":"2021-01-12 16:41:50","sysTime1":"20210112164150"}"""
    try:
        url = 'http://10.228.84.20:21000/get_local_timestamp'
        ts = requests.get(url)
        if ts.status_code == 200:
            json_data = json.loads(ts.text)
            return {"sysTime3": ts_toStr_det(json_data.get('time')),
                    "sysTime2": timestamp_toString(json_data.get('time')),
                    "sysTime1": f"{json_data.get('time')}"}
        else:
            json_data = {"sysTime3": ts_toStr_det(int(time.time())),
                         "sysTime2": datetime_toString(datetime.datetime.now()),
                         "sysTime1": f"{datetime_toTimestamp(datetime.datetime.now())}"}
            return json_data
    except:
        json_data = {"sysTime3": ts_toStr_det(int(time.time())),
                     "sysTime2": datetime_toString(datetime.datetime.now()),
                     "sysTime1": f"{datetime_toTimestamp(datetime.datetime.now())}"}
        return json_data

if __name__ == '__main__':
    # month_begin_day = month_datelist('2020-01')
    # print(getdate(1))
    print(get_taobao_time())
