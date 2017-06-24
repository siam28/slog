#!/usr/bin/python
# coding=utf8

import os
import logging
import subprocess as sp

from inspect import currentframe, getframeinfo
from time import strftime, sleep
from termcolor import colored

def ct():
    return strftime('%Y-%m-%d %H:%M:%S')

def get_file_and_lineno():
    ctx = currentframe().f_back.f_back.f_back
    fn = ctx.f_code.co_filename.split('/')[-1]
    lineno = ctx.f_lineno
    return ' (\033[1m{0}:{1}\033[0m) '.format(fn, lineno)

def noop_inspect():
    return ' '

def default_paint(s, color):
    return colored(s, color)

def noop_paint(s, color):
    return s

class Slog(object):
    def __init__(self, logfile=None, loglvl=3, inspect=False, bufsize=4096, splotch=u'⬢'):
        # the log file
        if logfile is not None:
            self.logfile = open(logfile, 'w+', bufsize)
        else:
            self.logfile = None

        # acceptable string log levels
        loglvls = ['silent', 'crit', 'fail', 'warn', 'info', 'all']

        if loglvl in [0, 1, 2, 3, 4, 5]:
            self.loglvl = loglvl
        elif loglvl in loglvls:
            try:
                self.loglvl = loglvls.index(loglvl)
            except ValueError:
                raise SlogLevelError('"{0}":str is not a valid Slog log level.'.format(loglvl))
        else:
            raise SlogLevelError('"{0}":{1} is not a valid Slog log level.'.format(loglvl, type(loglvl)))

        # whether or not calls to `inspect` functions will be made
        if inspect:
            self.inspect_func = get_file_and_lineno
        else:
            self.inspect_func = noop_inspect

        # detect color support or lack thereof
        if int(sp.check_output(['tput', 'colors'])) >= 8:
            self.paint = default_paint
        else:
            self.paint = noop_paint

        # custom splotch
        self.splotch = splotch

    def __del__(self):
        if self.logfile:
            self.logfile.close()

    def slog_fmt(self, level, message, color, fnln=None):
        if fnln is None:
            fnln = self.inspect_func
        if level != 'ok':
            return [
                    '\r' + ct() + ' || [ ' + level.upper() + ' ] ' + self.paint(self.splotch, color) + fnln() + message,
                    '\r' + ct() + ' || [ ' + level.upper() + ' ] ' + fnln() + message]
        else:
            return [
                    '\r' + ct() + ' || [  '+ level.upper() +'  ] ' + self.paint(self.splotch, color) + fnln() + message,
                    '\r' + ct() + ' || [  '+ level.upper() +'  ] ' + fnln() + message]

    def slog_print(self, message, level, writem):
        if level <= self.loglvl:
            if 't' in writem:
                print(message[0])
            if self.logfile and 'f' in writem:
                self.logfile.write(message[1] + '\n')

    def ok(self, message, writem='ft'):
        message = self.slog_fmt(u'ok', message, 'green')
        self.slog_print(message, 5, writem)

    def info(self, message, writem='ft'):
        message = self.slog_fmt(u'info', message, 'blue')
        self.slog_print(message, 4, writem)

    def warn(self, message, writem='ft'):
        message = self.slog_fmt(u'warn', message, 'yellow')
        self.slog_print(message, 3, writem)

    def fail(self, message, writem='ft'):
        message = self.slog_fmt(u'fail', message, 'red')
        self.slog_print(message, 2, writem)

    def crit(self, message, writem='ft'):
        message = self.slog_fmt(u'crit', message, 'magenta', get_file_and_lineno)
        self.slog_print(message, 1, writem)

    def write(self, message, level=3, color='blue', writem='ft'):
        self.slog_fmt(level, message, color)
        self.slog_print(message, level, writem)

class SlogLevelError(Exception):
    pass

