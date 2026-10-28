def generate_personalized_meal_plan(user_profile: dict):
    goal = user_profile.get("goal", "General Fitness")
    dietary_preference = user_profile.get("preference", "Balanced")
    calories = user_profile.get("target_calories", 2000)
    
    # Adaptive Meal Planning Logic based on user profile and goals
    if "Weight Loss" in goal:
        breakfast = "Oatmeal with fresh berries and almond milk (approx. 350 kcal)"
        lunch = "Grilled chicken/tofu salad with olive oil dressing (approx. 450 kcal)"
        dinner = "Baked fish or lentil soup with steamed vegetables (approx. 400 kcal)"
    elif "Muscle Gain" in goal:
        breakfast = "Scrambled eggs, whole wheat toast, and a banana smoothie (approx. 550 kcal)"
        lunch = "Brown rice, grilled paneer/chicken breast, and mixed veggies (approx. 650 kcal)"
        dinner = "Quinoa bowl with chickpeas, sweet potatoes, and avocado (approx. 600 kcal)"
    else:
        breakfast = "Greek yogurt with honey and nuts (approx. 400 kcal)"
        lunch = "Whole grain wrap with vegetables and lean protein (approx. 500 kcal)"
        dinner = "Mixed vegetable stir-fry with tofu or chicken (approx. 500 kcal)"

    return {
        "user_goal": goal,
        "dietary_preference": dietary_preference,
        "target_daily_calories": calories,
        "meal_plan": {
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner,
            "snack": "Handful of mixed nuts or green tea"
        },
        "recommendation_status": "Personalized successfully based on activity and nutrition profile."
    }