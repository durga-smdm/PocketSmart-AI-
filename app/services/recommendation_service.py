from app.services.gemini_service import generate_ai_recommendation


def get_home_recommendations(data):
    prompt = f"""
You are a smart home interior budget assistant.

Room type: {data.room_type}
Budget: ₹{data.budget}
Quantity: {data.quantity}
Preferences: {data.preferences}

Give practical recommendations within the user's budget.
Include:
1. Suggested items
2. Approximate budget allocation
3. Useful shopping suggestions
4. Short explanation for each recommendation
"""

    return generate_ai_recommendation(prompt)


def get_party_recommendations(data):
    prompt = f"""
You are a smart party budget planning assistant.

Total budget: ₹{data.budget}
Number of guests: {data.guest_count}
Event type: {data.event_type}
Venue: {data.venue}

Create a practical party budget plan.
Include:
1. Catering
2. Decoration
3. Entertainment
4. Venue-related expenses
5. Remaining budget
"""

    return generate_ai_recommendation(prompt)


def get_jewelry_recommendations(data):
    prompt = f"""
You are a smart jewelry recommendation assistant.

Budget: ₹{data.budget}
Occasion: {data.occasion}
Style preference: {data.style}
Outfit description: {data.outfit_description}

Suggest jewelry options suitable for the occasion and budget.
Include:
1. Jewelry type
2. Style suggestion
3. Approximate price range
4. Why it suits the occasion
"""

    return generate_ai_recommendation(prompt)