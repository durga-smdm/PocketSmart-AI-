from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database.db import get_db_connection

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/history")
def history(request: Request):

    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    connection = get_db_connection()

    records = connection.execute(
        """
        SELECT *
        FROM recommendation_history
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "history": [dict(record) for record in records]
        }
    )