from loguru import logger as context_logger


# from conf import DIR


class GeneralLog:
    # __instance = None
    # def __new__(cls, *args, **kwargs):
    #     if not cls.__instance:
    #         cls.__instance = super(GeneralLog, cls).__new__(cls, *args, **kwargs)
    #     return cls.__instance

    def __init__(self, file_rec: bool = False, file_name: str = '', file_addr: str = '', *args, **kwargs):
        super(GeneralLog, self).__init__(*args, **kwargs)
        if file_rec:
            if file_name and file_addr:
                log_name = f'{file_addr}{file_name}.log'
                log_error_name = f'{file_addr}{file_name}_error.log'
            else:
                log_name = f'{file_name}.log'
                log_error_name = f'{file_name}_error.log'
            context_logger.add(log_name, format="{time} {level} {extra[cron_uuid]} {extra[pub_uuid]} {message}", rotation="23:00", retention="7 days", encoding='utf-8', enqueue=True)
            context_logger.add(log_error_name, format="{time} {level} {extra[cron_uuid]} {extra[pub_uuid]} {message}", rotation="23:00", retention="7 days", encoding='utf-8', enqueue=True, level='ERROR')
        self.context_logger = context_logger
        self.uuid1 = None
        self.uuid2 = None
        self.logger = self.get_logger()

    def get_logger(self, **kwargs):
        uuid1 = self.uuid1 if self.uuid1 else kwargs.get('uuid1')
        uuid2 = self.uuid2 if self.uuid2 else kwargs.get('uuid2')
        _logger = self.context_logger.bind(uuid1=uuid1, uuid2=uuid2)
        return _logger

# aa = GeneralLog()
# aa.logger.info('info')
# aa.logger.warning('warning')
# aa.logger.debug('debug')
# aa.logger.error('error')


# from loguru import logger
# import os
#
# logs_dir = f"{os.path.dirname(os.path.dirname(__file__))}/log"
# file_name = 'ApiTestLogs'
#
#
# class Loggings:
#     __instance = None
#     logger.add(f"{logs_dir}/{file_name}.log", rotation="500MB", encoding="utf-8", enqueue=True,
#                retention="10 days")
#
#     def __new__(cls, *args, **kwargs):
#         if not cls.__instance:
#             cls.__instance = super(Loggings, cls).__new__(cls, *args, **kwargs)
#
#         return cls.__instance
#     def __init__(self):
#         self.className = self.__class__.__name__
#
#     def info(self, msg):
#
#         return logger.info(msg)
#
#     def debug(self, msg):
#         return logger.debug(msg)
#
#     def warning(self, msg):
#         return logger.warning(msg)
#
#     def error(self, msg):
#         '''
#         打印错误信息
#         '''
#         return logger.error(msg)
#
#     def exception(self,msg):
#         '''
#         打印异常信息方法
#         '''
#         return logger.exception(msg)
