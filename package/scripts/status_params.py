#!/usr/bin/env python
from resource_management import *

config = Script.get_config()

locator_piddir = config['configurations']['gemfire-env']['locator_piddir']
locator_pidfile = format("{locator_piddir}/vf.gf.locator.pid")

server_piddir = config['configurations']['gemfire-env']['server_piddir']
server_pidfile = format("{server_piddir}/vf.gf.server.pid")