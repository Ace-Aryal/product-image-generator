from imagekitio import ImageKit
from ..config import IMAGEKIT_PRIVATE_KEY, IMAGEKIT_URL_ENDPOINT, IMAGEKIT_PUBLIC_KEY

imagekit = ImageKit(private_key=IMAGEKIT_PRIVATE_KEY)


def upload_file(
    file_bytes: bytes, file_name: str, folder: str, content_type: str = "iamage/png"
):
    try:
        response = imagekit.files.upload(
            file=(file_bytes, file_name, content_type),
            file_name=file_name,
            folder=folder,
            content_type=content_type,
            is_private_file=False,
            use_unique_file_name=True,
        )
        return response.url
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None


def get_varinats(base_url: str) -> dict:
    variants = {
        "square": f"{base_url}?tr=w-1080,h-1090,fo-auto,c_maintain_ratio",
        "default": f"{base_url}?tr=w-1280,h-720,fo-auto,c_maintain_ratio",
        "reels": f"{base_url}?tr=w-1080,h-1920,fo-auto,c_maintain_ratio",
    }
    return variants
