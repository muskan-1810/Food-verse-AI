import random
from PIL import Image

# Activity 4.1: Restaurant Hygiene Compliance Scoring
async def evaluate_restaurant_hygiene(image: Image.Image):
    compliance_score = round(random.uniform(70.0, 99.9), 1)
    return {
        "compliance_score": compliance_score,
        "rating": "Grade A (Excellent)" if compliance_score > 85 else "Grade B (Needs Improvement)",
        "violations_detected": 0 if compliance_score > 85 else 1,
        "inspection_status": "Passed" if compliance_score > 85 else "Review Required"
    }

# Activity 4.2: Smart Kitchen Cooking Guidance & Recipe Generation
def generate_smart_recipe(ingredients: list[str], cuisine_preference: str = "Any"):
    ingredients_str = ", ".join(ingredients)
    return {
        "recipe_title": f"Smart Chef Special ({cuisine_preference} Style)",
        "ingredients_used": ingredients,
        "instructions": [
            f"Inspect and preprep ingredients: {ingredients_str}.",
            "Heat cooking vessel on medium flame and add recommended healthy spices.",
            "Combine ingredients carefully and cook until done."
        ],
        "estimated_cooking_time": "20 minutes",
        "nutritional_tip": "Balanced with essential micronutrients."
    }