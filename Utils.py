import logging
from datetime import datetime
import sys, os
import subprocess

LOG_PATH = './logs/'

def init_path(path):
    try:
        os.makedirs(path)
    except OSError as error:
        if error.errno != 17: #Other then FileNotExist
            raise error

def init_logger(logger_name,
                logger_level=logging.DEBUG,
                logger_formatter = logging.Formatter("%(asctime)-15s Process-%(process)d %(levelname)s %(name)s %(message)s")):

    init_path(LOG_PATH)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)

    file_handler = logging.FileHandler('%s%s.log' % (LOG_PATH, logger_name))
    console_handler = logging.StreamHandler()

    file_handler.setLevel(logger_level)
    console_handler.setLevel(logger_level)

    file_handler.setFormatter(logger_formatter)
    console_handler.setFormatter(logger_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def getDate(format='%Y%m%d'):
    return datetime.now().strftime(format)


def getTime(format='%H%M'):
    return datetime.now().strftime(format)


def getDateTime(format='%Y%m%d_%H%M'):
    return datetime.now().strftime(format)

def isLinux():
    if sys.platform.startswith('linux'):
        return True
    else:
        return False

def is_xmllint_installed():
    popen = subprocess.Popen(args = ['xmllint', '--version'], stderr=subprocess.PIPE)
    output, errors = popen.communicate()

    if 'xmllint: using libxml' in errors.decode():
        return True
    else:
        return False



def is_jq_installed():
    popen = subprocess.Popen(args = ['jq', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = popen.communicate()

    if 'jq' in str(output.decode()) and str(errors.decode()) == '':
        return True
    else:
        return False

def is_json_file(filename):
        if filename.endswith(('.json')):
            return True
        else:
            return False

def is_xml_file(filename):
    if filename.endswith(('.xml')):
        return True
    else:
        return False

class TimeElapsedCounter:

    def __init__(self):
        self.start_time = None
        self.stop_time = None
        self.is_started = False
        self.is_stoped = False
        self.elapsed_time = None

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __str__(self):
        return str(self.get_elapsed_time())

    def start(self):
        if not self.is_started:
            self.start_time = datetime.now()
            self.is_started = True

        return self

    def stop(self):
        if self.is_started:
            self.stop_time = datetime.now()
            self.is_started = False
            self.is_stoped = True

            self.elapsed_time = self.stop_time - self.start_time

        return self

    def get_elapsed_time(self):
        if not self.is_started and self.is_stoped:
            return self. elapsed_time

    @staticmethod
    def run_time_measure(function):
        def wrapper(*args, **kwargs):
            time_differ = TimeElapsedCounter().start()

            wrapper_content = function(*args, **kwargs)
            print(kwargs)
            kwargs['self'].logger.info('Time needed to calculation: %s' % time_differ.stop().get_elapsed_time())

            args[0].logger.info('Time needed to calculation: %s' % time_differ.stop().get_elapsed_time())
            return wrapper_content

        return wrapper

