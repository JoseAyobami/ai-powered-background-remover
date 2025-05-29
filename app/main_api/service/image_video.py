import requests
import json
from fastapi import UploadFile
import time
from PIL import Image
import io



with open('../secrets/config.json', 'r') as keys:
    secret_keys = json.load(keys)

STABILITY_API_KEY = secret_keys["stability_ai_token_video"]

def resize_image_to_supported(image_file: UploadFile) -> bytes:
    # Open the uploaded image
    img = Image.open(image_file.file)
    # Choose a supported size (e.g., 768x768)
    supported_size = (768, 768)
    img = img.resize(supported_size)
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes.read()

def image_to_video(image: UploadFile, output_format: str = "mp4") -> bytes:
    file_bytes = resize_image_to_supported(image)
    response = requests.post(
        url="https://api.stability.ai/v2beta/image-to-video",
        headers={
            "authorization": f"Bearer {STABILITY_API_KEY}",
            "accept": "application/json"
        },
        files={
            "image": (image.filename, file_bytes, "image/png")
        },
        data={
            "output_format": output_format
        },
    )

    # If the response contains a generation ID, poll for the result
    if response.status_code == 200 and "id" in response.json():
        generation_id = response.json()["id"]
        result_url = f"https://api.stability.ai/v2beta/image-to-video/result/{generation_id}"
        for _ in range(20):  # Try up to 20 times
            result_response = requests.get(
                result_url,
                headers={
                    "authorization": f"Bearer {STABILITY_API_KEY}",
                    "accept": "video/mp4"
                }
            )
            if result_response.status_code == 200 and result_response.headers.get("content-type", "").startswith("video"):
                return result_response.content
            time.sleep(3)  # Wait 3 seconds before retrying
        raise Exception("Video generation timed out.")
    elif response.status_code == 200 and response.headers.get("content-type", "").startswith("video"):
        # If the video is returned immediately
        return response.content
    else:
        raise Exception(str(response.json()))






