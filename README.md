# LinkedIn Scraper API

This FastAPI-based project allows users to authenticate with LinkedIn using Selenium, fetch their connections using LinkedIn's Voyager API, and secure API endpoints with JWT authentication.

## Features
-  Secure authentication with JWT
-  Automated LinkedIn login using Selenium
-  Fetch LinkedIn connections via Voyager API
-  FastAPI-based RESTful API

## Prerequisites
Before running this project, ensure you have:
- Python 3.8+
- Google Chrome and ChromeDriver installed
- `pip install -r requirements.txt`
- LinkedIn credentials set in `.env`

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/linkedin-scraper.git
   cd linkedin-scraper
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your credentials:
   ```ini
   LINKEDIN_EMAIL=your-email@example.com
   LINKEDIN_PASSWORD=your-password
   SECRET_KEY=your-secret-key
   ```

## Running the API

Start the FastAPI application:
```sh
uvicorn main:app --reload
```

## API Endpoints

### 1️ Login
#### `POST /login`
Authenticates the user and returns a JWT token.

**Response:**
```json
{
  "access_token": "your-token",
  "token_type": "bearer"
}
```

### 2️ Fetch Connections
#### `GET /connections`
Fetches LinkedIn connections for the logged-in user.

**Headers:**
```sh
Authorization: Bearer <your-token>
```

**Query Parameters:**
- `page` (int, default=1): The page number.
- `count` (int, default=10): Number of connections per page.

**Response:**
```json
{
  "connections": [
    { "name": "John Doe", "profile_url": "https://www.linkedin.com/in/johndoe" }
  ]
}
```
### 3 Unit Testing

 
To run unit tests, use the following command:

python -m unittest test_scraper.py


## Troubleshooting
- Ensure your LinkedIn credentials are correct in `.env`.
- If LinkedIn blocks your request, try rotating user-agents in `scraper.py`.
- Ensure ChromeDriver is installed and matches your Chrome version.

 
