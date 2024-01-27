import time

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


# POMs
class LoginForm:
    USERNAME_INPUT_XPATH = '//*[@id="id_username"]'
    PASSWORD_INPUT_XPATH = '//*[@id="id_password"]'
    LOGIN_BUTTON_XPATH = "/html/body/div/div[2]/div/form/button"

    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.XPATH, self.USERNAME_INPUT_XPATH)
        self.password_input = (By.XPATH, self.PASSWORD_INPUT_XPATH)
        self.login_button = (By.XPATH, self.LOGIN_BUTTON_XPATH)

    def enter_credentials(self, username, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)

    def click_login_button(self):
        self.driver.find_element(*self.login_button).click()


class RegistrationForm:
    USERNAME_INPUT_XPATH = '//*[@id="id_username"]'
    EMAIL_INPUT_XPATH = '//*[@id="id_email"]'
    PASSWORD1_INPUT_XPATH = '//*[@id="id_password1"]'
    PASSWORD2_INPUT_XPATH = '//*[@id="id_password2"]'
    REGISTER_BUTTON_XPATH = "/html/body/div/div[2]/div/form/button"
    USERNAME_ERROR_XPATH = '//*[@id="error_1_id_username"]'
    EMAIL_ERROR_XPATH = '//*[@id="error_1_id_email"]'

    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.XPATH, self.USERNAME_INPUT_XPATH)
        self.email_input = (By.XPATH, self.EMAIL_INPUT_XPATH)
        self.password1_input = (By.XPATH, self.PASSWORD1_INPUT_XPATH)
        self.password2_input = (By.XPATH, self.PASSWORD2_INPUT_XPATH)
        self.register_button = (By.XPATH, self.REGISTER_BUTTON_XPATH)
        self.username_error = (By.XPATH, self.USERNAME_ERROR_XPATH)
        self.email_error = (By.XPATH, self.EMAIL_ERROR_XPATH)

    def enter_credentials(self, username, email, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.email_input).send_keys(email)
        self.driver.find_element(*self.password1_input).send_keys(password)
        self.driver.find_element(*self.password2_input).send_keys(password)

    def click_register_button(self):
        self.driver.find_element(*self.register_button).click()

    def username_error_exists(self):
        try:
            self.driver.find_element(*self.username_error)
            return True
        except NoSuchElementException:
            return False

    def email_error_exists(self):
        try:
            self.driver.find_element(*self.email_error)
            return True
        except NoSuchElementException:
            return False


class LogoutForm:
    ACCOUNT_DROPDOWN_XPATH = '//*[@id="navbarMenu"]/ul[3]/li/a'
    LOGOUT_BUTTON_XPATH = '//*[@id="navbarMenu"]/ul[3]/li/ul/li/a'

    def __init__(self, driver):
        self.driver = driver
        self.account_dropdown = (By.XPATH, self.ACCOUNT_DROPDOWN_XPATH)
        self.logout_button = (By.XPATH, self.LOGOUT_BUTTON_XPATH)

    def logout(self):
        self.driver.find_element(*self.account_dropdown).click()
        time.sleep(0.5)
        self.driver.find_element(*self.logout_button).click()
        time.sleep(0.5)

    def get_account_dropdown_element(self):
        return self.driver.find_element(*self.account_dropdown)


class ProjectForm:
    NEW_PROJECT_CARD_XPATH = '//*[@id="modal-toggle"]'
    PROJECT_NAME_INPUT_XPATH = '//*[@id="id_name"]'
    CREATE_BUTTON_XPATH = '//*[@id="exampleModal"]/div/div/form/div[2]/button'
    CREATED_PROJECT_CARD_XPATH = "/html/body/div/div[2]/div/div[2]/a[2]"
    FORM_ERROR_XPATH = '//*[@id="error_1_id_name"]'

    def __init__(self, driver):
        self.driver = driver
        self.new_project_card = (By.XPATH, self.NEW_PROJECT_CARD_XPATH)
        self.project_name_input = (By.XPATH, self.PROJECT_NAME_INPUT_XPATH)
        self.create_button = (By.XPATH, self.CREATE_BUTTON_XPATH)
        self.created_project = (By.XPATH, self.CREATED_PROJECT_CARD_XPATH)
        self.form_error = (By.XPATH, self.FORM_ERROR_XPATH)

    def create_project(self, project_name):
        self.driver.find_element(*self.new_project_card).click()
        time.sleep(0.5)
        self.driver.find_element(*self.project_name_input).send_keys(project_name)
        self.driver.find_element(*self.create_button).click()
        time.sleep(0.5)

    def get_new_project_element(self):
        return self.driver.find_element(*self.created_project)

    def form_error_exists(self):
        try:
            self.driver.find_element(*self.form_error)
            return True
        except NoSuchElementException:
            return False


# Tests
class SeleniumTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


class LoginFormTest(SeleniumTestCase):
    USERNAME = "testuser"
    EMAIL = "testuser@example.com"
    PASSWORD = "testpassword"
    FAIL_MSG = "Failed login attempt"

    def test_login_form(self):
        User.objects.create_user(self.USERNAME, self.EMAIL, self.PASSWORD)

        self.driver.get(self.live_server_url + "/login")
        login_form = LoginForm(self.driver)

        login_form.enter_credentials(self.USERNAME, self.PASSWORD)
        login_form.click_login_button()
        time.sleep(0.5)

        homepage_url = self.live_server_url + "/"
        current_url = self.driver.current_url

        self.assertEqual(current_url, homepage_url, self.FAIL_MSG)


class RegistrationFormTest(SeleniumTestCase):
    USERNAME = "testuser"
    EMAIL = "testuser@example.com"
    PASSWORD = "testpassword"
    FAIL_MSG = "Failed registration attempt"

    def test_successful_registration(self):
        self.driver.get(self.live_server_url + "/register")
        registration_form = RegistrationForm(self.driver)

        registration_form.enter_credentials(self.USERNAME, self.EMAIL, self.PASSWORD)
        registration_form.click_register_button()
        time.sleep(0.5)

        self.assertTrue(self.is_user_registered(self.USERNAME), self.FAIL_MSG)

    def test_duplicate_username_registration_prevention(self):
        self.driver.get(self.live_server_url + "/register")
        registration_form = RegistrationForm(self.driver)

        User.objects.create_user(
            self.USERNAME, "existinguser@example.com", self.PASSWORD
        )

        registration_form.enter_credentials(self.USERNAME, self.EMAIL, self.PASSWORD)
        registration_form.click_register_button()
        time.sleep(0.5)

        self.assertTrue(registration_form.username_error_exists())

    def test_duplicate_email_registration_prevention(self):
        self.driver.get(self.live_server_url + "/register")
        registration_form = RegistrationForm(self.driver)

        User.objects.create_user("existinguser", self.EMAIL, self.PASSWORD)

        registration_form.enter_credentials(self.USERNAME, self.EMAIL, self.PASSWORD)
        registration_form.click_register_button()
        time.sleep(0.5)

        self.assertTrue(registration_form.email_error_exists())

    def is_user_registered(self, username):
        try:
            User.objects.get(username=username)
            return True
        except User.DoesNotExist:
            return False


class LogoutFormTest(SeleniumTestCase):
    USERNAME = "testuser"
    EMAIL = "testuser@example.com"
    PASSWORD = "testpassword"
    FAIL_MSG = "Failed logout attempt"

    def test_logout_form(self):
        User.objects.create_user(self.USERNAME, self.EMAIL, self.PASSWORD)

        self.driver.get(self.live_server_url + "/login")
        login_form = LoginForm(self.driver)
        logout_form = LogoutForm(self.driver)

        login_form.enter_credentials(self.USERNAME, self.PASSWORD)
        login_form.click_login_button()
        time.sleep(0.5)

        logout_form.logout()
        time.sleep(0.5)

        account_dropdown = logout_form.get_account_dropdown_element()

        self.assertEqual(account_dropdown.text, "Account", self.FAIL_MSG)


class ProjectFormTest(SeleniumTestCase):
    USERNAME = "testuser"
    EMAIL = "testuser@example.com"
    PASSWORD = "testpassword"
    FAIL_MSG = "Failed to create project"

    def test_project_form(self):
        self.driver.get(self.live_server_url + "/login")
        User.objects.create_user(self.USERNAME, self.EMAIL, self.PASSWORD)
        login_form = LoginForm(self.driver)

        login_form.enter_credentials(self.USERNAME, self.PASSWORD)
        login_form.click_login_button()
        time.sleep(0.5)

        self.driver.get(self.live_server_url + "/projects")
        project_name = "Test project"
        project_form = ProjectForm(self.driver)
        project_form.create_project(project_name)

        created_project_card = project_form.get_new_project_element()

        self.assertEqual(created_project_card.text, project_name, self.FAIL_MSG)

    def test_duplicate_name_project_form_prevention(self):
        self.driver.get(self.live_server_url + "/login")
        User.objects.create_user(self.USERNAME, self.EMAIL, self.PASSWORD)
        login_form = LoginForm(self.driver)

        login_form.enter_credentials(self.USERNAME, self.PASSWORD)
        login_form.click_login_button()
        time.sleep(0.5)

        self.driver.get(self.live_server_url + "/projects")
        project_name = "Test project"
        project_form = ProjectForm(self.driver)
        project_form.create_project(project_name)
        project_form.create_project(project_name)

        self.assertTrue(project_form.form_error_exists())
