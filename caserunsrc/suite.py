#!/usr/bin/env python3

import sys
import typing
import importlib
import xml.dom.minidom

import caserunsrc.log
import caserunsrc.case


class Parser(object):
    """
    解析测试用例配置文件的类.

    配置文件仅支持按照规则编写的XML文件,
    XML文件格式详见样例目录.
    """

    def __init__(self, suite: str, wosrkspace: str) -> None:
        """
        :@param suite: 测试套的路径.
        :@param workspace: 测试用例的存放路径.
        """
        self.workspace = wosrkspace
        self.xmldom = xml.dom.minidom.parse(suite).documentElement

    def cases(self) -> typing.List[caserunsrc.case.BaseCase]:
        """ 从配置文件中提取测试用例信息.
        """
        sys.path.append(self.workspace)

        cases = list()
        # 解析配置文件
        xmldom_cases = self.xmldom.getElementsByTagName("case")
        for xmldom_case in xmldom_cases:

            s_class = xmldom_case.getElementsByTagName(
                "class")[0].firstChild.data
            s_module = xmldom_case.getElementsByTagName(
                "module")[0].firstChild.data

            module = importlib.import_module(s_module)
            cs = getattr(module, s_class)
            cases.append(cs)

        return cases

    def log(self) -> typing.Tuple[caserunsrc.log.Level, str]:
        """ 从配置文件中提取日志信息.
        """
        xmldom_log = self.xmldom.getElementsByTagName("log")[0]
        dest = xmldom_log.getElementsByTagName("dest")[0].firstChild.data
        level = xmldom_log.getElementsByTagName("level")[0].firstChild.data

        return int(level), dest
