#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function
from builtins import input
from future import standard_library
standard_library.install_aliases()

import os
import sys
import signal
import re
import fnmatch
import argparse
import logging
import random
import string
import urllib3
import posixpath
from  configparser import ConfigParser
import time


DEFAULT_CONFIG='~/bisque/config' if os.name == 'nt' else "~/.bisque/config"

def bisque_argument_parser(*args, **kw):
    parser = argparse.ArgumentParser(*args, **kw)
    parser.add_argument('-c', '--config', help='bisque config', default=DEFAULT_CONFIG)
    parser.add_argument('--profile', help="Profile to use in bisque config", default='default')
    parser.add_argument('-n', '--dry-run', action="store_true", help='report actions w/o changes', default=False)
    parser.add_argument('-d', '--debug',  nargs='?', help='set debug level: debug,info,warn,error' )
    parser.add_argument('--debug-file', help='output filename for debug messages', default=None )
    parser.add_argument('-q', '--quiet', action="store_true", help='print actions ', default=False)
    parser.add_argument('-a', '--credentials', help= "A bisque login.. admin ", default=None)
    parser.add_argument('--bisque-host', help = "Default bisque server to connect to ")
    parser.add_argument('--alias', help = "Use admin credentials to login as alias  ")
    # Local arguments
    return parser

def bisque_session(parser=None, args=None, root_logger = None):
    """Get a bisque session for command line tools using arguments and ~/.bisque/config files

    Usage:
    parser = bisque_argument_parser ("MyCommand")
    parser.add_argument ('newarg', help='any specific argument')
    args = parser.parse_args()
    session = bisque_session(args)

    ~/.bisque/config:
    [default]
    host=
    user=
    password=

    [testing]
    host=
    user=
    password=
    """
    user =  password =  root =  config = alias_user = None
    if parser is None:
        parser = bisque_argument_parser()
    pargs = parser.parse_args (args = args)
    config = ConfigParser ()
    if os.path.exists (os.path.expanduser(pargs.config)):
        config.read (os.path.expanduser(pargs.config))
        try:
            profile = config[pargs.profile]
            root = profile.get('host')
            user = profile.get('user')
            password = profile.get('password')
            alias_user = profile.get('alias', None)
        except KeyError:
            print ("No or incomplete profile named {}".format(pargs.profile))

    if pargs.bisque_host:
        root = pargs.bisque_host
    if pargs.credentials:
        user,password = pargs.credentials.split(':')
    if not (root and user and password):
        print ("Please configure how to connect to bisque with profile {}".format (pargs.profile))
        root = input("BisQue URL [{}] ".format (root)) or root
        user = input("username[{}] ".format (user)) or user
        password = input("password[{}]: ".format(password)) or password
        config_file = os.path.expanduser (pargs.config)
        if not os.path.isdir (os.path.dirname(config_file)):
            os.makedirs(os.path.dirname(config_file))
        with open(config_file, 'w') as conf:
            config[pargs.profile]  = { 'host': posixpath.join(root.strip(), ''), 'user': user.strip(), 'password':password.strip()}
            config.write(conf)
            print ("configuration has been saved to", pargs.config)

    if pargs.debug:
        logging.captureWarnings(True)
        if root_logger is None:
            if pargs.debug_file is not None:
                logging.basicConfig (filename = pargs.debug_file, filemode="w")
            else:
                logging.basicConfig(level=logging.DEBUG)
            root_logger = logging.getLogger()
        root_logger.setLevel ({'debug':logging.DEBUG, 'info':logging.INFO,'warn':logging.WARN,'error':logging.ERROR}.get (pargs.debug.lower(), logging.DEBUG))


    if root and user and password:
        import urllib3
        from .comm import BQSession
        session =   BQSession()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        session.c.verify = False
        session = session.init_local(bisque_root=root,  user = user, pwd=password, create_mex=False, as_user=alias_user)
        if session is None:
            print ("Could not create bisque session with root={} user={} pass={}".format(root, user, password))
        elif not pargs.quiet:
            print  ("Session for  ", root, " for user ", user, " created")
    return session, pargs
