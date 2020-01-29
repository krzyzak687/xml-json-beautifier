from Utils import init_path, init_logger
from Utils import is_xmllint_installed, is_jq_installed, isLinux
from Utils import is_json_file, is_xml_file
import os
import subprocess

XML = 1
JSON = 2
XMLJSON = 3
JSONXML = 3
BOTH = 3

class XJBeauty():
    _log = init_logger('XJBeauty')

    def __init__(self, mode, input_path='./input/', output_path='./output/'):
        self._input_path = input_path
        self._output_path = output_path
        self._mode = mode

        init_path(self._output_path)
        init_path(self._input_path)
        pass

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

        command = 'xmllint --format --output %s%s %s%s' %(self._output_path, filename, self._input_path, filename)
        self._log.debug(command)
        os.system(command)


    def _beauty_JSON(self, filename):
        self._log.debug('JSON beauti %s' % filename)

        command = 'jq \'\' %s%s > %s%s' % (self._input_path, filename, self._output_path, filename)
        self._log.debug(command)
        os.system(command)


if __name__ == '__main__':
    xj_beauty = XJBeauty('both')
    xj_beauty.run()


