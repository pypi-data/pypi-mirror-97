import os
import shutil
import logging

# Define logging
# Create logger definition
logger = logging.getLogger('cqe_util.log')
logger.setLevel(logging.DEBUG)

# Create file handler which logs messages in log file
fh = logging.FileHandler('cqe_util.log')
fh.setLevel(logging.DEBUG)

# Create console handler with high level log messages in console
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)
# logger.addHandler(fh)


def delete_and_create_dir(dir_path: str):
    """
    This method is used to delete existing directory and create new directory based on dir_path
    :param dir_path: r'C://Desktop//Comparison//data//actual//'
    :return:
    """
    logger.info('****************************************************************************************************')
    logger.info('FileUtil - Delete and Create Directory')
    logger.info('****************************************************************************************************')
    logger.info('Step-01 : Verify if the directory already exist if Yes, delete and create the directory')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    else:
        shutil.rmtree(dir_path)
        os.mkdir(dir_path)
    logger.info('****************************************************************************************************')

