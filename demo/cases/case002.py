#!/usr/bin/env python3

from caserunsrc.log import Logger
from caserunsrc.case import BaseCase
from caserunsrc.concurrence import ThreadPool


class DemoCase002(BaseCase):

    @classmethod
    def environ(cls) -> None:
        Logger.info("{}: environ".format(cls.__name__))

    @classmethod
    def prepare(cls) -> None:
        Logger.info("{}: prepare".format(cls.__name__))

    @classmethod
    def execute(cls) -> None:
        Logger.info("{}: execute".format(cls.__name__))

        def test(i):
            Logger.info("Test thread pool: {}".format(i))

        tp = ThreadPool(2)
        tp.map(test, (1, 2))
        tp.submit(test, 3)
        tp.submit(test, 4)
        tp.wait()
        tp.shutdown()

    @classmethod
    def cleanup(cls) -> None:
        Logger.info("{}: cleanup".format(cls.__name__))
