from transformers import pipeline

_food_classifier = None


def recognize_food(image):
    global _food_classifier

    if _food_classifier is None:
        _food_classifier = pipeline(
            "image-classification",
            model="nateraw/food"
        )

    results = _food_classifier(image)

    return [
        {
            "food": result["label"],
            "confidence": round(result["score"] * 100, 2)
        }
        for result in results[:5]
    ]