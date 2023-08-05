"""Naive Tester

Usage:
-----

    $ tester [script] [test_case_folder]

script - a script to test
test_case_folder - a folder containing pairs of .in and .out files,
where
    .in holds [script] arguments
    .out holds expected output

Contact:
-------

More information is available at:
- https://github.com/FilippSolovev/naive-tester

Version:
-------

- naive-tester v1.2.1
"""
import sys
import logging

import tester.config
from tester.io import check_files_existence, get_files
from tester.io import do_files_comply, load_files
from tester.runner import run_jobs

logger = logging.getLogger(__name__)


def main():

    args = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
    opts = [opt for opt in sys.argv[1:] if opt.startswith('-')]

    if len(args) > 1:
        script_name = args[0]
        dir_name = args[1]
    else:
        sys.exit()

    if '-v' in opts:
        tester.config.verbose_output_flg = True

    check_files_existence(script_name, 'Script given does not exist')
    check_files_existence(dir_name, 'Directory given does not exist')

    argument_files = get_files(dir_name, '.in')
    output_files = get_files(dir_name, '.out')
    if not do_files_comply(argument_files, output_files):
        logger.error('Input and output files do not comply')
        sys.exit()

    jobs_arguments = load_files(argument_files)
    reference_outputs = load_files(output_files)

    jobs = zip([script_name for _ in jobs_arguments],
               jobs_arguments)

    jobs_with_outputs = zip(jobs, reference_outputs)

    run_jobs(jobs_with_outputs)


if __name__ == '__main__':
    main()
