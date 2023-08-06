import os
import PIL
import base64
import requests
from PIL import Image
from io import BytesIO
from mimetypes import guess_type


def image_to_bytes(image, format_file):
    im_file = BytesIO()
    image.save(im_file, format=format_file)
    return im_file.getvalue()


def get_format_file(image_file_name: str):
    format_file = image_file_name.partition(".")[-1]
    if format_file.upper() == "JPG":
        format_file = "JPEG"
    return format_file


def get_mimetype(image_file_name: str):
    return guess_type(image_file_name)[0]


def file_to_image(image_file_name: str):
    with open(image_file_name, 'r') as f_image:
        return Image.open(f_image)


def image_size(image_file_name: str):
    image = Image.open(image_file_name)
    return image.size


def url_to_image(url: str):
    req = requests.get(url)
    image = BytesIO(req.content)
    return image


def string_to_image(image_string: str):
    image_file = BytesIO(image_string)
    image = Image.open(image_file)
    return image


def image_to_b64(image: bytes, mimetype: str):
    return f'data:{mimetype};base64,' + base64.b64encode(image).decode('utf-8')


def b64_to_image(image_b64, quality=100):
    foto = BytesIO()
    base64_str = image_b64.partition(';base64,')
    content_type = base64_str[0].replace('data:', '')
    image_string = BytesIO(base64.b64decode(base64_str[2]))
    image = Image.open(image_string)
    image.save(foto, image.format, quality=quality)
    foto.seek(0)
    return foto, content_type


def resize(image_base_path: str, width_base=720):
    image = Image.open(image_base_path)
    width_percent = (width_base / float(image.size[0]))
    height_percent = int((float(image.size[1]) * float(width_percent)))
    image_resized = image.resize(
        (width_base, height_percent), PIL.Image.ANTIALIAS)
    # image_resized.save(image_resized_path)
    return image_resized


def thumbnail(image_base_path: str, width_base=200, resample=3, reducing_gap=2.0):
    image = Image.open(image_base_path)
    width_percent = (width_base / float(image.size[0]))
    height_percent = int((float(image.size[1]) * float(width_percent)))
    image.thumbnail(size=(width_base, height_percent),
                    resample=resample, reducing_gap=reducing_gap)
    # image.save(image_thumbnail_path)
    return image
