import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_create_article(browser):
    browser.get('http://localhost:8000/')
    username_input = WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div > div > div > div.col-sm-4 > div:nth-child(2) > input'))
    )
    username_input.send_keys('test')
    password_input = WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div > div > div > div.col-sm-4 > div:nth-child(3) > input'))
    )
    password_input.send_keys('test1234')
    login_button = WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div[3]/div/button[1]'))
    )
    login_button.click()
    time.sleep(20)

    # browser.get('http://localhost:8000/admin/core/article/add/')
    # title_input = WebDriverWait(browser, 10).until(
    #     EC.presence_of_element_located((By.NAME, 'title'))
    # )
    # title_input.send_keys('Test Article')
    # description_input = WebDriverWait(browser, 10).until(
    #     EC.presence_of_element_located((By.NAME, 'description'))
    # )
    # description_input.send_keys('This is a test article')
    # browser.find_element(By.XPATH, '//input[@name="_save"]').click()

    # WebDriverWait(browser, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//li[contains(text(), "Test Article")]'))
    # )

