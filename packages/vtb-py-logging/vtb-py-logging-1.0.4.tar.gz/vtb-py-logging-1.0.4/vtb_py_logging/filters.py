import logging
import os


class SyslogFilter(logging.Filter):
    hostname = os.getenv('HOSTNAME')

    def filter(self, record):
        record.hostname = SyslogFilter.hostname
        return True
