# coding:utf-8
import datetime as dt
from typing import Callable
from functools import wraps
from bs4 import BeautifulSoup

from src.browser import Browser
from src.utils.color import Color


class AttendanceManager(object):
    def __init__(self, headless=True):
        self.headless = headless
        self.browser = Browser(headless=headless)
        self.driver = self.browser.driver

    def confirm(self, method):
        if method in dir(self):
            if (fun := getattr(self, method)):
                fun()
            self.exit()

    def open_attendance(self):
        return self.browser.open_attendance()

    def open_prev_attendance(self):
        return self.browser.open_prev_attendance()

    def current_date(self):
        return dt.datetime.now().day

    def history(self):
        """
        dakoker history実行時に走る
        """
        if self.open_attendance():
            times = self.get_timetable(self.get_attendance)
            self.print_timetable(times)

    def overtime(self):
        """
        dakoker overtime 実行時に走る
        """
        if self.open_attendance():
            overtimes = self.get_timetable(self.get_overtime)
            self.print_overtime(overtimes)

    def prev_overtime(self):
        """
        dakoker prev_overtime 実行時に走る
        """
        if self.open_prev_attendance():
            overtimes = self.get_timetable(self.get_overtime)
            self.print_overtime(overtimes)

    def get_timetable(self, getter: Callable) -> list:
        """
        getterで指定した方法でタイムテーブルを取得する
        """
        timetable = getter()
        for i, time in enumerate(timetable):
            timetable[i] = [time for time in time.strings]

        return timetable

    def get_attendance(self) -> list:
        html = self.driver.page_source.encode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        attendances = soup.find_all("td", class_="column-attendance")

        attendance_array = []
        time = 0
        while time < len(attendances):
            attendance_array.append(attendances[time : time + 4])
            time += 4

        return attendance_array[self.current_date() - 1]

    def get_overtime(self) -> list:
        html = self.driver.page_source.encode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        normal = (
            soup.select(".attendance-table-contents")[3].select("tr")[2].select("td")[3]
        )
        designated = (
            soup.select(".attendance-table-contents")[3].select("tr")[3].select("td")[3]
        )
        law = (
            soup.select(".attendance-table-contents")[3].select("tr")[4].select("td")[3]
        )

        return [normal, designated, law]

    def exit(self):
        self.driver.close()

    def printer(func: Callable) -> Callable:
        """
        print系メソッド用のラッパー関数
        """

        @wraps(func)
        def newfunc(*args) -> None:
            print("================================")
            func(*args)
            print("================================")

        return newfunc

    @printer
    def print_timetable(self, times):
        texts = [
            Color.get_colored(Color.BOLD, "出勤:     ") + ", ".join(times[0]),
            Color.get_colored(Color.BOLD, "退勤:     ") + ", ".join(times[1]),
            Color.get_colored(Color.BOLD, "休憩開始: ") + ", ".join(times[2]),
            Color.get_colored(Color.BOLD, "休憩終了: ") + ", ".join(times[3]),
        ]
        for text in texts:
            print(text)

    @printer
    def print_overtime(self, times):
        texts = [
            "各残業時間",
            Color.get_colored(Color.BOLD, "平日:     ") + ", ".join(times[0]),
            Color.get_colored(Color.BOLD, "所定休日: ") + ", ".join(times[1]),
            Color.get_colored(Color.BOLD, "法定休日: ") + ", ".join(times[2]),
        ]
        for text in texts:
            print(text)
