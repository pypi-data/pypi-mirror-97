#!/usr/bin/env python3

import logging as logging
from logging import handlers
import os


class Logger(logging.Logger):

    def __init__(self, name, logdir, envtype=None):
        super().__init__(name=name, level=logging.DEBUG)

        # create console handler and set level to info
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # create file handler and set level to debug
        logfile = os.path.join(logdir, name + '.log')
        fh = handlers.TimedRotatingFileHandler(filename=logfile, when='D', interval=1, backupCount=6)
        fh.setLevel(logging.DEBUG)
        # create smtp handler and set level to error
        sh = handlers.SMTPHandler(mailhost='smtp.inria.fr', fromaddr='logger@gtlville.inrialpes.fr',
                                  toaddrs=['dance.eng@inria.fr'], subject='GTLVille alert')
        sh.setLevel(logging.ERROR)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to handlers
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)

        # add handlers to logger
        self.addHandler(ch)
        self.addHandler(fh)
        if envtype != 'local':
            self.addHandler(sh)
