from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database.db import get_db_connection
from app.core.security import hash_password, verify_password


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


# =========================
# REGISTER PAGE
# =========================

@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )


# =========================
# REGISTER USER
# =========================

@router.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    connection = get_db_connection()

    existing_user = connection.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    if existing_user:
        connection.close()
        return {"error": "Email already registered"}

    hashed_password = hash_password(password)

    connection.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username, email, hashed_password)
    )

    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/login",
        status_code=303
    )


# =========================
# LOGIN PAGE
# =========================

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


# =========================
# LOGIN USER
# =========================

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    connection = get_db_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    connection.close()

    if not user or not verify_password(password, user["password"]):
        return {"error": "Invalid email or password"}

    request.session["user_id"] = user["id"]
    request.session["username"] = user["username"]

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )


# =========================
# LOGOUT
# =========================

@router.get("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303
    )