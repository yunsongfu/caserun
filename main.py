#!/usr/bin/python3

import os
import sys
import concurrent.futures

from caserunsrc.log import Logger
from caserunsrc.case import Result
from caserunsrc.suite import Parser


class CaseRunner(object):

    def __init__(self, suite: str, workspace: str, threads: int = 1) -> None:
        """
        :@param suite: 测试套文件的路径.
        :@param workspace: 测试用例的根目录.
        :@param threads: 执行测试用例的线程数.
        """
        self.suite = suite
        self.workspace = workspace
        self.threads = threads

    def main(self):
        """ 执行测试用例的主函数.
        """
        parse = Parser(self.suite, self.workspace)
        level, logdir = parse.log()
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        # 初始化主线程日志配置.
        Logger.level = level
        Logger.initial("{}/main.log".format(logdir))

        def initial(func, name: str) -> Result:
            """ 添加初始化子线程的日志配置步骤.
            """
            Logger.initial("{}/{}.log".format(logdir, name))
            return func()

        # 创建线程池,执行测试用例
        tp = concurrent.futures.ThreadPoolExecutor(self.threads)
        sys.path.append(self.workspace)
        futures = list()
        cases = parse.cases()
        for cs in cases:
            futures.append(tp.submit(initial, cs.runner, cs.__name__))

        # 检查执行结果并输出到日志中.
        for cs, future in zip(cases, concurrent.futures.as_completed(futures)):
            if future.result() == Result.SUCCESS:
                Logger.info("@@@ Case {} is complated: Success.".format(
                    cs.__name__))
            if future.result() == Result.FAILED:
                Logger.error("@@@ Case {} is complated: Failed.".format(
                    cs.__name__))
        tp.shutdown()


if __name__ == "__main__":
    import argparse

    parse = argparse.ArgumentParser(
        description="Executing 'caserun' test project.")
    parse.add_argument("--suite-path",
                       type=str,
                       required=True,
                       help="The path of xml test suite file.")
    parse.add_argument("--workspace",
                       type=str,
                       required=True,
                       help="The root path of test cases.")
    args = parse.parse_args()

    cr = CaseRunner(suite=args.suite_path, workspace=args.workspace)
    cr.main()
