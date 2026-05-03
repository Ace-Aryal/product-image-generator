from google import genai
from google.genai import types
from ..config import GEMINI_API_KEY
from io import BytesIO
import requests
from PIL import Image

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_product_image(
    user_prompt: str, style_prompt: str, headshot_url: str
) -> bytes:

    full_prompt = (
        f"{style_prompt}\n\n "
        f"User Prompt : {user_prompt}\n"
        "IMPORTANT: The image should be a product image with a clear background, suitable for e-commerce listings, Product should be as prominent as possible in the image, with the headshot used as a reference for style and lighting."
        f"Headshot URL: {headshot_url}"
    )
    image = Image.open(BytesIO(requests.get(headshot_url).content))
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[full_prompt, image],
        config=types.GenerateContentConfig(
            image_config=types.ImageConfig(
                image_size="512", aspect_ratio="1:1", output_mime_type="image/png"
            )
        ),
    )
    for part in response.parts:
        if part.inline_data is not None:
            image = part.as_image()
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            return buffer.getvalue()
    raise ValueError("No image data found in the response")
