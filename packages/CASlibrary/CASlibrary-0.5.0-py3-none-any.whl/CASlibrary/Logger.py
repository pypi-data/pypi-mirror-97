import os
import sys

import logbook
from logbook import StreamHandler


class Logger:
    def __init__(self, module):
        logbook.set_datetime_format("utc")
        loglevel = os.getenv('LOGGING_LEVEL', 'INFO')
        StreamHandler(sys.stdout, level=loglevel).push_application()
        self.logger = logbook.Logger(module)

    def getLogger(self):
        return self.logger
