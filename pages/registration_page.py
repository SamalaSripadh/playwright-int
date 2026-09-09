
class RegistrationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        
    registration_page_btn_loc= self.page.locator("a[href='/login']")
    
    def go_to_registration_page(self):
        self.do_click(registration_page_btn_loc)
        
    def enter_name(self, name_field_loc, name):
        self.do_fill(name_field_loc, name)
    
    def enter_email(self, email_field_loc, email):
        self.do_fill(email_field_loc, email)
    
    def click_signup_button(self, signup_button_loc):
        self.do_click(signup_button_loc)
    
    title_radio_loc = [self.page.locator("input#id_gender1"), self.page.locator("input#id_gender2")]
    name_field_loc = self.page.locator("input#name")
    email_field_loc = self.page.locator("input#email")
    password_field_loc = self.page.locator("input#password")
    day_dropdown_loc = self.page.locator("select#days")
    month_dropdown_loc = self.page.locator("select#months")
    year_dropdown_loc = self.page.locator("select#years")
    newsletter_checkbox_loc = self.page.locator("input#newsletter")
    offers_checkbox_loc = self.page.locator("input#optin")
    first_name_field_loc = self.page.locator("input#first_name")
    last_name_field_loc = self.page.locator("input#last_name")
    company_field_loc = self.page.locator("input#company")
    address1_field_loc = self.page.locator("input#address1")
    address2_field_loc = self.page.locator("input#address2")
    country_dropdown_loc = self.page.locator("select#country")
    state_field_loc = self.page.locator("input#state")
    city_field_loc = self.page.locator("input#city")
    zipcode_field_loc = self.page.locator("input#zipcode")
    mobile_number_field_loc = self.page.locator("input#mobile_number")
        
    def fill_account_information(self, title, name, email, password, day, month, year, newsletter, offers, first_name, last_name, company, address1, address2, country, state, city, zipcode, mobile_number):
        if title == "Mr":
            self.do_check(self.title_radio_loc[0])
        elif title == "Mrs":
            self.do_check(self.title_radio_loc[1])
        self.do_fill(self.name_field_loc, name)
        self.do_fill(self.email_field_loc, email)
        self.do_fill(self.password_field_loc, password)
        self.do_select(self.day_dropdown_loc, day)
        self.do_select(self.month_dropdown_loc, month)
        self.do_select(self.year_dropdown_loc, year)
        if newsletter:
            self.do_check(self.newsletter_checkbox_loc)
        if offers:
            self.do_check(self.offers_checkbox_loc)
        self.do_fill(self.first_name_field_loc, first_name)
        self.do_fill(self.last_name_field_loc, last_name)
        self.do_fill(self.company_field_loc, company)
        self.do_fill(self.address1_field_loc, address1)
        self.do_fill(self.address2_field_loc, address2)
        self.do_select(self.country_dropdown_loc, country)
        self.do_fill(self.state_field_loc, state)
        self.do_fill(self.city_field_loc, city)
        self.do_fill(self.zipcode_field_loc, zipcode)
        self.do_fill(self.mobile_number_field_loc, mobile_number)
    
    create_account_button_loc = self.page.locator("button[data-qa='create-account']")
    def click_create_account_button(self, create_account_button_loc):
        self.do_click(create_account_button_loc)