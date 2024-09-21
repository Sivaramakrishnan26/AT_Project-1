from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class PimAddPage(BasePage):  # Class for adding a new employee
    # Mention the locators
    PIM = (By.XPATH, "//span[text()='PIM']")
    ADD_BUTTON = (By.XPATH, "//*[text()=' Add ']")
    FIRST_NAME = (By.XPATH, "//input[@placeholder='First Name']")
    MIDDLE_NAME = (By.XPATH, "//input[@placeholder='Middle Name']")
    LAST_NAME = (By.XPATH, "//input[@placeholder='Last Name']")
    CHECKBOX = (By.XPATH, "//input[@type='checkbox']")
    INPUT_DETAILS = (By.CLASS_NAME, "oxd-input")
    SAVE_BUTTON = (By.XPATH, "//button[text()=' Save ']")
    DROPDOWN = (By.XPATH, "//div[text()='-- Select --']")
    GENDER = (By.XPATH, "//label[text()='Male']")

    # Method to add a new employee
    def add_user(self, first_name, middle_name, last_name, employee_id, dl_number, dl_exp_date, nationality, marital_status, date_of_birth, blood_type, test):
        self.click_element(self.PIM)
        self.click_element(self.ADD_BUTTON)
        self.enter_text(self.FIRST_NAME, first_name)
        self.enter_text(self.MIDDLE_NAME, middle_name)
        self.enter_text(self.LAST_NAME, last_name)

        Input_Details_Add = self.find_elements(self.INPUT_DETAILS)
        EMPLOYEE_ID = Input_Details_Add[4]
        EMPLOYEE_ID.send_keys(employee_id)

        time.sleep(2)
        self.click_element(self.SAVE_BUTTON)
        
        time.sleep(10)
        Input_Details_PIM = self.find_elements(self.INPUT_DETAILS)
        DL_NUMBER = Input_Details_PIM[6]
        DL_NUMBER.send_keys(dl_number)
        DL_EXP_DATE = Input_Details_PIM[7]
        DL_EXP_DATE.send_keys(dl_exp_date)
        DATE_OF_BIRTH = Input_Details_PIM[8]
        DATE_OF_BIRTH.send_keys(date_of_birth)
        TEST = Input_Details_PIM[9]
        TEST.send_keys(test)

        Dropdown = self.find_elements(self.DROPDOWN)
        NATIONALITY = Dropdown[0]
        MARITAL_STATUS = Dropdown[1]
        BLOOD_TYPE = Dropdown[2]
        NATIONALITY.send_keys(nationality)
        MARITAL_STATUS.send_keys(marital_status)
        BLOOD_TYPE.send_keys(blood_type)
        self.click_element(self.GENDER)
        
        Save_Button = self.find_elements(self.SAVE_BUTTON)
        SAVE_BUTTON_1 = Save_Button[0]
        SAVE_BUTTON_2 = Save_Button[1]
        SAVE_BUTTON_1.click()
        SAVE_BUTTON_2.click()
