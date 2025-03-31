from fastapi import FastAPI
from auth import get_logged_in_user  # ✅ Import from auth
from scraper import get_connections  # ✅ Import from scraper
from pydantic import BaseModel  # ✅ Import BaseModel
app = FastAPI()

 
class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/login")
def login_user(login_request: LoginRequest):
    try:
        scraper_instance.login(login_request.email, login_request.password)
        token = create_access_token({"email": login_request.email})
        return {"message": "Login successful", "access_token": token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/connections")
def connections(page: int = 1, count: int = 10):
    return get_connections(page, count)
