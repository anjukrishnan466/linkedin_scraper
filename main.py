from fastapi import FastAPI, Depends, HTTPException
from scraper import LinkedInScraper
from auth import create_access_token, verify_token
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.post("/login")
def login():
    """Authenticates the user and returns a JWT token."""
    user_email = os.getenv("LINKEDIN_EMAIL")
    user_password = os.getenv("LINKEDIN_PASSWORD")

    if not user_email or not user_password:
        raise HTTPException(status_code=401, detail="Invalid LinkedIn credentials")

    access_token = create_access_token({"sub": user_email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/connections")
def get_connections(page: int = 1, count: int = 10, user: dict = Depends(verify_token)):
    """Fetches LinkedIn connections for the logged-in user."""
    scraper = LinkedInScraper()
    start = (page - 1) * count
    return scraper.fetch_connections(start=start, count=count)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
