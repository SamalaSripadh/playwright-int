from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def go_to_cart_page(self):
        self.go_to_url("/view_cart")

    def product_row(self, product_name):
        return self.page.locator("#cart_info_table tbody tr").filter(has_text=product_name).first

    def is_product_visible(self, product_name):
        return self.product_row(product_name)

    def product_price(self, product_name):
        return self.product_row(product_name).locator(".cart_price").inner_text()

    def product_quantity(self, product_name):
        return self.product_row(product_name).locator(".cart_quantity").inner_text()

    def product_total(self, product_name):
        return self.product_row(product_name).locator(".cart_total").inner_text()

    def remove_product(self, product_name):
        self.product_row(product_name).locator(".cart_quantity_delete").click()

    def click_checkout(self):
        self.do_click(self.page.get_by_text("Proceed To Checkout"))

    def is_cart_empty_visible(self):
        return self.is_visible("#empty_cart")