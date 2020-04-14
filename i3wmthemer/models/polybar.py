import logging

from i3wmthemer.enumeration.attributes import PolybarAttr
from i3wmthemer.models.abstract_theme import AbstractTheme
from i3wmthemer.utils.fileutils import FileUtils

logger = logging.getLogger(__name__)


class PolybarTheme(AbstractTheme):
    """
    Class that contains the Polybar theme attributes.
    """

    def __init__(self, json_file):
        """
        Initializer.
        :param json_file: file that contains the polybar theme.
        """
        self.theme = json_file[PolybarAttr.NAME.value]
        self.defaults = {k:v for k, v in self.theme.items() if type(v) == str}
        self.modules = {k:v for k, v in self.theme.items() if type(v) != str}

    def load(self, configuration):
        """
        Function that loads the Polybar theme.

        :param configuration: the configuration.
        """
        logger.warning('Applying changes to Polybar configuration file')

        if FileUtils.locate_file(configuration.polybar_config):
            for k,v in self.defaults.items():
                FileUtils.replace_line(configuration.polybar_config, f"{k} =", f"{k} = {v}")

            for module in self.modules:
                # TODO Replace only for relevant module
                for k,v in module.items():
                    FileUtils.replace_in_section()
                    FileUtils.replace_line(configuration.polybar_config, f"{k} =", f"{k} = {v}")
        else:
            logger.error('Failed to locate the Polybar configuration file')
