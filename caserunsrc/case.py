#!/usr/bin/env python3

import abc
import traceback
import threading

from caserunsrc.log import Logger


class Result(object):
    """ 测试用例的执行结果集.
    """
    SUCCESS = 0
    FAILED = 1


class BaseCase(object):
    """
    所有测试用例的基类.

    执行顺序:
        environ -> prepare -> execute -> cleanup -> Result.SUCCESS
        encrion (raise) -> Result.FAILED
        encrion -> prepare (raise) -> Result.FAILED
        encrion -> prepare -> execute (raise) -> Result.FAILED
        encrion -> prepare -> execute -> cleanup (raise) -> Result.FAILED

    环境变量:
        设置变量: cls.vars.{name} = value
        获取变量: value = cls.vars.{name}

    用例中需要开启多线程时,请使用框架提供的线程池. 否则日志信息可能无法正确输出到日志文件.
    """
    vars = threading.local()

    @classmethod
    @abc.abstractmethod
    def environ(cls) -> None:
        """ 设置环境变量.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def prepare(cls) -> None:
        """ 准备测试环境.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def execute(cls) -> None:
        """ 执行测试用例.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def cleanup(cls) -> None:
        """ 清理测试环境.
        """
        pass

    @classmethod
    def runner(cls) -> Result:
        """ [禁止重写] 测试阶段运行测试用例的函数.
        """

        def exec(func) -> bool:
            try:
                func()
            except Exception as e:
                del e
                Logger.error(traceback.format_exc())
                return False
            return True

        Logger.info("@@@ Start to run case {}.".format(cls.__name__))

        for func in [cls.environ, cls.prepare, cls.execute]:
            Logger.info("@@@ Start to run {}: {}.".format(
                cls.__name__, func.__name__))
            if not exec(func):
                break
        else:
            Logger.info("@@@ Start to run {}: cleanup.".format(cls.__name__))
            if exec(cls.cleanup):
                return Result.SUCCESS
            return Result.FAILED

        Logger.info("@@@ Start to run {}: cleanup.".format(cls.__name__))
        exec(cls.cleanup)
        return Result.FAILED


if __name__ == "__main__":

    class TestCase(BaseCase):

        @classmethod
        def environ(cls):
            cls.vars.var1 = 1

        @classmethod
        def prepare(cls):
            Logger.info(cls.vars.var1)

        @classmethod
        def execute(cls):
            Logger.info(cls.vars.var2)

        @classmethod
        def cleanup(cls):
            Logger.info(cls.vars.var1)

    from log import Level
    Logger.initial(Level.DEBUG, "test.log")
    TestCase.runner()
