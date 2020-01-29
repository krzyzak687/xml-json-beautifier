from Utils import init_path, init_logger
from Utils import is_xmllint_installed, is_jq_installed, isLinux
from Utils import is_json_file, is_xml_file
import os
import subprocess
import argparse

LOG_LEVEL = 'DEBUG'
LOG_LEVEL = 'INFO'

class XJBeauty():
    _log = init_logger('XJBeauty', LOG_LEVEL)

    def __init__(self, mode, input_path='./input/', output_path='./output/'):
        self._input_path = input_path
        self._output_path = output_path
        self._mode = mode

        init_path(self._output_path)
        init_path(self._input_path)

    def test(self):
        if isLinux() and is_jq_installed() and is_xmllint_installed():
            self._log.info('jq and xmllint are installed on linux.')
            return True
        else:
            self._log.error('this is not the linux or jq or xmllint are not installed.')
            return False

    def run(self):
        if self.test():
            for file in os.listdir(self._input_path):
                self._log.info('Current processing file: %s' % file)
                if is_json_file(file):
                    self._beauty_JSON(file)
                elif is_xml_file(file):
                    self._beauty_XML(file)
                else:
                    self._log.warn('File %s is not xml or json.' % file)

    def _beauty_XML(self, filename):
        self._log.debug('XML beauti %s' % filename)

        output_file = '%s%s' % (self._output_path, filename)
        input_file = '%s%s' % (self._input_path, filename)

        popen = subprocess.Popen(args=['xmllint', '--format', '--output', output_file, input_file],
                                 stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE)

        output, error = popen.communicate()

        self._log.debug('output: %s' % output)
        self._log.debug('error: %s' % error)
        self._log.debug('returncode: %s' % popen.returncode)

        #TODO: validation of success

    def _beauty_JSON(self, filename):
        self._log.debug('JSON beauti %s' % filename)

        input_file = '%s%s' % (self._input_path, filename)
        output_file = '%s%s' % (self._output_path, filename)

        popen = subprocess.Popen(args=['jq', '''''', input_file],
                                 stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE)

        output, error = popen.communicate()

        output = output.decode()
        error = error.decode()

        self._log.debug('output: %s' % output)
        self._log.debug('error: %s' % error)
        self._log.debug('returncode: %s' % popen.returncode)

        if error == '' and output != '':
            with open(output_file, 'w') as file:
                file.write(output)
        else:
            self._log.error('There is nothing to save and error occures: %s' % error)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This tool can be used to simple and fast parse xml and json files.'
                                                 'Only on linux. jq and xmllind are required.')
    parser.add_argument('--mode', choices=['xml', 'json', 'both', 'xmljson', 'jsonxml'], default='both')
    parser.add_argument('--input_folder' ,default='./input/')
    parser.add_argument('--output_folder', default='./output/')
    parser.add_argument('--log_level',choices=['DEBUG', 'INFO'], default='INFO')
    arguments = parser.parse_args()

    LOG_LEVEL = arguments.log_level

    xj_beauty = XJBeauty(arguments.mode, input_path=arguments.input_folder, output_path=arguments.output_folder)
    xj_beauty.run()


