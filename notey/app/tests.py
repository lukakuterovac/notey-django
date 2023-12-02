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
        User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

        self.driver.get(self.live_server_url + "/login")

        username_input_xpath = '//*[@id="id_username"]'
        password_input_xpath = '//*[@id="id_password"]'
        login_button_xpath = "/html/body/div/div[2]/div/form/button"

        username_input = self.driver.find_element(By.XPATH, username_input_xpath)
        password_input = self.driver.find_element(By.XPATH, password_input_xpath)
        login_button = self.driver.find_element(By.XPATH, login_button_xpath)

        username_input.send_keys("testuser")
        password_input.send_keys("testpassword")
        login_button.click()
        time.sleep(0.5)

        homepage_url = self.live_server_url + "/"
        current_url = self.driver.current_url

        self.assertEqual(current_url, homepage_url, "Failed login attempt")


class RegistrationFormTest(SeleniumTestCase):
    def test_successful_registration(self):
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

        username = "newuser"
        email = "newuser@example.com"
        password = "testpassword"

        username_input.send_keys(username)
        email_input.send_keys(email)
        password1_input.send_keys(password)
        password2_input.send_keys(password)
        register_button.click()
        time.sleep(0.5)

        self.assertTrue(
            self.is_user_registered(username), "Failed registration attempt"
        )

    def test_duplicate_username_registration_prevention(self):
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

        existing_user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

        username_input.send_keys(existing_user.username)
        email_input.send_keys("newemail@example.com")
        password1_input.send_keys("testpassword")
        password2_input.send_keys("testpassword")
        register_button.click()
        time.sleep(0.5)

        username_error_xpath = '//*[@id="error_1_id_username"]'

        try:
            username_error_element = self.driver.find_element(
                By.XPATH, username_error_xpath
            )
            self.assertIn("already exists", username_error_element.text)
        except NoSuchElementException:
            self.fail("No error message displayed for duplicate username")

    def test_duplicate_email_registration_prevention(self):
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

        existing_user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

        username_input.send_keys("newuser")
        email_input.send_keys(existing_user.email)
        password1_input.send_keys("testpassword")
        password2_input.send_keys("testpassword")
        register_button.click()
        time.sleep(0.5)

        email_error_xpath = '//*[@id="error_1_id_email"]'

        try:
            email_error_element = self.driver.find_element(By.XPATH, email_error_xpath)
            self.assertIn("already exists", email_error_element.text)
        except NoSuchElementException:
            self.fail("No error message displayed for duplicate email")

    def is_user_registered(self, username):
        try:
            User.objects.get(username=username)
            return True
        except User.DoesNotExist:
            return False


class LogoutFormTest(SeleniumTestCase):
    def test_logout_form(self):
        User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

        self.driver.get(self.live_server_url + "/login")

        username_input_xpath = '//*[@id="id_username"]'
        password_input_xpath = '//*[@id="id_password"]'
        login_button_xpath = "/html/body/div/div[2]/div/form/button"

        username_input = self.driver.find_element(By.XPATH, username_input_xpath)
        password_input = self.driver.find_element(By.XPATH, password_input_xpath)
        login_button = self.driver.find_element(By.XPATH, login_button_xpath)

        username_input.send_keys("testuser")
        password_input.send_keys("testpassword")
        login_button.click()
        time.sleep(0.5)

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


class NewProjectFormTest(SeleniumTestCase):
    def test_new_project_form(self):
        self.login()

        self.driver.get(self.live_server_url + "/projects")

        new_project_card_xpath = '//*[@id="modal-toggle"]'

        new_project_card = self.driver.find_element(By.XPATH, new_project_card_xpath)

        new_project_card.click()
        time.sleep(0.5)

        project_name = "Test project"

        project_name_input_xpath = '//*[@id="id_name"]'
        create_button_xpath = '//*[@id="exampleModal"]/div/div/form/div[2]/button'

        project_name_input = self.driver.find_element(
            By.XPATH, project_name_input_xpath
        )
        create_button = self.driver.find_element(By.XPATH, create_button_xpath)

        project_name_input.send_keys(project_name)
        create_button.click()
        time.sleep(0.5)

        created_project_card_xpath = "/html/body/div/div[2]/div/div[2]/a[2]"

        created_project_card = self.driver.find_element(
            By.XPATH, created_project_card_xpath
        )

        self.assertEqual(
            created_project_card.text, project_name, "Failed to create project"
        )

    def test_duplicate_name_new_project_form_prevention(self):
        self.login()

        self.driver.get(self.live_server_url + "/projects")

        new_project_card_xpath = '//*[@id="modal-toggle"]'

        new_project_card = self.driver.find_element(By.XPATH, new_project_card_xpath)

        new_project_card.click()
        time.sleep(0.5)

        project_name = "Test project"

        project_name_input_xpath = '//*[@id="id_name"]'
        create_button_xpath = '//*[@id="exampleModal"]/div/div/form/div[2]/button'

        project_name_input = self.driver.find_element(
            By.XPATH, project_name_input_xpath
        )
        create_button = self.driver.find_element(By.XPATH, create_button_xpath)

        project_name_input.send_keys(project_name)
        create_button.click()
        time.sleep(0.5)

        new_project_card = self.driver.find_element(By.XPATH, new_project_card_xpath)

        new_project_card.click()
        time.sleep(0.5)

        project_name_input = self.driver.find_element(
            By.XPATH, project_name_input_xpath
        )
        create_button = self.driver.find_element(By.XPATH, create_button_xpath)

        project_name_input.send_keys(project_name)
        create_button.click()
        time.sleep(0.5)

        form_error_xpath = '//*[@id="error_1_id_name"]'

        try:
            form_error = self.driver.find_element(By.XPATH, form_error_xpath)
            self.assertIn("already exists", form_error.text)
        except NoSuchElementException:
            self.fail("No error message displayed for project with duplicate name")

    def login(self):
        User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

        self.driver.get(self.live_server_url + "/login")

        username_input_xpath = '//*[@id="id_username"]'
        password_input_xpath = '//*[@id="id_password"]'
        login_button_xpath = "/html/body/div/div[2]/div/form/button"

        username_input = self.driver.find_element(By.XPATH, username_input_xpath)
        password_input = self.driver.find_element(By.XPATH, password_input_xpath)
        login_button = self.driver.find_element(By.XPATH, login_button_xpath)

        username_input.send_keys("testuser")
        password_input.send_keys("testpassword")
        login_button.click()
        time.sleep(0.5)
