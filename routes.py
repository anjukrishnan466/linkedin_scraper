from fastapi import APIRouter, Depends, HTTPException
from .scraper import LinkedInScraper
from .auth import create_access_token, verify_token
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
scraper = LinkedInScraper()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    if request.email == os.getenv("LINKEDIN_EMAIL") and request.password == os.getenv("LINKEDIN_PASSWORD"):
        token = create_access_token({"sub": request.email})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/connections")
def get_connections(start: int = 0, count: int = 10, token: str = Depends(oauth2_scheme)):
    verify_token(token)
    return scraper.fetch_connections(start, count)
