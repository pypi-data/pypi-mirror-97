# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['AssertionEngine']

package_data = \
{'': ['*']}

install_requires = \
['robotframework>=3.2.2,<4.0.0']

setup_kwargs = {
    'name': 'robotframework-assertion-engine',
    'version': '0.0.2',
    'description': 'Generic way to create meaningful and easy to use assertions for the Robot Framework libraries.',
    'long_description': 'Assertion Engine\n================\n\nGeneric way to create meaningful and easy to use assertions for the `Robot Framework`_\nlibraries. This tools is spin off from `Browser library`_ project, where the Assertion\nEngine was developed as part of the of library.\n\n.. image:: https://github.com/MarketSquare/AssertionEngine/actions/workflows/on-push.yml/badge.svg\n   :target: https://github.com/MarketSquare/AssertionEngine\n.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg\n   :target: https://opensource.org/licenses/Apache-2.0\n\nSupported Assertions\n--------------------\n\nCurrently supported assertion operators are:\n\n+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+\n| Operator | Alternative Operators     | Description                                                                        | Validate Equivalent              |\n+==========+===========================+====================================================================================+==================================+\n| ==       | equal, should be          | Checks if returned value is equal to expected value.                               | value == expected                |\n+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+\n| !=       | inequal, should not be    | Checks if returned value is not equal to expected value.                           | value != expected                |\n+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+\n| >        | greater than              | Checks if returned value is greater than expected value.                           | value > expected                 |\n+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+\n| >=       |                           | Checks if returned value is greater than or equal to expected value.               | value >= expected                |\n+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+\n| <        | less than                 | Checks if returned value is less than expected value.                              | value < expected                 |\n+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+\n| <=       |                           | Checks if returned value is less than or equal to expected value.                  | value <= expected                |\n+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+\n| \\*=      | contains                  | Checks if returned value contains expected value as substring.                     | expected in value                |\n+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+\n|          | not contains              | Checks if returned value does not contain expected value as substring.             | expected not in value            |\n+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+\n| ^=       | should start with, starts | Checks if returned value starts with expected value.                               | re.search(f"^{expected}", value) |\n+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+\n| $=       | should end with, ends     | Checks if returned value ends with expected value.                                 | re.search(f"{expected}$", value) |\n+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+\n| matches  |                           | Checks if given RegEx matches minimum once in returned value.                      | re.search(expected, value)       |\n+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+\n| validate |                           | Checks if given Python expression evaluates to True.                               |                                  |\n+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+\n| evaluate |  then                     | When using this operator, the keyword does return the evaluated Python expression. |                                  |\n+----------+---------------------------+------------------------------------------------------------------------------------+----------------------------------+\n\nUsage\n-----\nWhen keywords needs to do an assertion\n\n\n.. _Robot Framework: http://robotframework.org\n.. _Browser library: https://robotframework-browser.org/',
    'author': 'Tatu Aalto',
    'author_email': 'aalto.tatu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MarketSquare/AssertionEngine',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
