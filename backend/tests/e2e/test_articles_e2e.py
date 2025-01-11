import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

class TestCreateArticle:
    def setup_method(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        # self.driver = webdriver.Remote(
        #     command_executor='http://localhost:4444/wd/hub',
        #     options=chrome_options
        # )
        self.driver.implicitly_wait(10)  # Set implicit wait to speed up tests

    def teardown_method(self):
        self.driver.quit()

    def test_create_article(self):
        self.driver.get('http://localhost:8000/')
        self._login()

        post_title = 'Test Post Title'
        post_description = 'This is a test post description'
        self._create_article(post_title, post_description)

        post_header = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//h1[contains(text(), "{post_title}")]'))
        )

        post_description_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//p[contains(text(), "{post_description}")]'))
        )

        assert post_title in post_header.text
        assert post_description in post_description_element.text

        time.sleep(3)  # Make test slower

        self._logout()

    def test_create_multiple_articles(self):
        self.driver.get('http://localhost:8000/')
        self._login()

        articles = [
            {'title': 'First Test Post', 'description': 'This is the first test post description'},
            {'title': 'Second Test Post', 'description': 'This is the second test post description'},
        ]

        for article in articles:
            self._create_article(article['title'], article['description'])

            post_header = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//h1[contains(text(), "{article["title"]}")]'))
            )

            post_description_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//p[contains(text(), "{article["description"]}")]'))
            )

            assert article['title'] in post_header.text
            assert article['description'] in post_description_element.text

            time.sleep(1)  # Make test slower

        self._logout()

    def test_edit_post(self):
        self.driver.get('http://localhost:8000/')
        self._login()

        post_title = 'Test Post Title'
        post_description = 'This is a test post description'
        self._create_article(post_title, post_description)

        post_header = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//h1[contains(text(), "{post_title}")]'))
        )

        post_description_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//p[contains(text(), "{post_description}")]'))
        )

        edit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Update"]'))
        )
        edit_button.click()

        title_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Enter Post Title"]'))
        )
        title_input.clear()
        title_input.send_keys('Edited Test Post Title')

        description_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Enter Post Description"]'))
        )
        description_input.clear()
        description_input.send_keys('This is the edited test post description')

        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "btn-success") and text()="Update"]'))
        )
        submit_button.click()

        post_header = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//h1[contains(text(), "Edited Test Post Title")]'))
        )

        post_description_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//p[contains(text(), "This is the edited test post description")]'))
        )

        assert 'Edited Test Post Title' in post_header.text
        assert 'This is the edited test post description' in post_description_element.text

        time.sleep(3)  # Make test slower

        self._logout()

    def test_delete_added_article(self):
        self.driver.get('http://localhost:8000/')
        self._login()

        post_title = 'Test Post Title'
        post_description = 'This is a test post description'
        self._create_article(post_title, post_description)

        post_header = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//h1[contains(text(), "{post_title}")]'))
        )

        delete_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "btn-danger") and text()="Delete"]'))
        )
        delete_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element(post_header)
        )

        assert 'Test Post Title' not in self.driver.page_source

        time.sleep(3)  # Make test slower

        self._logout()

    def _login(self):
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div > div > div > div.col-sm-4 > div:nth-child(2) > input'))
        )
        username_input.send_keys('test')
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div > div > div > div.col-sm-4 > div:nth-child(3) > input'))
        )
        password_input.send_keys('test1234')
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div[3]/div/button[1]'))
        )
        login_button.click()

    def _create_article(self, post_title, post_description):
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Create Post"]'))
        )
        submit_button.click()

        title_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Enter Post Title"]'))
        )
        title_input.send_keys(post_title)

        description_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Enter Post Description"]'))
        )
        description_input.send_keys(post_description)

        save_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Post"]'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
        save_button.click()

    def _logout(self):
        logout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Log out"]'))
        )
        logout_button.click()

