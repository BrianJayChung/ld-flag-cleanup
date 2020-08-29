import logging
import sys
import os
import glob

from typing import Union
from subprocess import run
from datetime import date

# Configure Logging
LOG = logging.getLogger(sys.modules[__name__].__name__)
_CH = logging.StreamHandler(sys.stdout)
_FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s')
_CH.setFormatter(_FORMATTER)
LOG.addHandler(_CH)
DATE = str(date.today())

def check_local() -> None:
    """
    Verify required directories exist.

    This functions checks the current working directory to ensure that
    the required directories exist. If they do not exist, it will create them.
    """
    to_check = ['./replay/toDelete', './replay/archive']

    for i in to_check:
        if not os.path.exists(i):
            os.makedirs(i)

def create_file(flags: list) -> None:
    """
    Create file of flags to delete.
    """
    check_local()
    save_path = './replay/toDelete'
    complete_name = os.path.join(save_path, DATE)

    flags = str(flags).replace(', ', '\n').replace("'",'').replace('{','').replace('}','')
    with open(complete_name, 'w') as filename:
        filename.write(flags)

def read_file() -> Union[list, str]:
    files = glob.glob('./replay/toDelete/*')
    sorted_files = sorted(files, key=os.path.getctime)

    if sorted_files:  # list is not empty
        LOG.info('Found %s, beginning execution.', sorted_files)
        for command_file in sorted_files:
            with open(command_file, 'r') as file:
                list_of_flags = file.read().splitlines()
                return list_of_flags, file.name
    else:
        LOG.warning('No files found, nothing to delete.')

def move_file(file_name: str) -> None:
    LOG.info('moving %s to archive', file_name)
    move_file = 'mv {0} ./replay/archive/'.format(file_name)

    run(move_file, shell=True, check=True)

    LOG.info('LaunchDarkly Flags have been deleted file has been moved to archive')

