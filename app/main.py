from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.database.db import initialize_database
from app.routes.auth import router as auth_router
from app.routes.planners import router as planner_router
from app.routes.history import router as history_router


app = FastAPI(
    title="PocketSmart AI",
    description="Smart Budget & Recommendation Assistant",
    version="1.0.0"
)

templates = Jinja2Templates(directory="app/templates")


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.add_middleware(
    SessionMiddleware,
    secret_key="pocketsmart-secret-key-change-later"
)


initialize_database()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/dashboard")
def dashboard(request: Request):

    if not request.session.get("user_id"):
        from fastapi.responses import RedirectResponse
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )


@app.get("/home-planner")
def home_planner(request: Request):

    if not request.session.get("user_id"):
        from fastapi.responses import RedirectResponse
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="home_planner.html"
    )


@app.get("/party-planner")
def party_planner(request: Request):

    if not request.session.get("user_id"):
        from fastapi.responses import RedirectResponse
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="party_planner.html"
    )


@app.get("/jewelry-planner")
def jewelry_planner(request: Request):

    if not request.session.get("user_id"):
        from fastapi.responses import RedirectResponse
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="jewelry_planner.html"
    )


app.include_router(auth_router)
app.include_router(planner_router)
app.include_router(history_router)