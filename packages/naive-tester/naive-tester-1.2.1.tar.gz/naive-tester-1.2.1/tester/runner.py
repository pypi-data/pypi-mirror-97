"""Run an external script and assess its output."""
import contextlib
import logging
import subprocess
import sys
import time

import tester.config


logger = logging.getLogger(__name__)


@contextlib.contextmanager
def timer():
    """Time the execution of a context block.

    Yields:
    ------
        None
    """
    start = time.time()
    yield
    end = time.time()
    logger.info(f'Elapsed time: {(end - start):.2f}s')


def run_job(job):
    """Run a script with it's arguments.

    Parameters
    ----------
    job : a tuple of script's name and its arguments.

    Returns
    --------
    Standard out of a script in a string form.

    """
    script, args = job
    output = subprocess.run(
        [sys.executable] + [script] + [arg for arg in args],
        stdout=subprocess.PIPE,
        universal_newlines=True).stdout.strip('\n')
    return output


def assert_job(job, reference_output):
    """Check if script's output coincides with the reference output."""
    script, args = job
    with timer():
        try:
            reference_output = reference_output[0]
            actual_output = run_job(job)
            assert actual_output == reference_output
            if tester.config.verbose_output_flg:
                logger.info(f'Successfully run the {script}. With argument(s) '
                            f'{args} got the output of {reference_output}.')
            else:
                logger.info(f'Successfully run the {script}.')
        except AssertionError:
            if tester.config.verbose_output_flg:
                logger.error(
                    f'Failed run of the {script} with {args}. '
                    f'The output should be {reference_output}, '
                    f'but got {actual_output}.')
            else:
                logger.error(f'Run of the {script} failed.')


def run_jobs(jobs_with_outputs):
    """Sequentially run scripts."""
    for job_with_output in jobs_with_outputs:
        assert_job(*job_with_output)
