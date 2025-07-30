# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import vertexai
import os
import google.genai.types as types

from dotenv import load_dotenv
from google.adk.tools.tool_context import ToolContext
from google.genai.types import GenerateContentConfig, Part

from vertexai.preview.vision_models import ImageGenerationModel


load_dotenv()

PROJECT_ID=os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION=os.getenv("GOOGLE_CLOUD_LOCATION")


async def generate_image_data(tool_context: ToolContext, fact: str) -> dict:
    """Generates an image and returns a dict with text and image_bytes."""
    print(f"Tool running: Generating image for '{fact}'...")
    
    try:      
        if not PROJECT_ID or not LOCATION:
            raise ValueError("GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION must be set in the environment.")
        
        vertexai.init(project=PROJECT_ID, location=LOCATION)
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
