from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv
import requests

load_dotenv()

LOGIN_URL = "https://www.linkedin.com/login"
CONNECTIONS_API_URL = "https://www.linkedin.com/voyager/api/voyagerIdentityDashConnections"

class LinkedInScraper:
    def __init__(self):
        self.driver = None
        self.session_cookies = None

    def login(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(LOGIN_URL)
        time.sleep(2)

        email_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        email_input.send_keys(os.getenv("LINKEDIN_EMAIL"))
        password_input.send_keys(os.getenv("LINKEDIN_PASSWORD"))
        login_button.click()
        time.sleep(5)

        self.session_cookies = {cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()}
        self.driver.quit()
    
    def get_headers(self):
        if not self.session_cookies:
            self.login()
        return {"cookie": "; ".join([f"{key}={value}" for key, value in self.session_cookies.items()])}

    def fetch_connections(self, start=0, count=10):
        headers = self.get_headers()
        params = {"start": start, "count": count}

        response = requests.get(CONNECTIONS_API_URL, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        return {"error": "Failed to fetch connections"}

# ✅ Add a function to call the scraper class
def get_connections(page: int = 1, count: int = 10):
    scraper = LinkedInScraper()
    start = (page - 1) * count
    return scraper.fetch_connections(start=start, count=count)
