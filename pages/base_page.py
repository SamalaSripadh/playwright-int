from playwright.sync_api import Page, Locator

class BasePage:
    def __init__(self, page:Page):
        self.page = page

    def go_to_url(self, url:str):
        self.page.goto(url, wait_until="domcontentloaded")

    def do_click(self, locator: Locator):
        locator.click()

    def do_fill(self, locator: Locator, value: str):
        locator.fill(value)

    def do_check(self, locator: Locator):
        locator.check()

    def do_select(self, locator: Locator, value):
        value = int(value)
        locator.select_option(index=value)

    def is_visible(self, locator: Locator):
        if isinstance(locator, str):
            locator = self.page.locator(locator)
        return locator
