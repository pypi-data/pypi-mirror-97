# coding:utf-8
import datetime


class Calc(object):
    @staticmethod
    def current_time():
        return str(datetime.datetime.now()).split(".")[0]
