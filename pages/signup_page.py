from playwright.sync_api import Page
from pages.base_page import BasePage


class SignupPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def go_to_signup_page(self):
        self.go_to_url("/login")

    def enter_signup_name(self, name):
        self.do_fill(self.page.locator("[data-qa='signup-name']"), name)

    def enter_signup_email(self, email):
        self.do_fill(self.page.locator("[data-qa='signup-email']"), email)

    def click_signup(self):
        self.do_click(self.page.locator("[data-qa='signup-button']"))

    def select_gender(self, gender):
        self.do_click(self.page.locator(f"#id_gender{gender}"))

    def enter_password(self, password):
        self.do_fill(self.page.locator("[data-qa='password']"), password)

    def enter_first_name(self, first_name):
        self.do_fill(self.page.locator("[data-qa='first_name']"), first_name)

    def enter_last_name(self, last_name):
        self.do_fill(self.page.locator("[data-qa='last_name']"), last_name)

    def select_date_of_birth(self, day, month, year):
        self.page.locator("[data-qa='days']").select_option(label=str(day))
        self.page.locator("[data-qa='months']").select_option(label=str(month))
        self.page.locator("[data-qa='years']").select_option(label=str(year))

    def enter_address(self, address):
        self.do_fill(self.page.locator("[data-qa='address']"), address)

    def select_country(self, country):
        self.page.locator("[data-qa='country']").select_option(label=country)

    def enter_state(self, state):
        self.do_fill(self.page.locator("[data-qa='state']"), state)

    def enter_city(self, city):
        self.do_fill(self.page.locator("[data-qa='city']"), city)

    def enter_zipcode(self, zipcode):
        self.do_fill(self.page.locator("[data-qa='zipcode']"), zipcode)

    def enter_mobile_number(self, mobile_number):
        self.do_fill(self.page.locator("[data-qa='mobile_number']"), mobile_number)

    def click_create_account(self):
        self.do_click(self.page.locator("[data-qa='create-account']"))

    def click_continue(self):
        self.do_click(self.page.locator("[data-qa='continue-button']"))

    def is_account_created_visible(self):
        return self.is_visible("[data-qa='account-created']")

    def is_existing_email_error_visible(self):
        return self.is_visible("p:has-text('Email Address already exist!')")

    def is_signup_form_visible(self):
        return self.is_visible(".signup-form")