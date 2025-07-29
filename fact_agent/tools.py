import io
import vertexai
import os
import google.genai.types as types

from dotenv import load_dotenv
from google.adk.tools.tool_context import ToolContext
from google.genai.types import GenerateContentConfig, Part

from vertexai.preview.vision_models import ImageGenerationModel


load_dotenv()

async def generate_image_data(tool_context: ToolContext, fact: str) -> dict:
    """Generates an image and returns a dict with text and image_bytes."""
    print(f"Tool running: Generating image for '{fact}'...")
    
    try:      
        project = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION")

        if not project or not location:
            raise ValueError("GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION must be set in the environment.")
        
        vertexai.init(project=project, location=location)
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")

        images = model.generate_images(
            prompt=f"Generate a single image in futuristic style representing the following fact: {fact}",
            number_of_images=1,
            language="en",
            aspect_ratio="1:1",
            safety_filter_level="block_some",
            person_generation="allow_adult",
        )

        image_bytes = images[0]._image_bytes

        blob_part = Part.from_bytes(data=image_bytes, mime_type="image/png")
        
        try:
            res = await tool_context.save_artifact(filename="image.png", artifact=blob_part)
            return {
                'status': 'success',
                'result': res
            }
        except Exception as e:
            error_message = f"Failed to save artifact: {e}"
            print(error_message)
            return {"status": "error", "error_message": error_message}
    
    except ValueError as ve:
        print(f"Configuration error: {ve}")
        return {"status": "error", "error_message": str(ve)}
