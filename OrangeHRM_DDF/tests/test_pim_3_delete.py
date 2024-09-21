from pages.login_page import LoginPage
from pages.pim_3_delete_page import PimDeletePage
from datetime import datetime
from conftest import setup
import pandas as pd
import pytest
import os


def get_delete_data():  # Method to get the Employee Data from the Excel sheet to delete an existing employee
    delete_data = []
    # Read the Excel file into a DataFrame
    df = pd.read_excel('pim_3_delete_data.xlsx', 'PIM_DELETE')  # Update the path to your Excel file if needed
    df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
    print(df.columns)

    # Iterate through the rows of the DataFrame and extract username and password
    for index, row in df.iterrows():
        login_username = row['LOGIN USERNAME']
        login_password = row['LOGIN PASSWORD']
        employee_name = row['EMPLOYEE NAME']

        delete_data.append((login_username, login_password, employee_name))

    return delete_data


def update_excel(login_username, login_password, employee_name, test_result, tester_name):  # Method to update the status in the Excel sheet
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    file_path = 'pim_3_delete_data.xlsx'
    temp_file_path = 'pim_3_delete_data_temp.xlsx'

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
        if row["LOGIN USERNAME"] == login_username and row["LOGIN PASSWORD"] == login_password and row['EMPLOYEE NAME'] == employee_name:
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
            df.to_excel(writer, index=False, sheet_name='PIM_DELETE')

        os.replace(temp_file_path, file_path)  # Replace the original file with the temporary file
    except Exception as e:
        print(f"Error writing to the Excel file: {e}")
        # Optionally, handle the temporary file cleanup here
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@pytest.mark.usefixtures("setup")
class TestPimDelete:
    @pytest.mark.parametrize("login_username, login_password, employee_name", get_delete_data())
    def test_delete(self, setup, login_username, login_password, employee_name):
        login_page = LoginPage(self.driver)
        login_page.login(login_username, login_password)

        pim_page = PimDeletePage(self.driver)
        pim_page.delete_user(employee_name)

        # Replace 'Tester_Name' with the actual tester's name or get it dynamically
        tester_name = "Sivaramakrishnan T"

        # Check if the employee was deleted successful
        if "viewEmployeeList" in self.driver.current_url:
            update_excel(login_username, login_password, employee_name, "Passed", tester_name)
            print("Employee Deleted Successfully")
        else:
            update_excel(login_username, login_password, employee_name, "Failed", tester_name)
            print("Failed to Delete Employee")
