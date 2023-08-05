"""Handle files for tester."""
import sys
import os
import logging

logger = logging.getLogger(__name__)


def get_files(path, extension='.txt'):
    """Returns a list of files in the path directory based on provided extension.
    """
    reference_files = []
    for dirname, _, files in os.walk(path):
        for fname in files:
            if fname.endswith(extension):
                reference_files.append(os.path.join(dirname, fname))
    # logger.info(f'total {len(reference_files)} files')
    return sorted(reference_files)


def check_files_existence(file_name, err_msg='File does not exit'):
    """Checks if a file or directory exists."""
    if not os.path.exists(file_name):
        logger.error(err_msg)
        sys.exit()


def do_files_comply(actual_in_files, actual_out_files):
    """Check if the 'in' files correspond to the 'out' files by names."""
    expected = set(map(lambda x: x[:-3] + '.out', actual_in_files))
    return not expected.difference(set(actual_out_files))


def load_files(file_names):
    """Reads bunch of files and loads its content.

    Parameters
    ----------
    file_names : a list with names of the files to load content from.

    Returns
    -------
    A list where each element keeps the content of a file.

    """
    output_list = []
    for file_name in file_names:
        with open(file_name, 'r') as output_file:
            output = output_file.read().strip()
            output = output.split('\n')
            output_list.append(output)
    return output_list
