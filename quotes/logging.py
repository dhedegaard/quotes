from __future__ import absolute_import
import os
from logging.handlers import TimedRotatingFileHandler


class AllWriteTimedRotatingFileHandler(TimedRotatingFileHandler):

    def _open(self):
        prev_umask = os.umask(0o000)
        try:
            result = super(AllWriteTimedRotatingFileHandler, self)._open()
        finally:
            os.umask(prev_umask)
        return result
