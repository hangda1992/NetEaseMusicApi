#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import logging
from DjangoMusic import settings
from logging.handlers import TimedRotatingFileHandler


def _get_log():
    # 创建错误日志对象
    try:
        logger = logging.getLogger()
        hdlr = TimedRotatingFileHandler(
            os.path.join('./log/', 'Music.log'),
            when='D',
            interval=1,
            backupCount=7,
        )
        formatter = logging.Formatter(
            "[%(asctime)s] [%(filename)s] [fun:%(funcName)s] [line:%(lineno)d] [%(levelname)s] %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.NOTSET)

    except IOError as e:
        if e.errno == 28:
            logger.setLevel(100)
    return logger


logger = _get_log()


def WriteLog(log, level='INFO', is_service_socket=0):
    # 写错误日志
    global logger
    if logger.level > logging.CRITICAL:
        pass
    try:
        level = level.upper()
        if settings.WRITEDEBUGLOG:
            if settings.CONFIG['PrintLog'] or is_service_socket:
                if level == 'INFO':
                    logger.info(log)
                elif level == 'DEBUG':
                    logger.debug(log)
                elif level == 'WARNING':
                    logger.warning(log)
            if level == 'ERROR':
                logger.error(log)
            elif level == 'CRITICAL':
                logger.critical(log)
    except IOError as e:
        if e.errno == 28:
            logger.setLevel(100)


class UserException(Exception):
    # 自定义异常
    def __init__(self, val):
        self.val = val
