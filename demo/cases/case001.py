#!/usr/bin/env python3

from src.demo import test_log
from caserunsrc.log import Logger
from caserunsrc.case import BaseCase


class DemoCase001(BaseCase):
    @classmethod
    def environ(cls) -> None:
        Logger.info("{}: environ".format(cls.__name__))
        test_log()

    @classmethod
    def prepare(cls) -> None:
        Logger.info("{}: prepare".format(cls.__name__))

    @classmethod
    def execute(cls) -> None:
        Logger.info("{}: execute".format(cls.__name__))

    @classmethod
    def cleanup(cls) -> None:
        Logger.info("{}: cleanup".format(cls.__name__))
