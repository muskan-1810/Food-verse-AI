import random
from pydantic import BaseModel
from backend.smart_kitchen import evaluate_restaurant_hygiene, generate_smart_recipe
from backend.extra_features import router as extra_features_router
from backend.freshness_detector import detect_food_freshness
from backend.nutrition import get_nutrition
from fastapi import FastAPI, UploadFile, File
from PIL import Image
from io import BytesIO
import random
from pydantic import BaseModel

from backend.food_recognition import recognize_food


app = FastAPI(title="Food-Verse AI")
class KitchenRequest(BaseModel):
    ingredients: list[str]
    cuisine_preference: str = "Any"
app.include_router(extra_features_router)

class KitchenRequest(BaseModel, extra='allow'):
    ingredients: list[str]
    cuisine_preference: str = "Any"

@app.get("/")
def home():
    return {
        "message": "Food-Verse AI Backend is running!",
        "status": "success"
    }


@app.post("/recognize-food")
async def recognize_food_api(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(BytesIO(image_data)).convert("RGB")

    results = recognize_food(image)
    top_food = results[0]["food"]
    nutrition = get_nutrition(top_food)
    
    return {
        "filename": file.filename,
        "food": top_food,
        "confidence": results[0]["confidence"],
        "nutrition": nutrition,
        "other_predictions": results[1:]
    }


@app.post("/detect-freshness")
async def detect_freshness_api(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(BytesIO(image_data)).convert("RGB")

    result = await detect_food_freshness(image)

    return {
        "filename": file.filename,
        "freshness_analysis": result
    }

# --- Epic 4: Restaurant Hygiene & Smart Kitchen Modules ---
@app.post("/api/hygiene/score")
async def evaluate_hygiene(file: UploadFile = File(...)):
    compliance_score = round(random.uniform(70.0, 99.9), 1)
    return {
        "filename": file.filename,
        "compliance_score": compliance_score,
        "rating": "Grade A" if compliance_score > 85 else "Grade B (Needs Improvement)",
        "violations_detected": 0 if compliance_score > 85 else 1
    }

@app.post("/api/kitchen/recipe")
async def generate_recipe(data: KitchenRequest):
    ingredients_str = ", ".join(data.ingredients)
    return {
        "recipe_title": f"Smart Chef Special with {data.cuisine_preference} style",
        "ingredients_used": data.ingredients,
        "instructions": [
            f"Preprep and clean the ingredients: {ingredients_str}.",
            "Heat pan with medium flame and add preferred seasoning.",
            "Combine ingredients, cook evenly, and serve hot."
        ],
        "estimated_cooking_time": "20 minutes"
    }

# --- Epic 4: Restaurant Hygiene & Smart Kitchen Modules ---
@app.post("/api/hygiene/score")
async def hygiene_score_api(file: UploadFile = File(...)):
    image = Image.open(BytesIO(await file.read())).convert("RGB")
    result = await evaluate_restaurant_hygiene(image)
    return {"filename": file.filename, "hygiene_analysis": result}

@app.post("/api/kitchen/recipe")
async def smart_recipe_api(data: KitchenRequest):
    result = generate_smart_recipe(data.ingredients, data.cuisine_preference)
    return result

from backend.meal_planner import generate_personalized_meal_plan

class UserProfileRequest(BaseModel):
    goal: str = "General Fitness"
    preference: str = "Balanced"
    target_calories: int = 2000

@app.post("/api/meal-plan/generate")
async def generate_meal_plan_api(data: UserProfileRequest):
    result = generate_personalized_meal_plan(data.dict())
    return result