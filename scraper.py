from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

LOGIN_URL = "https://www.linkedin.com/login"
CONNECTIONS_API_URL = "https://www.linkedin.com/voyager/api/relationships/connections"  # Verify this in DevTools

class LinkedInScraper:
    def __init__(self):
        self.driver = None
        self.session_cookies = None

    def login(self):
        """Logs in to LinkedIn and stores session cookies."""
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

        # Save session cookies
        self.session_cookies = {cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()}
        print(" Session Cookies:", self.session_cookies)  # Debugging

        self.driver.quit()
    
    def get_headers(self):
        """Generates headers for API requests using session cookies."""
        if not self.session_cookies:
            self.login()

        csrf_token = self.session_cookies.get("JSESSIONID", "").strip('"')
        li_at = self.session_cookies.get("li_at", "")

        if not li_at:
            raise Exception("❌ Error: 'li_at' cookie is missing. Login failed or LinkedIn blocked the request.")

        headers = {
            "cookie": f"li_at={li_at}; " + "; ".join([f"{key}={value}" for key, value in self.session_cookies.items()]),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Csrf-Token": csrf_token,
            "X-RestLi-Protocol-Version": "2.0.0",
            "Accept": "application/vnd.linkedin.normalized+json+2.1",
            "Referer": "https://www.linkedin.com/feed/",
        }
        
        # print(" Request Headers:", headers)  # Debugging
        return headers

    def fetch_connections(self, start=0, count=10):
        """Fetches LinkedIn connections."""
        headers = self.get_headers()
        params = {"start": start, "count": count}

        response = requests.get(CONNECTIONS_API_URL, headers=headers, params=params)

        # print(f" Response Status Code: {response.status_code}")
        # print(f" Response Headers: {response.headers}")  
        # print(f" Response Content: {response.text}")  

        if response.status_code == 200:
            return response.json()
        
        return {"error": f"Failed to fetch connections: {response.status_code}, {response.text}"}

# ✅ Function to fetch connections
def get_connections(page: int = 1, count: int = 10):
    scraper = LinkedInScraper()
    start = (page - 1) * count
    return scraper.fetch_connections(start=start, count=count)

#  Run the script
if __name__ == "__main__":
    print(get_connections(page=1, count=10))
