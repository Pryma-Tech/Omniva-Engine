"""Authentication routes (placeholder)."""
# TODO: Add password hashing, DB storage, secure cookies.

from fastapi import APIRouter, Form, Request, Response
from fastapi.templating import Jinja2Templates

from auth.session_manager import session_manager


router = APIRouter()
templates = Jinja2Templates(directory="dashboard/pages")


@router.get("/login")
async def login_page(request: Request):
    """Render placeholder login form."""
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def perform_login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    """Create placeholder session."""
    # TODO: Validate against stored credentials
    token = session_manager.create_session(username)
    response.set_cookie(key="session_token", value=token)
    return {"status": "logged in (placeholder)", "token": token}


@router.get("/logout")
async def logout(request: Request, response: Response):
    """Destroy placeholder session."""
    token = request.cookies.get("session_token")
    if token:
        session_manager.delete_session(token)
    response.delete_cookie("session_token")
    return {"status": "logged out (placeholder)"}
