# coding:utf-8
from src.browser import Browser
from src.utils.color import Color
from src.utils.calc import Calc


class StampManager(object):
    def __init__(self):
        self.browser = Browser()
        self.driver = self.browser.driver

    def stamp(self, method):
        if self.login() and method in dir(self):
            if (fun := getattr(self, method)):
                fun()
            self.exit()

    def login(self):
        return self.browser.login()

    def clock_execute(self, selector, time_prefix):
        if self.driver.current_url != self.browser.MYPAGE_URL:
            print("Please login.")

        self.driver.find_element_by_class_name(selector).click()
        print(time_prefix + Calc.current_time())

    def start(self):
        selector = "attendance-card-time-stamp-clock-in"
        prefix = Color.get_colored(Color.BOLD, "出勤: ")
        self.clock_execute(selector, prefix)

        Color.print(Color.GREEN, "打刻が完了しました。良い一日を！")

    def end(self):
        selector = "attendance-card-time-stamp-clock-out"
        prefix = Color.get_colored(Color.BOLD, "退勤: ")
        self.clock_execute(selector, prefix)

        Color.print(Color.GREEN, "打刻が完了しました。一日お疲れ様でした！")

    def start_break(self):
        selector = "attendance-card-time-stamp-start-break"
        prefix = Color.get_colored(Color.BOLD, "休憩開始: ")
        self.clock_execute(selector, prefix)

        Color.print(Color.GREEN, "休憩開始の打刻が完了しました。")

    def end_break(self):
        selector = "attendance-card-time-stamp-end-break"
        prefix = Color.get_colored(Color.BOLD, "休憩終了: ")
        self.clock_execute(selector, prefix)

        Color.print(Color.GREEN, "休憩終了の打刻が完了しました。")

    def exit(self):
        self.driver.close()
