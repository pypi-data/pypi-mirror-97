# coding:utf-8
from pick import pick
from halo import Halo
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from src.utils.color import Color
from src.user_info_manager import UserInfoManager


class Browser(object):
    TIMEOUT = 3
    ROOT_URL = "https://attendance.moneyforward.com"
    LOGIN_URL = ROOT_URL + "/employee_session/new"
    MYPAGE_URL = ROOT_URL + "/my_page"
    ATTENDANCE_URL = MYPAGE_URL + "/attendances"
    LOGIN_SUCCEED = "ログインに成功しました。"
    LOGIN_FAILED = "ログインに失敗しました。"

    DRIVER = "DRIVER"
    SAFARI = "Safari Drievr"
    CHROME = "Chrome Drievr"

    def __init__(self, headless=True):
        self.headless = headless
        self.info_manager = UserInfoManager()
        self.setup_userinfo()

    def setup_userinfo(self):
        self.userinfo = self.info_manager.get()
        self.set_driver_to_userinfo()
        self.set_driver()

    def set_driver(self):
        if self.userinfo[self.DRIVER] == self.SAFARI:
            self.driver = webdriver.Safari()
        else:
            options = webdriver.ChromeOptions()
            options.headless = self.headless
            self.driver = webdriver.Chrome(chrome_options=options)

    def set_driver_to_userinfo(self):
        if self.DRIVER not in self.userinfo.keys():
            message = "ブラウザドライバを選択してください:"
            options = [self.SAFARI, self.CHROME]
            option, _ = pick(options, message)
            self.userinfo[self.DRIVER] = option

    def login(self):
        spinner = Halo(text="ログインページをロードしています...", spinner="dots")
        spinner.start()
        self.driver.get(self.LOGIN_URL)
        spinner.succeed("ログインページのロードを完了しました。")

        spinner = Halo(text="ログイン中...", spinner="dots")
        spinner.start()
        return self.login_with_userinfo(spinner)

    def login_with_userinfo(self, spinner):
        self.driver.find_element_by_id(
            "employee_session_form_office_account_name"
        ).send_keys(self.userinfo[self.info_manager.CORP_ID])
        self.driver.find_element_by_id(
            "employee_session_form_account_name_or_email"
        ).send_keys(self.userinfo[self.info_manager.USER_ID])
        self.driver.find_element_by_id("employee_session_form_password").send_keys(
            self.userinfo[self.info_manager.USER_PASS]
        )

        self.driver.find_element_by_class_name(
            "attendance-before-login-card-button"
        ).click()

        return self.check_login(spinner)

    def check_login(self, spinner):
        try:
            WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, "attendance-card-title"))
            )
            self.info_manager.save(self.userinfo)
            spinner.succeed(self.LOGIN_SUCCEED)
            return True

        except TimeoutException:
            if self.driver.find_elements(By.CLASS_NAME, "is-error") != 0:
                Color.print(Color.RED, "\n企業ID, ユーザーID もしくはパスワードが間違っています。")
                spinner.fail(self.LOGIN_FAILED)
                UserInfoManager.remove()
                return False
            else:
                Color.print(Color.RED, "\nログイン中にタイムアウトしました。")
                spinner.fail(self.LOGIN_FAILED)
                return False

    def open_attendance(self):
        if self.login():
            spinner = Halo(text="日次勤怠ページをロードしています...", spinner="dots")
            self.driver.get(self.ATTENDANCE_URL)

        try:
            WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "modal-controller-my-page-attendances")
                )
            )
            spinner.succeed("日次勤怠ページのロードを完了しました。")
            return True

        except TimeoutException:
            return False

    def open_prev_attendance(self):
        if self.open_attendance():
            spinner = Halo(text="先月の日次勤怠ページをロードしています...", spinner="dots")
            self.driver.find_element_by_class_name(
                "attendance-table-header-month-range-previous"
            ).click()
            # 先月の日次勤怠ページ表示までsleepを挟む
            sleep(1)

        try:
            WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "modal-controller-my-page-attendances")
                )
            )
            spinner.succeed("先月の日次勤怠ページのロードを完了しました。")
            return True

        except TimeoutException:
            return False
