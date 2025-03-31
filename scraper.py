from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import random
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LOGIN_URL = "https://www.linkedin.com/login"
CONNECTIONS_API_URL = "https://www.linkedin.com/voyager/api/relationships/connections"

# User-Agent Rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.90 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.177 Safari/537.36"
]

class LinkedInScraper:
    def __init__(self):
        self.driver = None
        self.session_cookies = None

    def setup_driver(self):
        """Sets up Selenium WebDriver with anti-bot measures."""
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def login(self):
        """Logs into LinkedIn and stores session cookies."""
        self.setup_driver()
        self.driver.get(LOGIN_URL)
        time.sleep(random.uniform(2, 5))

        email_input = self.driver.find_element(By.ID, "username")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        email_input.send_keys(os.getenv("LINKEDIN_EMAIL"))
        time.sleep(random.uniform(1, 3))
        password_input.send_keys(os.getenv("LINKEDIN_PASSWORD"))
        time.sleep(random.uniform(1, 3))
        login_button.click()
        time.sleep(random.uniform(5, 8))

        self.session_cookies = {cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()}
        print("Session Cookies:", self.session_cookies)

        self.driver.quit()

    def get_headers(self):
        """Generates request headers with session cookies."""
        if not self.session_cookies:
            self.login()

        csrf_token = self.session_cookies.get("JSESSIONID", "").strip('"')
        li_at = self.session_cookies.get("li_at", "")

        if not li_at:
            raise Exception("Login failed or LinkedIn blocked the request.")

        headers = {
            "cookie": f"li_at={li_at}; " + "; ".join([f"{key}={value}" for key, value in self.session_cookies.items()]),
            "User-Agent": random.choice(USER_AGENTS),
            "Csrf-Token": csrf_token,
            "X-RestLi-Protocol-Version": "2.0.0",
            "Accept": "application/vnd.linkedin.normalized+json+2.1",
            "Referer": "https://www.linkedin.com/feed/",
        }
        return headers

    def fetch_connections(self, start=0, count=10):
        """Fetches LinkedIn connections using the Voyager API."""
        headers = self.get_headers()
        params = {"start": start, "count": count}

        response = requests.get(CONNECTIONS_API_URL, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        
        return {"error": f"Failed to fetch connections: {response.status_code}, {response.text}"}
