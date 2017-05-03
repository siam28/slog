#!/usr/bin/python
# coding=utf8

import logging

from inspect import currentframe, getframeinfo
from time import strftime, sleep
from termcolor import colored

def ct():
    return strftime('%Y-%m-%d %H:%M:%S')

class Slog(object):
    def __init__(self, logfile=None, loglvl=3, inspect=False, bufsize=4096, splotch=u'⬢'):
        # the log file
        if logfile is not None:
            self.logfile = open(logfile, 'w+', bufsize)
        else:
            self.logfile = None

        # acceptable string log levels
        loglvls = ['silent', 'crit', 'fail', 'warn', 'info', 'all']

        if type(loglvl) is int and 0 <= loglvl <= 5:
            self.loglvl = loglvl
        elif loglvl in loglvls:
            try:
                self.loglvl = loglvls.index(loglvl)
            except ValueError:
                raise SlogLevelError('{0} is not a valid Slog log level.'.format(loglvl))
        else:
            raise SlogLevelError('{0} is not a valid Slog log level.'.format(loglvl))

        # whether or not calls to `inspect` functions will be made
        if inspect:
            self.inspect_func = self.get_file_and_lineno
        else:
            self.inspect_func = self.null_inspect

        # custom splotch
        self.splotch = splotch

    def get_file_and_lineno(self):
        fn = currentframe().f_back.f_back.f_back.f_code.co_filename
        fn = fn.split('/')[-1]
        lineno = currentframe().f_back.f_back.f_back.f_lineno
        return ' (\033[1m{0}:{1}\033[0m) '.format(fn, lineno)

    def null_inspect(self):
        return ' '

    def __del__(self):
        if self.logfile:
            self.logfile.close()

    def slog_fmt(self, level, message, color, fnln=None):
        if fnln is None:
            fnln = self.inspect_func
        if level != 'ok':
            return [
                    '\r' + ct() + ' || [ ' + level.upper() + ' ] ' + colored(self.splotch, color) + fnln() + message,
                    '\r' + ct() + ' || [ ' + level.upper() + ' ] ' + fnln() + message]
        else:
            return [
                    '\r' + ct() + ' || [  '+ level.upper() +'  ] ' + colored(self.splotch, color) + fnln() + message,
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
        message = self.slog_fmt(u'crit', message, 'magenta', self.get_file_and_lineno)
        self.slog_print(message, 1, writem)

    def write(self, message, level=3, color='blue', writem='ft'):
        self.slog_fmt(level, message, color)
        self.slog_print(message, level, writem)

class SlogLevelError(Exception):
    pass

