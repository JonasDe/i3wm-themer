import json
import yaml
import logging
import os.path
from abc import ABC, abstractmethod
from os import fdopen, remove
from shutil import move
from tempfile import mkstemp

logger = logging.getLogger(__name__)


class FileUtils:
    """
    File utilities method.
    """

    @staticmethod
    def locate_folder(path):
        """
        Check if the given path is a directory.

        :param path: path to check.
        :return:  True if the path is an existing directory.
        """
        return os.path.isdir(path)

    @staticmethod
    def locate_file(path):
        """
        Check if the given path is file.

        :param path: path to check.
        :return: true if the path is an existing file.
        """
        return os.path.isfile(path)

    @staticmethod
    def load_theme_from_file(path):
        """
        JSon file loader.

        Loads the theme from the given JSON file and returns it.

        :param path: json filepath.
        :return: the loaded theme.
        """
        file = ''
        if FileUtils.locate_file(path):
            logger.warning('Located the theme file.')
            with open(path) as theme_data:
                if file.endswith("json"):
                    file = json.load(theme_data)
                else:
                    file = yaml.safe_load(theme_data)
        else:
            logger.error('Failed to locate the theme file.')
            exit(9)

        return file

    @staticmethod
    def replace_line(file, pattern, new_line):
        """
        Function that replaces the given line in the given file.

        :param file: file to modify.
        :param pattern: pattern to filter.
        :param new_line: line to replace with.
        """
        fh, abs_path = mkstemp()
        with fdopen(fh, 'w') as new_file:
            with open(file) as old_file:
                for line in old_file:
                    if line.startswith(pattern):
                        pl1 = line
                        pl1 = pl1.rstrip()
                        pl2 = new_line
                        pl2 = pl2.rstrip()
                        logger.warning('Replacing line: \'%s\' with \'%s\'', pl1, pl2)
                        try:
                            new_file.write(new_line + '\n')
                        except IOError:
                            logger.error('FailedThis should allow for a user to!')
                    else:
                        try:
                            new_file.write(line)
                        except IOError:
                            logger.error('Failed!')
        remove(file)
        move(abs_path, file)

    @staticmethod
    def replace_in_section(file, start_pattern, end_pattern, linemap):
        """

        :return:
        """
        fh, abs_path = mkstemp()
        with fdopen(fh, 'w') as new_file:
            with open(file) as old_file:
                lines = old_file.readline()
                line = lines[0]
                counter = 0
                while not line.startswith(start_pattern) and counter < len(lines):
                    counter += 1
                    new_file.write(line)
                    line = line[counter]
                # section found
                while not line.startswith(end_pattern) and counter < len(lines):
                    counter += 1
                    for pattern, l in linemap.items():  # if line in linemap:
                        if line.startswith(pattern):
                            # replace
                            pl1 = line
                            pl1 = pl1.rstrip()
                            pl2 = linemap(pl1)
                            line = pl2 + '\n'
                            pl2 = pl2.rstrip()
                            logger.warning('Replacing line: \'%s\' with \'%s\'', pl1, pl2)
                    new_file.write(line)
                    counter += 1
                    line = line[counter]

                while counter < len(lines):
                    new_file.write(line)
                    counter += 1
                    line = line[counter]

        remove(file)
        move(abs_path, file)

class _FileOperation(ABC):

    @abstractmethod
    def execute(self):
        pass

class _ReplaceLine(_FileOperation):

    def __init__(self, file, pattern, line):
        self.file = file
        self.pattern = pattern
        self.line = line


class _ReplaceSection(_FileOperation):

    def __init__(self, file, start_pattern, end_pattern, linemap):
        self.file = file
        self.start_pattern = start_pattern
        self.end_pattern = end_pattern
        self.linemap = linemap


class FileParser:
    def __init__(self):
        self.operations = []

    def replace_line(self, file, pattern, new_line):
        self.operations.append(_ReplaceLine(file, pattern, new_line))

    def replace_section(self, file, start_pattern, end_pattern, linemap):
        self.operations.append(_ReplaceSection(file, start_pattern, end_pattern, linemap))

    def execute(self):
        for line in lines:
            for operation in self.operations:
                



        for operation in self.operations:
            operation.execute()
