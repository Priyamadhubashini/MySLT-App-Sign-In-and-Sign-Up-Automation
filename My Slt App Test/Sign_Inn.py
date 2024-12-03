import time
import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Test data for login scenarios
test_data = [
    {'user_id': '0703270241', 'password': '1488Lap28', 'reason': 'Valid credentials'},
    {'user_id': '0703270241', 'password': 'wrongpassword', 'reason': 'Invalid password'},
    {'user_id': 'invaliduser@gmail.com', 'password': '1488Lap28', 'reason': 'Invalid username'},
    {'user_id': '', 'password': '1488Lap28', 'reason': 'Empty username'},
    {'user_id': '0703270241', 'password': '', 'reason': 'Empty password'},
    {'user_id': '', 'password': '', 'reason': 'Empty credentials'},
    {'user_id': '0703270241@#$', 'password': '1488Lap28', 'reason': 'Special characters in username'},
    {'user_id': '0' * 51, 'password': '1488Lap28', 'reason': 'Username too long'},
    {'user_id': '0703270241', 'password': 'p' * 51, 'reason': 'Password too long'},
    {'user_id': 'username_without_digits', 'password': '1488Lap28', 'reason': 'Invalid username format'}
]

# Fixture for the driver
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("https://myslt.slt.lk/")
    yield driver
    time.sleep(2)
    driver.quit()

# Function to log in
def login(driver, user_id, password):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                    '#root > div > div.formView > div.form.d-block.m-auto.login-form > div.input-group > div:nth-child(1) > input[type="text"]'))).send_keys(
        user_id)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                    '#root > div > div.formView > div.form.d-block.m-auto.login-form > div.input-group > div:nth-child(2) > input[type="password"]'))).send_keys(
        password)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                    '#root > div > div.formView > div.form.d-block.m-auto.login-form > div.input-container-footer > button'))).click()

# Helper to get error message
def get_error_message(driver):
    error_messages = []
    try:
        user_id_error = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[1]/span')
        ))
        error_messages.append(user_id_error.text)
    except TimeoutException:
        pass

    try:
        password_error = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/span')
        ))
        error_messages.append(password_error.text)
    except TimeoutException:
        pass

    try:
        login_error = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]')
        ))
        error_messages.append(login_error.text)
    except TimeoutException:
        pass

    print("All error messages found:", error_messages)
    return " & ".join(error_messages) if error_messages else ""

# Tests
def test_valid_login(driver):
    login(driver, test_data[0]['user_id'], test_data[0]['password'])
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#root > div > nav > div > img")
        ))
        print("Successfully logged in.")
    except TimeoutException:
        print("Login failed: Not redirected to home page.")
        assert False, "Login failed with valid credentials."

def test_invalid_password(driver):
    login(driver, test_data[1]['user_id'], test_data[1]['password'])
    error_text = get_error_message(driver)
    assert error_text in ["Invalid user name and password", "Enter valid email or mobile"]

def test_invalid_username(driver):
    login(driver, test_data[2]['user_id'], test_data[2]['password'])
    error_text = get_error_message(driver)
    assert error_text in ["Invalid user name and password", "Enter valid email or mobile"]

def test_empty_username(driver):
    login(driver, test_data[3]['user_id'], test_data[3]['password'])
    error_text = get_error_message(driver)
    assert error_text in ["User ID cannot be empty", "Enter valid email or mobile"]

def test_empty_password(driver):
    login(driver, test_data[4]['user_id'], test_data[4]['password'])
    error_text = get_error_message(driver)
    assert error_text == "Minimum 6 characters"

def test_empty_credentials(driver):
    login(driver, test_data[5]['user_id'], test_data[5]['password'])
    error_text = get_error_message(driver)
    assert "User ID cannot be empty" in error_text or "Minimum 6 characters" in error_text

# Additional test cases with flexible error message validation
def test_special_characters_in_username(driver):
    login(driver, test_data[6]['user_id'], test_data[6]['password'])
    error_text = get_error_message(driver)
    assert error_text in ["Invalid user name and password", "Enter valid email or mobile"]

def test_username_too_long(driver):
    login(driver, test_data[7]['user_id'], test_data[7]['password'])
    error_text = get_error_message(driver)
    assert error_text in ["Username is too long", "Invalid user name and password", "Enter valid email or mobile"]

def test_password_too_long(driver):
    login(driver, test_data[8]['user_id'], test_data[8]['password'])
    error_text = get_error_message(driver)
    assert error_text == "Invalid user name and password"

def test_username_format_invalid(driver):
    login(driver, test_data[9]['user_id'], test_data[9]['password'])
    error_text = get_error_message(driver)
    assert error_text in ["Invalid user name format", "Enter valid email or mobile"]
