from playwright.sync_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def go_to_home_page(self):
        self.go_to_url("/")

    def is_navbar_visible(self):
        return self.is_visible("header .shop-menu")

    def is_header_visible(self):
        return self.is_visible("header")

    def is_footer_visible(self):
        return self.is_visible("footer")

    def click_signup_login(self):
        self.do_click(self.page.get_by_text("Signup / Login"))

    def enter_subscription_email(self, email):
        self.do_fill(self.page.locator("#susbscribe_email"), email)

    def click_subscribe(self):
        self.do_click(self.page.locator("#subscribe"))

    def is_subscription_success_visible(self):
        return self.is_visible(".alert-success")







