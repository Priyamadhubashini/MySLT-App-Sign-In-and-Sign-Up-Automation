import time
import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Test data for registration (Updated with your details)
test_data = [
    {'user_id': '0703270241', 'name': 'Priya', 'password': '1488Lap28'},  # Your details
    {'user_id': '07699151622', 'name': 'Priya', 'password': '1488Lap28'},  # Invalid Mobile
    {'user_id': '0703270241', 'name': '', 'password': '1488Lap28'},  # Name cannot be empty
    {'user_id': '', 'name': 'Priya', 'password': '1488Lap28'},  # User ID cannot be empty
    {'user_id': '0703270241', 'name': 'Priya', 'password': ''},  # Minimum 6 characters
    {'user_id': '0703270241', 'name': 'P', 'password': '9971'},  # Name too short, password too short
    {'user_id': '', 'name': '', 'password': ''}  # All fields empty
]

# Fixture for the driver
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("https://myslt.slt.lk/")
    yield driver
    time.sleep(2)
    driver.quit()

# Function to register
def register(driver, user_id, name, password):
    # Click the "Register" link
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             '#root > div > div.formView > div.form.d-block.m-auto.login-form > div.register-container > a'))
    ).click()

    # Fill out the registration form
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        '#root > div > div.formView > div:nth-child(2) > div > div.input-group > div:nth-child(1) > input'))
    ).send_keys(user_id)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        '#root > div > div.formView > div:nth-child(2) > div > div.input-group > div:nth-child(2) > input'))
    ).send_keys(name)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        '#root > div > div.formView > div:nth-child(2) > div > div.input-group > div:nth-child(3) > input'))
    ).send_keys(password)

    # Click the "Register" button
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#sign'))
    ).click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#root > div > div.formView > div:nth-child(2) > div > div.mt-4.clearfix > button'))
    ).click()

# Test case to verify re-registration message
def test_valid_reregister(driver):
    register(driver, test_data[0]['user_id'], test_data[0]['name'], test_data[0]['password'])
    # Verify re-registration message
    expected_text = "User is already registered"
    try:
        disable_report_text1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]'))
        )
        assert expected_text in disable_report_text1.text
        print("Test passed: 'User is already registered' error displayed successfully.")
    except TimeoutException:
        assert False, "Oops! Something went wrong."

def test_invaliduserid_register(driver):
    register(driver, test_data[1]['user_id'], test_data[1]['name'], test_data[1]['password'])
    # Verify re-registration message
    expected_text = "Invalid Mobile"
    try:
        disable_report_text1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]'))
        )
        assert expected_text in disable_report_text1.text
        print("Test passed: 'Invalid Mobile' displayed successfully.")
    except TimeoutException:
        assert False, "Oops! Something went wrong."

def test_emptyname_register(driver):
    register(driver, test_data[2]['user_id'], test_data[2]['name'], test_data[2]['password'])
    # Verify re-registration message
    expected_text = "Name cannot be empty"
    try:
        disable_report_text1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div[2]/span'))
        )
        assert expected_text in disable_report_text1.text
        print("Test passed: 'Name cannot be empty' displayed successfully.")
    except TimeoutException:
        assert False, "Oops! Something went wrong."

def test_emptuserid_register(driver):
    register(driver, test_data[3]['user_id'], test_data[3]['name'], test_data[3]['password'])
    # Verify re-registration message
    expected_text = "User ID cannot be empty"
    try:
        disable_report_text1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div[1]/span'))
        )
        assert expected_text in disable_report_text1.text
        print("Test passed: 'User ID cannot be empty' displayed successfully.")
    except TimeoutException:
        assert False, "Oops! Something went wrong."


def test_emptypass_register(driver):
    register(driver, test_data[4]['user_id'], test_data[4]['name'], test_data[4]['password'])
    # Verify re-registration message
    expected_text = "Minimum 6 characters"
    try:
        disable_report_text1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div[3]/span'))
        )
        assert expected_text in disable_report_text1.text
        print("Test passed: 'Minimum 6 characters' displayed successfully.")
    except TimeoutException:
        assert False, "Oops! Something went wrong."


def test_reducepass_register(driver):
    register(driver, test_data[5]['user_id'], test_data[5]['name'], test_data[5]['password'])
    # Verify re-registration message
    expected_text = "Minimum 6 characters"
    try:
        disable_report_text1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div[3]/span'))
        )
        assert expected_text in disable_report_text1.text
        print("Test passed: 'Minimum 6 characters' displayed successfully.")
    except TimeoutException:
        assert False, "Oops! Something went wrong"