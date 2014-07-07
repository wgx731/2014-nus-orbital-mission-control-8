import os
import signal
import subprocess

from selenium import webdriver


def before_all(context):
    # NOTE: you can change to whatever driver you want, I use Firefox as a demo
    context.browser = webdriver.Firefox()
    # start the app engine server
    # make sure dev_appserver.py is in your PATH
    context.app_engine_proc = subprocess.Popen(
        ['dev_appserver.py',
         '--clear_datastore=true',
         '--port=4567', "%s/../" % os.path.dirname(os.path.abspath(__file__))],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    line = context.app_engine_proc.stdout.readline()
    while 'Starting admin server' not in line:
        print line
        if line == '':
            break
        line = context.app_engine_proc.stdout.readline()


def after_all(context):
    context.browser.quit()
    os.kill(context.app_engine_proc.pid, signal.SIGINT)
