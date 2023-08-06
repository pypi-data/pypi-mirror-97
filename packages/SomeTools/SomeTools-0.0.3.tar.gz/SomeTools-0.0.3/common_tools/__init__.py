# 工具箱中的工具都是开箱即用的，不依赖特别的数据、配置和业务逻辑

from common_tools.string_tools.string_cleaning import GeneralString
from common_tools.log_tools.logger_main import GeneralLog
from common_tools.datetime_tools.date_conversion import GeneralDatetime
from common_tools.chinese_to_pinyin_acronym.chinese_to_pinyin import GeneralChineseToPinyin


class Common_tools(GeneralChineseToPinyin, GeneralDatetime, GeneralString, GeneralLog):
    def __init__(self, *args, **kwargs):
        super(Common_tools, self).__init__(*args, **kwargs)
        self.logger.debug('SomeTools: Common_tools initialized')
