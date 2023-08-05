"""Naive tester console application

A simple testing system based on files. You provide a name of a script
to be tested and a folder containing files with arguments and reference
outputs. The app runs the script with the arguments from a file and compares
its result with that from the corresponding reference output file.
The following naming convention is applied:
each set of arguments is stored in the '.in' file, while the corresponding
output in the '.out' file, i.e., 'test_0.in' and 'test_0.out'.
Each pair must have identical names except for extensions.

For more information visit https://github.com/FilippSolovev/naive-tester

"""

import logging
import sys

logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO, format='%(message)s')

# Version of naive_tester package
__version__ = '1.2.1'
