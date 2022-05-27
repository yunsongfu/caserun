# caserun
Automated testing framework for black box.

## 1. Directory Structure
    |- caserun
        |- caserunsrc
            |- `__init__.py
            |- `case.py
            |- `concurrence.py
            |- `log.py
            |- `suite.py
        |- `main.py
    |- workspace
        |- `suite.xml
        |- cases
            |- `__init__.py
            |- `case001.py
            |- `case002.py
        |- src
            |- `__init__.py
            |- `demo.py

## 2. Create Suite File
```
<?xml version="1.0"?>

<project>
    <log>
        <level>10</level> <!-- 10: DEBUG, 20: INFO, 30: WARNING, 40: ERROR -->
        <dest>./log</dest>
    </log>

    <cases>
        <case id="DEMO.CASE.001">
            <class>DemoCase001</class>
            <module>cases.case001</module>
        </case>
        <case id="DEMO.CASE.002">
            <class>DemoCase002</class>
            <module>cases.case002</module>
        </case>
    </cases>
</project>
```

## 3. Test Cases
```
#!/usr/bin/env python3

from caserunsrc.log import Logger
from caserunsrc.case import BaseCase


class DemoCase001(BaseCase):
    @classmethod
    def environ(cls) -> None:
        """ Set global variables.
        """
        cls.vars.a = 1
        cls.vars.b = 2

    @classmethod
    def prepare(cls) -> None:
        """ Prepare for test case.
        """
        Logger.info("Setup completed.")

    @classmethod
    def execute(cls) -> None:
        Loggger.info("a: {0}".format(cls.vars.a))
        Loggger.info("b: {0}".format(cls.vars.b))

    @classmethod
    def cleanup(cls) -> None:
        Logger.info("Cleanup completed.")
```

## 4. Run Project
```
export PATH=${PATH}:${caserun}

python3 main.py --workspace=${workspace} --suite-path=${workspace}/suite.xml
```

## 5. Description
- Multithread use "concurrence.ThreadPool", otherwise the log will not be output to the log file.
- Module in suite file is base on workspace.
- Class in suite file is the class name of test case.