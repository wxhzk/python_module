#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logger

def main():
    logger.initlogger()
    for _ in xrange(10000):
        logger.debug("test logger debug")
        logger.info("test logger info")
        logger.warning("test logger warning")
        logger.error("test logger error")

if __name__=='__main__':
    main()



