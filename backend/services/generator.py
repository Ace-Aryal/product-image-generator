import asyncio
import logging
from sqlmodel import Session, select
from database import engine
from models import Job, PImage
from .gemini_service import generate_product_image
from .imagekit_service import upload_file

logger = logging.getLogger(__name__)

STYLING_PROMPTS = {
    "minimal_studio": """
Clean minimal studio product photography.
White or light gray background, soft diffused lighting.
Sharp focus on the product with subtle shadows.
E-commerce style, high clarity, professional catalog look.
No distractions in background.
""",
    "luxury_premium": """
High-end luxury product photography.
Dramatic lighting with dark moody background and soft highlights.
Cinematic reflections, premium aesthetic, glossy finish.
Shallow depth of field, focus on elegance and exclusivity.
Apple / Rolex-style advertising feel.
""",
    "lifestyle_natural": """
Lifestyle product photography in a real-world environment.
Natural lighting, casual human interaction context.
Product placed in daily use scenario (desk, home, outdoor).
Warm tones, realistic and relatable mood.
Feels authentic and social-media friendly.
""",
    "tech_futuristic": """
Futuristic tech product visualization.
Neon lighting accents, gradient backgrounds, cyber aesthetic.
Floating or holographic style presentation.
Clean geometric composition, high contrast lighting.
Modern AI / sci-fi commercial look.
""",
}

STYLE_ORDER = [
    "minimal_studio",
    "luxury_premium",
    "lifestyle_natural",
    "tech_futuristic",
]


# steps:
# 1.DB mark generating : for the job
# 2. AI call -> generate image bytes
# 3.upload generated image to imagekit -> get url
# 4. db call, save the url, mark as uploaded
async def generate_single_product_image(
    image_id: str,
    prompt: str,
    headshot_url: str,
):
    with Session(engine) as session:
        image = session.get(PImage, image_id)
        image.status = "generating"
        style_name = image.style_name
        job_id = image.job_id
        session.add(image)
        session.commit()
    style_prompt = STYLING_PROMPTS[style_name]
    # AI Call
    try:
        image_byte = await generate_product_image(prompt, style_prompt, headshot_url)
        # upload image to imagekit
        url = upload_file(
            image_byte,
            file_name=f"{image_id}.png",
            folder=f"product_images/{job_id}/",
        )
        with Session(engine) as session:
            image = session.get(PImage, image_id)
            image.status = "uploaded"
            image.imagekit_url = url
            session.add(image)
            session.commit()
        logger.info(f"Image {image_id} generated and uploaded successfully.")
    except Exception as e:
        logger.error(f"Error occurred while generating image {image_id}: {e}")
        with Session(engine) as session:
            image = session.get(PImage, image_id)
            image.status = "failed"
            image.error_message = str(e)[:300]
            session.add(image)
            session.commit()
