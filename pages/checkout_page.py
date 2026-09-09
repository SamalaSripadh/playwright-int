from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def is_address_details_visible(self):
        return self.is_visible("#address_delivery")

    def is_order_review_visible(self):
        return self.is_visible("#cart_info")

    def is_product_in_order_visible(self, product_name):
        return self.page.locator("#cart_info").get_by_text(product_name)