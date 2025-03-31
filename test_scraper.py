import unittest
from unittest.mock import patch, MagicMock
from scraper import LinkedInScraper  # Import your scraper file

class TestLinkedInScraper(unittest.TestCase):

    @patch("scraper.webdriver.Chrome")  # Mocking Selenium WebDriver
    def test_login(self, mock_chrome):
        """Test if login correctly stores session cookies."""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        # Mock elements
        mock_driver.find_element.return_value.send_keys = MagicMock()
        mock_driver.find_element.return_value.click = MagicMock()
        mock_driver.get_cookies.return_value = [
            {"name": "JSESSIONID", "value": "csrf-token-123"},
            {"name": "li_at", "value": "session-456"},
        ]

        scraper = LinkedInScraper()
        scraper.login()

        self.assertIn("JSESSIONID", scraper.session_cookies)
        self.assertIn("li_at", scraper.session_cookies)
        self.assertEqual(scraper.session_cookies["li_at"], "session-456")

    def test_get_headers(self):
        """Test if headers are generated properly."""
        scraper = LinkedInScraper()
        scraper.session_cookies = {"JSESSIONID": "csrf-token-123", "li_at": "session-456"}

        headers = scraper.get_headers()

        self.assertIn("cookie", headers)
        self.assertIn("User-Agent", headers)
        self.assertIn("Csrf-Token", headers)
        self.assertEqual(headers["Csrf-Token"], "csrf-token-123")

    @patch("scraper.requests.get")
    def test_fetch_connections(self, mock_get):
        """Test if fetch_connections correctly fetches mock data."""
        scraper = LinkedInScraper()
        scraper.session_cookies = {"JSESSIONID": "csrf-token-123", "li_at": "session-456"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"connections": ["User1", "User2"]}
        mock_get.return_value = mock_response

        result = scraper.fetch_connections(start=0, count=2)

        self.assertEqual(result, {"connections": ["User1", "User2"]})
        mock_get.assert_called_once()

if __name__ == "__main__":
    unittest.main()
