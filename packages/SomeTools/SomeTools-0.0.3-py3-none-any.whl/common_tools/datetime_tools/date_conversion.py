"""无脑处理时间（兼容各种类型和格式互转）"""

import re
import datetime
from datetime import timedelta

_datetime_fmt_list = ['%Y-%m-%d',
                      '%Y%m%d',
                      '%d-%b-%Y%H:%M',
                      '    (%m/%d %H:%M)',
                      '%m/%d',
                      '%m/%d/%Y %H:%M:%S',
                      '%d-%Y %H:%M',
                      '%d/%Y %H:%M',
                      '%Y/%m/%d',
                      "%Y-%m-%dT%H:%M:%S.%fZ",
                      '%d %b %Y',
                      '时间：%Y-%m-%d',
                      '时间：%Y-%m-%d %H:%M:%S',
                      '时间：%Y-%m-%d %H:%M',
                      '%d%b%Y',
                      '[%Y-%m-%d]',
                      '发布时间：%Y-%m-%d',
                      '发布日期：%Y-%m-%d',
                      '更新日期：%Y-%m-%d',
                      '更新时间：%Y-%m-%d',
                      '发布时间：%Y-%m-%d %H:%M:%S',
                      '更新时间：%Y-%m-%d %H:%M:%S',
                      '更新日期：%Y-%m-%d %H:%M:%S',
                      '%Y-%m-%d %H:%M:%S',
                      '%Y-%m-%dT%H:%M:%S+00:00',
                      '【%Y-%m-%d】',
                      '创建日期：%Y-%m-%d',
                      '公开时间：%Y-%m-%d',
                      '%Y年%m月',
                      '%Y年%m月%d日',
                      '发布时间：%Y-%m-%d %H:%M',
                      '%Y.%m.%d',
                      '%Y-%m',
                      '(%m月%d日 %H:%M)',
                      '%Y年%m月%d日%H：%M',
                      '%Y-%m-%d %H:%M',
                      '1',
                      '%d-%m-%Y',
                      ' %Y年%m月%d日  %H:%M',
                      '(%Y年%m月%d日 %H:%M)',
                      '%m-%d %H:%M',
                      '%Y/%m/%d %H:%M',
                      '%Y-%m-%d  %H:%M',
                      '%m-%d',
                      '%m/%d',
                      '%Y年%m月%d日资金市场日评',
                      '%m月%d日 %H:%M',
                      '%Y年%m月%d日 %H:%M',
                      '[%Y/%m/%d %H:%M]',
                      '%m/%d %H:%M',
                      '[%m月%d日 %H:%M]',
                      '[ %Y年%m月%d日 ]',
                      '%Y-%m-%d %H:%M 来源：',
                      '%Y年%m月%d日%H:%M | 来源：',
                      '[%m月%d日]',
                      'crtime=%Y-%m-%d;document.write(crtime);',
                      '%Y年%m月%d日  %A',
                      'None',
                      '[%Y/%m/%d%H:%M]',
                      '%d%Y-%m',
                      '%d%B%Y',
                      "crtime= '%Y-%m-%d';\r\n"
                      '  \t                \r\n'
                      '  \t                    document.write(crtime);',
                      '大公信用%Y年第%m期',
                      'Expired: %Y-%m-%d',
                      '%Y %m月 %d',
                      '%H:%M:%S',
                      '%d %b %Y',
                      '%B %d, %Y',
                      '%B %Y',
                      '%Y-%m-%d%H:%M:%S',
                      '今天 %M:%S',
                      '时间：%Y年%m月%d日 %H:%M:%S&nbsp中财网',
                      ]


class GeneralDatetime:
    def __init__(self, *args, **kwargs):
        self.clean_string = None
        super(GeneralDatetime, self).__init__(*args, **kwargs)


    @classmethod
    def str_to_obj(self, datetime_str: str, change_future_time: bool = False) -> datetime.datetime:
        """
        字符串转为datetime对象
        :param datetime_str: str
        :param change_future_time: bool
        :return: datetime.datetime
        """
        assert isinstance(datetime_str, str)
        if not self.clean_string:
            from common_tools.string_tools.string_cleaning import GeneralString
            self.clean_string = GeneralString().clean_string

        _now_date_time = datetime.datetime.now()
        datetime_str = self.clean_string(datetime_str)
        if datetime_str in ['昨天', '1天前']:
            return _now_date_time - timedelta(days=1)
        if datetime_str in ['前天', '2天前']:
            return _now_date_time - timedelta(days=2)
        if datetime_str in ['大前天', '3天前']:
            return _now_date_time - timedelta(days=3)

        if '小时前' in datetime_str:
            if datetime_str.endswith('小时前'):
                if ':' in datetime_str:
                    temp_str = datetime_str.replace('小时前', '')
                    temp_str = temp_str.split(':')[-1]
                else:
                    temp_str = datetime_str.replace('小时前', '')
                return _now_date_time - timedelta(hours=int(temp_str))
        if '分钟前' in datetime_str:
            if datetime_str.endswith('分钟前'):
                if ':' in datetime_str:
                    temp_str = datetime_str.replace('分钟前', '')
                    temp_str = temp_str.split(':')[-1]
                else:
                    temp_str = datetime_str.replace('分钟前', '')
                return _now_date_time - timedelta(minutes=int(temp_str))

        p_date = None
        for _temp_index, fmt in enumerate(_datetime_fmt_list):
            try:
                p_date = datetime.datetime.strptime(datetime_str, self.clean_string(fmt))
                break
            except Exception as e:
                if _temp_index == len(_datetime_fmt_list) - 1:
                    mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", datetime_str)
                    if mat:
                        datetime_str = mat.groups()[0]
                        p_date = datetime.datetime.strptime(datetime_str, '%Y-%m-%d')
                else:
                    pass
        if p_date:
            # 不带年的加上年
            if p_date.year == 1900:
                p_date = p_date.replace(year=_now_date_time.year)
            if change_future_time:
                # 未来判定,转为过去
                if p_date.year == _now_date_time.year:
                    if p_date.month > _now_date_time.month:
                        p_date = p_date.replace(year=_now_date_time.year - 1)
                    if p_date.month == _now_date_time.month:
                        if p_date.day > _now_date_time.day:
                            p_date = p_date.replace(year=_now_date_time.year - 1)
            return p_date

    @staticmethod
    def obj_to_str(datetime_obj: datetime.datetime) -> str:
        """
        datetime对象转为字符串
        :param datetime_obj: datetime.datetime
        :return: str
        """
        assert isinstance(datetime_obj, datetime.datetime)
        return datetime.datetime.strftime(datetime_obj, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def timestamp_int_to_obj(timestamp_int: int) -> datetime.datetime:
        """
        时间戳转为datetime对象
        :param timestamp_int: int
        :return: datetime.datetime
        """
        assert isinstance(timestamp_int, int)
        return datetime.datetime.fromtimestamp(timestamp_int)
