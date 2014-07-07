import os
import sys
import signal
import subprocess

from selenium import webdriver


def before_all(context):
    # NOTE: you can change to whatever driver you want, I use Firefox as a demo
    context.browser = webdriver.Firefox()
    # start the app engine server
    # make sure dev_appserver.py is in your PATH
    if os.environ['SERVER_RUNNING'] != "True":
        context.app_engine_proc = subprocess.Popen([
            'dev_appserver.py',
            '--clear_datastore=true',
            '--port=4567', "%s/../" %
            os.path.dirname(os.path.abspath(__file__))],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        line = context.app_engine_proc.stdout.readline()
        count = 75
        while ('Starting admin server' not in line) and (count > 0):
            sys.stdout.write(line)
            sys.stdout.write("count: %d\n" % count)
            sys.stdout.flush()
            line = context.app_engine_proc.stdout.readline()
            count = count - 1


def after_all(context):
    context.browser.quit()
    if os.environ['SERVER_RUNNING'] != "True":
        os.kill(context.app_engine_proc.pid, signal.SIGINT)
