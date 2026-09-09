from playwright.sync_api import Page
from pages.base_page import BasePage


class SubscriptionPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def enter_email(self, email):
        self.do_fill(self.page.locator("#susbscribe_email"), email)

    def click_subscribe(self):
        self.do_click(self.page.locator("#subscribe"))

    def is_success_message_visible(self):
        return self.is_visible(".alert-success")