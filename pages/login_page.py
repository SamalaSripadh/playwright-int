from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def enter_email(self, email):
        self.do_fill(self.page.locator("[data-qa='login-email']"), email)

    def enter_password(self, password):
        self.do_fill(self.page.locator("[data-qa='login-password']"), password)

    def click_login(self):
        self.do_click(self.page.locator("[data-qa='login-button']"))

    def click_logout(self):
        self.do_click(self.page.locator("a[href='/logout']"))

    def is_invalid_login_error_visible(self):
        return self.is_visible("p:has-text('Your email or password is incorrect!')")

    def is_logged_in_visible(self):
        return self.is_visible("a:has-text('Logged in as')")

    def is_login_form_visible(self):
        return self.is_visible(".login-form")