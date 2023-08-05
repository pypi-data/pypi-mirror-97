import re
import base64
from io import BytesIO
from PIL import Image

def get_image_bytes(image: Image, format: str = "png") -> bytes:
    buffer = BytesIO()
    image.save(buffer, format=format)
    return buffer.getvalue()

def get_base64image(image: bytes, format: str = "png") -> str:
    return """data:image/{format};base64,{data}""".format(
        format=format,
        data=base64.encodebytes(image).decode(),
        )

def parse_base64image(image: str):
    header, data = image.split(",", 1)
    format = re.findall("data:image/(.*);base64", header)[0]
    return format, base64.decodebytes(data.encode("utf-8"))

def resize(src: Image, scale: float) -> Image:
    src_size = src.size
    dst_size = (int(src_size[0] * scale), int(src_size[1] * scale))
    dst = src.resize(dst_size)
    return dst

