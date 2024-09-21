from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):  # Class for Login
    # Mention the locators
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE = (By.XPATH, "//p[text()='Invalid credentials']")

    def login(self, username, password):  # Method to login
        self.enter_text(self.USERNAME, username)
        self.enter_text(self.PASSWORD, password)
        self.click_element(self.LOGIN_BUTTON)

        # Check if the login was successful by verifying the presence of 'dashboard' in the current URL
        try:
            assert "dashboard" in self.driver.current_url
            print("Successfully Logged In")
        except AssertionError as e:
            print(f"Error Occurred: {e}")
            error_message = self.find_element(self.ERROR_MESSAGE)
            print("Error Message:", error_message.text)

