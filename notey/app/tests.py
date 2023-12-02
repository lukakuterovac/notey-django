import time

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


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
    def test_login_form(self):
        user = User.objects.create_user(
            username="testuser", email="test@user.com", password="12345"
        )

        self.driver.get(self.live_server_url + "/login")

        username_input_xpath = '//*[@id="id_username"]'
        password_input_xpath = '//*[@id="id_password"]'
        login_button_xpath = "/html/body/div/div[2]/div/form/button"

        username_input = self.driver.find_element(By.XPATH, username_input_xpath)
        password_input = self.driver.find_element(By.XPATH, password_input_xpath)
        login_button = self.driver.find_element(By.XPATH, login_button_xpath)

        username_input.send_keys("testuser")
        password_input.send_keys("12345")
        login_button.click()
        time.sleep(0.5)

        homepage_url = self.live_server_url + "/"
        current_url = self.driver.current_url

        self.assertEqual(
            current_url, homepage_url, "Login did not redirect back to the homepage"
        )


class RegistrationFormTest(SeleniumTestCase):
    def test_registration_form(self):
        self.driver.get(self.live_server_url + "/register")

        username_input_xpath = '//*[@id="id_username"]'
        email_input_xpath = '//*[@id="id_email"]'
        password1_input_xpath = '//*[@id="id_password1"]'
        password2_input_xpath = '//*[@id="id_password2"]'
        register_button_xpath = "/html/body/div/div[2]/div/form/button"

        username_input = self.driver.find_element(By.XPATH, username_input_xpath)
        email_input = self.driver.find_element(By.XPATH, email_input_xpath)
        password1_input = self.driver.find_element(By.XPATH, password1_input_xpath)
        password2_input = self.driver.find_element(By.XPATH, password2_input_xpath)
        register_button = self.driver.find_element(By.XPATH, register_button_xpath)

        username = "testuser"
        email = "test@user.com"
        password = "testpassword"

        username_input.send_keys(username)
        email_input.send_keys(email)
        password1_input.send_keys(password)
        password2_input.send_keys(password)
        register_button.click()
        time.sleep(0.5)

        homepage_url = self.live_server_url + "/"
        current_url = self.driver.current_url

        self.assertEqual(
            current_url,
            homepage_url,
            "Registration did not redirect back to the homepage",
        )


class LogoutFormTest(SeleniumTestCase):
    def test_logout_form(self):
        user = User.objects.create_user(
            username="testuser", email="test@user.com", password="12345"
        )

        self.driver.get(self.live_server_url + "/login")

        username_input_xpath = '//*[@id="id_username"]'
        password_input_xpath = '//*[@id="id_password"]'
        login_button_xpath = "/html/body/div/div[2]/div/form/button"

        username_input = self.driver.find_element(By.XPATH, username_input_xpath)
        password_input = self.driver.find_element(By.XPATH, password_input_xpath)
        login_button = self.driver.find_element(By.XPATH, login_button_xpath)

        username_input.send_keys("testuser")
        password_input.send_keys("12345")
        login_button.click()
        time.sleep(0.5)

        # homepage_url = self.live_server_url + "/"
        # current_url = self.driver.current_url

        # self.assertEqual(
        #     current_url, homepage_url, "Login did not redirect back to the homepage"
        # )

        account_dropdown_xpath = '//*[@id="navbarMenu"]/ul[3]/li/a'
        logout_button_xpath = '//*[@id="navbarMenu"]/ul[3]/li/ul/li/a'

        account_dropdown = self.driver.find_element(By.XPATH, account_dropdown_xpath)
        logout_button = self.driver.find_element(By.XPATH, logout_button_xpath)

        account_dropdown.click()
        time.sleep(0.5)

        logout_button.click()
        time.sleep(0.5)

        account_dropdown = self.driver.find_element(By.XPATH, account_dropdown_xpath)

        self.assertEqual(account_dropdown.text, "Account", "Failed to logout")
