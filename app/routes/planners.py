from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

from app.database.db import get_db_connection
from app.services.recommendation_service import (
    get_home_recommendations,
    get_party_recommendations,
    get_jewelry_recommendations
)

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


def save_history(request: Request, recommendation_type: str, input_data: str, recommendation: str):
    user_id = request.session.get("user_id")

    if not user_id:
        return

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO recommendation_history
        (user_id, recommendation_type, input_data, recommendation)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            recommendation_type,
            input_data,
            recommendation
        )
    )

    connection.commit()
    connection.close()


@router.post("/generate-home")
def generate_home(
    request: Request,
    room_type: str = Form(...),
    budget: float = Form(...),
    quantity: int = Form(...),
    preferences: str = Form("")
):
    result = get_home_recommendations(
        type(
            "HomeData",
            (),
            {
                "room_type": room_type,
                "budget": budget,
                "quantity": quantity,
                "preferences": preferences
            }
        )()
    )

    save_history(
        request,
        "Home Interior",
        f"Room: {room_type}, Budget: ₹{budget}, Quantity: {quantity}, Preferences: {preferences}",
        result
    )

    return templates.TemplateResponse(
        request=request,
        name="recommendation.html",
        context={
            "recommendation": result,
            "type": "Home Interior"
        }
    )


@router.post("/generate-party")
def generate_party(
    request: Request,
    budget: float = Form(...),
    guest_count: int = Form(...),
    event_type: str = Form(...),
    venue: str = Form("")
):
    result = get_party_recommendations(
        type(
            "PartyData",
            (),
            {
                "budget": budget,
                "guest_count": guest_count,
                "event_type": event_type,
                "venue": venue
            }
        )()
    )

    save_history(
        request,
        "Party Planning",
        f"Budget: ₹{budget}, Guests: {guest_count}, Event: {event_type}, Venue: {venue}",
        result
    )

    return templates.TemplateResponse(
        request=request,
        name="recommendation.html",
        context={
            "recommendation": result,
            "type": "Party Planning"
        }
    )


@router.post("/generate-jewelry")
def generate_jewelry(
    request: Request,
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form(...),
    outfit_description: str = Form("")
):
    result = get_jewelry_recommendations(
        type(
            "JewelryData",
            (),
            {
                "budget": budget,
                "occasion": occasion,
                "style": style,
                "outfit_description": outfit_description
            }
        )()
    )

    save_history(
        request,
        "Jewelry Recommendations",
        f"Budget: ₹{budget}, Occasion: {occasion}, Style: {style}, Outfit: {outfit_description}",
        result
    )

    return templates.TemplateResponse(
        request=request,
        name="recommendation.html",
        context={
            "recommendation": result,
            "type": "Jewelry Recommendations"
        }
    )