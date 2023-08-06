# -*- coding: utf-8 -*-
"""
Created on 18 September 2017
@author: Jeff Wang, Charlie Lewis
"""
import logging.handlers
import os
import socket

from poseidon_core.helpers.config import Config


class Logger:
    """
    Base logger class that handles logging. Outputs to both console, a poseidon
    specific log file and a user specified syslog. To log, create a logger:
    logger1 = logging.getLogger('mpapp.area1')
    """
    host = os.getenv('SYSLOG_HOST', 'NOT_CONFIGURED')
    port = int(os.getenv('SYSLOG_PORT', 514))

    level_int = {'CRITICAL': 50, 'ERROR': 40, 'WARNING': 30,
                 'INFO': 20, 'DEBUG': 10}

    config = Config().get_config()

    # setup existing loggers
    logging.getLogger('schedule').setLevel(logging.ERROR)

    use_file_logger = True
    # ensure log file exists
    try:
        if not os.path.exists('/var/log/poseidon'):
            os.makedirs('/var/log/poseidon')
        if not os.path.exists('/var/log/poseidon/poseidon.log'):
            with open('/var/log/poseidon/poseidon.log', 'w'):
                pass
        # set up logging to file
        level_str = config.get('logger_level', None)
        level = 0
        if isinstance(level_str, str):
            level = level_int.get(level_str.upper(), 0)
        logging.basicConfig(level=level,
                            format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
                            filename='/var/log/poseidon/poseidon.log',
                            filemode='a')
    except Exception as e:  # pragma: no cover
        use_file_logger = False

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    # don't try to connect to a syslog address if one was not supplied
    if host != 'NOT_CONFIGURED':  # pragma: no cover
        # if a syslog address was supplied, log to it
        syslog = logging.handlers.SysLogHandler(
            address=(host, port), socktype=socket.SOCK_STREAM)
        f_format = '%(asctime)s [%(levelname)s] %(name)s - %(message)s'
        f_formatter = logging.Formatter(f_format)
        syslog.setFormatter(f_formatter)
        logging.getLogger('').addHandler(syslog)
