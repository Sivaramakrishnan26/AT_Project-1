from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class PimDeletePage(BasePage):  # Class for deleting an existing employee
    # Mention the locators
    PIM = (By.XPATH, "//span[text()='PIM']")
    INPUT_NAME = (By.XPATH, "//input[@placeholder='Type for hints...']")
    SEARCH_BUTTON = (By.XPATH, "//button[text()=' Search ']")
    DELETE_BUTTON = (By.XPATH, "//*[@id='app']/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/div[2]/div/div/div[9]/div/button[2]")
    CONFIRM_DELETE = (By.XPATH, "//button[text()=' Yes, Delete ']")

    # Method to delete an existing employee
    def delete_user(self, employee_name):
        self.click_element(self.PIM)

        Enter_Employee_Name = self.find_elements(self.INPUT_NAME)
        EMPLOYEE_NAME = Enter_Employee_Name[0]
        EMPLOYEE_NAME.send_keys(employee_name)

        time.sleep(2)
        self.click_element(self.SEARCH_BUTTON)

        time.sleep(5)
        self.click_element(self.DELETE_BUTTON)
        self.click_element(self.CONFIRM_DELETE)
