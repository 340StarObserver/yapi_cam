# -*- coding: utf-8 -*-

from swoole.common.global_tool import fill_error_code

class BaseController(object):
    def __init__(self, para, res, logger):
        self.para   = para
        self.res    = res
        self.logger = logger

    def handler(self):
        fill_error_code(self.res, "invalid_method")
