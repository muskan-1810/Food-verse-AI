import os
import json
import asyncio
import numpy as np
from dotenv import load_dotenv


from google import genai
from PIL import Image, ImageOps

from pathlib import Path



load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


def preprocess_image(image: Image.Image):
    """Standardize the image and extract basic visual statistics."""

    image = ImageOps.exif_transpose(image)
    image = image.convert("RGB")
    image.thumbnail((1024, 1024))

    pixels = np.asarray(image, dtype=np.float32)

    features = {
        "width": image.width,
        "height": image.height,
        "mean_rgb": [
            round(float(value), 2)
            for value in pixels.mean(axis=(0, 1))
        ],
        "brightness": round(float(pixels.mean()), 2),
        "contrast": round(float(pixels.std()), 2),
    }

    return image, features


async def detect_food_freshness(image: Image.Image):
    """Analyze visible food freshness indicators using Gemini."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "item_name": "Unknown",
            "freshness_level": "Unable to determine",
            "confidence": 0,
            "visible_observations": [],
            "recommendation": "GEMINI_API_KEY is not configured.",
        }

    try:
        processed_image, features = preprocess_image(image)

        prompt = """
        Analyze the provided food image for visible freshness indicators.

        Return ONLY valid JSON with these fields:
        {
          "item_name": "identified food",
          "freshness_level": "Fresh, Moderate, or Spoiled",
          "confidence": 0,
          "visible_observations": ["visible observation"],
          "recommendation": "practical recommendation"
        }

        Confidence must be a number from 0 to 100.
        Use visible evidence only. Mention unclear images or
        uncertain observations. Do not claim that an image alone
        can prove food is safe to eat.
        """

        client = genai.Client(api_key=api_key)

        response = await asyncio.to_thread(
            client.models.generate_content,
            model=MODEL_NAME,
            contents=[prompt, processed_image],
        )

        result_text = response.text

        if not result_text:
            raise ValueError("The AI returned an empty response.")

        result_text = result_text.strip()
        result_text = result_text.replace("```json", "")
        result_text = result_text.replace("```", "").strip()

        # Also handle responses containing text before the JSON object.
        start = result_text.find("{")
        if start == -1:
            raise ValueError("No JSON object found in AI response.")

        result, _ = json.JSONDecoder().raw_decode(
            result_text[start:]
        )

        allowed_levels = {"Fresh", "Moderate", "Spoiled"}

        if result.get("freshness_level") not in allowed_levels:
            result["freshness_level"] = "Unable to determine"

        try:
            confidence = float(result.get("confidence", 0))
            result["confidence"] = max(0, min(100, confidence))
        except (TypeError, ValueError):
            result["confidence"] = 0

        if not isinstance(result.get("visible_observations"), list):
            result["visible_observations"] = []

        result.setdefault("item_name", "Unknown")
        result.setdefault(
            "recommendation",
            "Use caution; image analysis cannot establish food safety."
        )

        # Basic preprocessing features, not a trained freshness score.
        result["image_features"] = features

        return result

    except Exception as e:
        print("FRESHNESS ERROR:", repr(e), flush=True)
        return {
            "item_name": "Unknown",
            "freshness_level": "Unable to determine",
            "confidence": 0,
            "visible_observations": [],
            "recommendation": (
                "Image analysis failed. Check the API key, "
                "model availability, network, and server logs."
            ),
        }