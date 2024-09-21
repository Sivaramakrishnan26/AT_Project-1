from pages.login_page import LoginPage
from pages.pim_2_edit_page import PimEditPage
from datetime import datetime
from conftest import setup
import pandas as pd
import pytest
import os


def get_edit_data():  # Method to get the Employee Data from the Excel sheet to edit an existing employee
    edit_data = []
    # Read the Excel file into a DataFrame
    df = pd.read_excel('pim_2_edit_data.xlsx', 'PIM_EDIT')  # Update the path to your Excel file if needed
    df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
    print(df.columns)

    # Iterate through the rows of the DataFrame and extract username and password
    for index, row in df.iterrows():
        login_username = row['LOGIN USERNAME']
        login_password = row['LOGIN PASSWORD']

        employee_name = row['EMPLOYEE NAME']

        first_name = row['FIRST NAME']
        middle_name = row['MIDDLE NAME']
        last_name = row['LAST NAME']
        dl_number = row['DL NUMBER']
        dl_exp_date = row['DL EXP DATE']
        nationality = row['NATIONALITY']
        marital_status = row['MARITAL STATUS']
        date_of_birth = row['DATE OF BIRTH']
        blood_type = row['BLOOD TYPE']
        test = row['TEST']

        edit_data.append((login_username, login_password, employee_name, first_name, middle_name, last_name, dl_number, dl_exp_date, nationality, marital_status, date_of_birth, blood_type, test))

    return edit_data


def update_excel(login_username, login_password, employee_name, first_name, middle_name, last_name, dl_number, dl_exp_date, nationality, marital_status, date_of_birth, blood_type, test, test_result, tester_name):  # Method to update the status in the Excel sheet
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    file_path = 'pim_2_edit_data.xlsx'
    temp_file_path = 'pim_2_edit_data_temp.xlsx'

    try:
        df = pd.read_excel(file_path, engine='openpyxl')  # Load the existing Excel file into a DataFrame
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return

    # Ensure necessary columns are present and of type string
    for col in ["DATE", "TIME OF TEST", "NAME OF TESTER", "TEST RESULT"]:
        if col not in df.columns:
            df[col] = ""  # Add missing columns with empty strings

    df["DATE"] = df["DATE"].astype(str)
    df["TIME OF TEST"] = df["TIME OF TEST"].astype(str)
    df["NAME OF TESTER"] = df["NAME OF TESTER"].astype(str)
    df["TEST RESULT"] = df["TEST RESULT"].astype(str)

    # Update the DataFrame with the test result for the matching username and password
    record_found = False
    for index, row in df.iterrows():
        if row["LOGIN USERNAME"] == login_username and row["LOGIN PASSWORD"] == login_password and row['EMPLOYEE NAME'] == employee_name and row['FIRST NAME'] == first_name and row['MIDDLE NAME'] == middle_name and row['LAST NAME'] == last_name and row['DL NUMBER'] == dl_number and row['DL EXP DATE'] == dl_exp_date and row['NATIONALITY'] == nationality and row['MARITAL STATUS'] == marital_status and row['DATE OF BIRTH'] == date_of_birth and row['BLOOD TYPE'] == blood_type and row['TEST'] == test:
            df.at[index, "DATE"] = current_date
            df.at[index, "TIME OF TEST"] = current_time
            df.at[index, "NAME OF TESTER"] = tester_name
            df.at[index, "TEST RESULT"] = test_result
            record_found = True
            break

    if not record_found:
        print(f"No matching record found for username: {login_username} and password: {login_password}")
        return

    try:
        # Save the updated DataFrame to a temporary file
        with pd.ExcelWriter(temp_file_path, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False, sheet_name='PIM_EDIT')

        os.replace(temp_file_path, file_path)  # Replace the original file with the temporary file
    except Exception as e:
        print(f"Error writing to the Excel file: {e}")
        # Optionally, handle the temporary file cleanup here
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@pytest.mark.usefixtures("setup")
class TestPimEdit:
    @pytest.mark.parametrize("login_username, login_password, employee_name, first_name, middle_name, last_name, dl_number, dl_exp_date, nationality, marital_status, date_of_birth, blood_type, test", get_edit_data())
    def test_add(self, setup, login_username, login_password, employee_name, first_name, middle_name, last_name, dl_number, dl_exp_date, nationality, marital_status, date_of_birth, blood_type, test):
        login_page = LoginPage(self.driver)
        login_page.login(login_username, login_password)

        pim_page = PimEditPage(self.driver)
        pim_page.edit_user(employee_name, first_name, middle_name, last_name, dl_number, dl_exp_date, nationality, marital_status, date_of_birth, blood_type, test)

        # Replace 'Tester_Name' with the actual tester's name or get it dynamically
        tester_name = "Sivaramakrishnan T"

        # Check if the employee details was edited successful by verifying the presence of 'viewPersonalDetails' in the URL
        if "viewPersonalDetails" in self.driver.current_url:
            update_excel(login_username, login_password, employee_name, first_name, middle_name, last_name, dl_number, dl_exp_date, nationality, marital_status, date_of_birth, blood_type, test, "Passed", tester_name)
            print("Employee Edited Successfully")
        else:
            update_excel(login_username, login_password, employee_name, first_name, middle_name, last_name, dl_number, dl_exp_date, nationality, marital_status, date_of_birth, blood_type, test, "Failed", tester_name)
            print("Failed to Edit Employee")
