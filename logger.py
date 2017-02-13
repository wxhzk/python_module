#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import os
import time
import logging as _logging
from logging.handlers import BaseRotatingHandler

def getNowDate():
    lt = time.localtime()
    return lt.tm_year*10000+lt.tm_mon*100+lt.tm_mday

class TimedRotatingFileHandler(BaseRotatingHandler):
    ''''''
    def __init__(self, filename, mode='a', maxBytes=1024*1024*50, encoding=None, delay=0):
        self.curCount = 0
        self.created = getNowDate()
        BaseRotatingHandler.__init__(self, filename, mode, encoding, delay)
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        if self.stream is None:
            self.stream = self._open()
        if self.created != getNowDate():
            return 1
        if self.maxBytes > 0:
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        return 0

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        dfn = "{0}.{1}".format(self.baseFilename, self.curCount)
        if os.path.exists(self.baseFilename):
            if os.path.exists(dfn):
                os.remove(dfn)
            os.rename(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()

    def _open(self):
        curdate = getNowDate()
        if curdate != self.created:
            self.curCount = 0
            self.created = curdate
        self.curCount += 1
        return BaseRotatingHandler._open(self)

class Logger(_logging.Logger):
    ''''''
    def findCaller(self):
        f = _logging.currentframe()
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if os.path.basename(__file__) in filename or filename == _logging._srcfile :
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name)
            break
        return rv

root = Logger(_logging.DEBUG)

def error(msg, *args, **kwargs):
    root.error(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    root.info(msg, *args, **kwargs)

def debug(msg, *args, **kwargs):
    root.debug(msg, *args, **kwargs)

def exception(msg, *args, **kwargs):
    root.exception(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    root.critical(msg, *args, **kwargs)
fatal = critical

def warning(msg, *args, **kwargs):
    root.warning(msg, *args, **kwargs)
warn = warning

def log(msg, *args, **kwargs):
    root.log(msg, *args, **kwargs)

_logging.BASIC_FORMAT = "[%(asctime)s-%(levelname)1.1s] %(filename)s-%(lineno)d:%(message)s"

def initlogger(filename=""):
    fmt = _logging.Formatter(_logging.BASIC_FORMAT)
    if filename != "":
        hdlr = TimedRotatingFileHandler(filename)
    else:
        hdlr = _logging.StreamHandler()
    hdlr.setFormatter(fmt)
    hdlr.setLevel(_logging.DEBUG)
    root.addHandler(hdlr)

def test():
    initlogger()
    debug("test logging debug")
    info("test logging info")
    warning("test logging warning")
    error("test logging error")

if __name__=='__main__':
    test()
