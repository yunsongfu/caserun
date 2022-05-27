#!/usr/bin/env python3

import os
import random
import logging
import threading


class Level(object):
    """ 日志中需要打印的最低日志级别.
    """
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG


class Logger(object):
    """ 向控制台和指定文件路径输出日志.
    """
    level = Level.DEBUG
    vars = threading.local()
    vars.logger = None

    @classmethod
    def initial(cls, logfile: str = os.devnull) -> None:
        """ 初始化当前线程的日志打印对象.
        """
        logger = logging.Logger(name=str(random.randint(0, 1000000)))
        logger.setLevel(cls.level)

        formatter = logging.Formatter(
            "[%(asctime)s][%(thread)d][%(levelname)s] %(message)s")

        # 打印日志到控制台
        s_handler = logging.StreamHandler()
        s_handler.setFormatter(formatter)
        logger.addHandler(s_handler)

        # 打印日志到指定文件
        f_handler = logging.FileHandler(logfile)
        f_handler.setFormatter(formatter)
        logger.addHandler(f_handler)

        cls.vars.logger = logger

    @classmethod
    def critical(cls, message: str) -> None:
        """ 打印致命日志信息.
        """
        cls.vars.logger.critical(message)

    @classmethod
    def error(cls, message: str) -> None:
        """ 打印错误日志信息.
        """
        cls.vars.logger.error(message)

    @classmethod
    def info(cls, message: str) -> None:
        """ 打印普通日志信息.
        """
        cls.vars.logger.info(message)

    @classmethod
    def warning(cls, message: str) -> None:
        """ 打印告警日志信息.
        """
        cls.vars.logger.warning(message)

    @classmethod
    def debug(cls, message: str) -> None:
        """ 打印调试日志信息.
        """
        cls.vars.logger.debug(message)
