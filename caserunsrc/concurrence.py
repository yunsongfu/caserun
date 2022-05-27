#!/usr/bin/env python3

import collections.abc
import concurrent.futures

import caserunsrc.log


class ThreadPool(object):
    """
    为测试项目AW和测试用例准备的线程池工具.
    使用该线程池类可以将子线程中的日志输出到控制台和日志文件中.
    """

    def __init__(self, capacity: int) -> None:
        """
        :@param capacity: 线程池容量.
        """
        self.futures = list()
        self.logger = caserunsrc.log.Logger.vars.logger
        self.threads = concurrent.futures.ThreadPoolExecutor(capacity)

    def submit(self, func, *args, **kwargs) -> None:
        """ 向线程池中添加非阻塞式任务.
        """

        def initial():
            """ 初始化线程的日志配置.
            """
            caserunsrc.log.Logger.vars.logger = self.logger
            return func(*args, **kwargs)

        self.futures.append(self.threads.submit(initial))

    def wait(self) -> None:
        """ 等待非阻塞式进程执行完成.
        """
        for future in concurrent.futures.as_completed(self.futures):
            pass

    def map(self, func, iterator: collections.abc.Iterable) -> list:
        """ 在线程池中执行组设施任务组.
        """
        # 重新组织参数迭代器
        n_iterator = list()
        for it in iterator:
            if not isinstance(it, collections.abc.Iterable):
                n_iterator.append((func, it))
                continue
            it = list(it)
            it.insert(0, func)
            n_iterator.append(tuple(it))
        n_iterator = tuple(n_iterator)

        def initial(args):
            """ 初始化线程的日志配置.
            """
            caserunsrc.log.Logger.vars.logger = self.logger
            return args[0](*args[1:])

        # 阻塞执行任务组
        results = list()
        for result in self.threads.map(initial, n_iterator):
            results.append(result)
        return results

    def shutdown(self) -> None:
        """ 关闭线程池.
        """
        self.threads.shutdown()
