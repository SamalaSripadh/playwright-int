from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from pages.base_page import BasePage


class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def go_to_products_page(self):
        self.go_to_url("/products")

    def search_product(self, product_name):
        self.do_fill(self.page.locator("#search_product"), product_name)
        self.do_click(self.page.locator("#submit_search"))

    def is_products_title_visible(self):
        return self.is_visible(".title.text-center")

    def are_search_results_visible(self):
        return self.is_visible(".features_items .productinfo")

    def is_empty_state_visible(self):
        return self.is_visible(".features_items .title")

    def add_product_to_cart(self, product_name):
        product = self.page.locator(".single-products:visible").filter(has_text=product_name).first
        product.hover()
        add_to_cart = product.locator(".productinfo a.add-to-cart")
        cart_modal = self.page.locator("#cartModal")
        add_to_cart.click(force=True)
        try:
            cart_modal.wait_for(state="visible", timeout=10000)
        except PlaywrightTimeoutError:
            add_to_cart.click(force=True)
            cart_modal.wait_for(state="visible", timeout=10000)

    def continue_shopping(self):
        cart_modal = self.page.locator("#cartModal")
        cart_modal.locator("button.close-modal").click(force=True)
        cart_modal.wait_for(state="hidden", timeout=10000)

    def click_cart(self):
        modal_cart_link = self.page.locator("#cartModal a[href='/view_cart']")
        if modal_cart_link.is_visible():
            modal_cart_link.click(force=True)
        else:
            self.do_click(self.page.locator("a[href='/view_cart']").first)