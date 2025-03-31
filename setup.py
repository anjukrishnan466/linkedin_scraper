import os

# Define the folder structure
folders = [
    "linkedin_scraper_test",
    "linkedin_scraper_test/tests"
]

# Define the files and their initial content
files = {
    "linkedin_scraper_test/main.py": "# Entry point for the application\n",
    "linkedin_scraper_test/config.py": "# Configuration settings (load from .env)\n",
    "linkedin_scraper_test/auth.py": "# Handles LinkedIn login and session management\n",
    "linkedin_scraper_test/scraper.py": "# Scrapes LinkedIn connections using Voyager API\n",
    "linkedin_scraper_test/utils.py": "# Helper functions (e.g., request handling, anti-bot detection)\n",
    "linkedin_scraper_test/requirements.txt": "# Dependencies list (Selenium, Requests, etc.)\n",
    "linkedin_scraper_test/.env": "# Environment variables (LinkedIn credentials)\n",
    "linkedin_scraper_test/tests/test_auth.py": "# Tests for authentication module\n",
    "linkedin_scraper_test/tests/test_scraper.py": "# Tests for scraper module\n",
    "linkedin_scraper_test/README.md": "# Project documentation\n",
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for file, content in files.items():
    with open(file, "w") as f:
        f.write(content)

print("✅ Project structure created successfully!")
