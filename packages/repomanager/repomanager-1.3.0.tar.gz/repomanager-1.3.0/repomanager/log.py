# See LICENSE for details

import logging

logger = logging.getLogger(__name__)

class ColoredFormatter(logging.Formatter):
    """                                                                         
        Class to create a log output which is colored based on level.           
    """

    def __init__(self, *args, **kwargs):
        super(ColoredFormatter, self).__init__(*args, **kwargs)
        self.colors = {
            'DEBUG': '\033[94m',
            'INFO': '\033[92m',
            'WARNING': '\033[93m',
            'ERROR': '\033[91m',
        }

        self.reset = '\033[0m'

    def format(self, record):
        msg = str(record.msg)
        level_name = str(record.levelname)
        name = str(record.name)
        color_prefix = self.colors[level_name]
        return '{0}{1:<9s} : {2}{3}'.format(color_prefix,
                                            '[' + level_name + ']', msg,
                                            self.reset)


def setup_logging(log_level):
    """Setup logging                                                            
                                                                                
        Verbosity decided on user input                                         
                                                                                                                                                   
        :param log_level: User defined log level                             
                                                                                
        :type log_level: str                                                               
    """
    numeric_level = getattr(logging, log_level.upper(), None)

    if not isinstance(numeric_level, int):
        print(
            "\033[91mInvalid log level passed. Please select from debug | info | warning | error\033[0m"
        )
        raise ValueError("{}-Invalid log level.".format(log_level))

    logging.basicConfig(level=numeric_level)

