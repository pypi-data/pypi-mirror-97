# coding:utf-8


class Color(object):
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    END = "\033[0m"

    @classmethod
    def get_colored(cls, color, text):
        return color + text + cls.END

    @classmethod
    def print(cls, color, text):
        print(cls.get_colored(color, text))
