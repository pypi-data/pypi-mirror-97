import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, Formatter, getLogger, StreamHandler
__version__ = '0.1.8'
version = __version__


default_log_name = 'xltoy'
default_log_level = ERROR
default_log_format = Formatter('%(levelname).3s %(message)s')
log = getLogger(default_log_name)
log.setLevel(default_log_level)
str_log = logging.StreamHandler()
str_log.setFormatter(default_log_format)
log.addHandler(str_log)


