import os
import PIL
import math
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


def resize_contain(image_base_path: str, size=(780, 480), resample=Image.LANCZOS, bg_color=(255, 255, 255, 0)):
    image = Image.open(image_base_path)

    img_format = image.format
    img = image.copy()
    img.thumbnail((size[0], size[1]), resample)
    background = Image.new('RGB', (size[0], size[1]), bg_color)
    img_position = (
        int(math.ceil((size[0] - img.size[0]) / 2)),
        int(math.ceil((size[1] - img.size[1]) / 2))
    )
    background.paste(img, img_position)
    background.format = img_format
    return background.convert('RGB')


# def resize_crop(image_base_path: str, size=(780, 480)):
#     image = Image.open(image_base_path)
#     img_format = image.format
#     image = image.copy()
#     old_size = image.size
#     left = (old_size[0] - size[0]) / 2
#     top = (old_size[1] - size[1]) / 2
#     right = old_size[0] - left
#     bottom = old_size[1] - top
#     rect = [int(math.ceil(x)) for x in (left, top, right, bottom)]
#     left, top, right, bottom = rect
#     crop = image.crop((left, top, right, bottom))
#     crop.format = img_format
#     return crop


# def resize_crop2(image, size=(780, 480)):

#     img_format = image.format
#     image = image.copy()
#     old_size = image.size
#     left = (old_size[0] - size[0]) / 2
#     top = (old_size[1] - size[1]) / 2
#     right = old_size[0] - left
#     bottom = old_size[1] - top
#     rect = [int(math.ceil(x)) for x in (left, top, right, bottom)]
#     left, top, right, bottom = rect
#     crop = image.crop((left, top, right, bottom))
#     crop.format = img_format
#     return crop


# def resize_height(image_base_path: str, size=(780, 480), resample=Image.LANCZOS):
#     image = Image.open(image_base_path)

#     try:
#         height = size[1]
#     except:
#         height = size
#     img_format = image.format
#     img = image.copy()
#     img_size = img.size

#     if img_size[1] == height:
#         return image
#     new_width = int(math.ceil((height / img_size[1]) * img_size[0]))
#     img.thumbnail((new_width, height), resample)
#     img.format = img_format
#     return img


# def resize_width(image_base_path: str, size=(780, 480), resample=Image.LANCZOS):
#     image = Image.open(image_base_path)

#     try:
#         width = size[0]
#     except:
#         width = size
#     img_format = image.format
#     img = image.copy()
#     img_size = img.size

#     if img_size[0] == width:
#         return image
#     new_height = int(math.ceil((width / img_size[0]) * img_size[1]))
#     img.thumbnail((width, new_height), resample)
#     img.format = img_format
#     return img


# def resize_cover(image_base_path: str, size=(780, 480), resample=Image.LANCZOS):
#     image = Image.open(image_base_path)

#     img_format = image.format
#     img = image.copy()
#     img_size = img.size
#     ratio = max(size[0] / img_size[0], size[1] / img_size[1])
#     new_size = [
#         int(math.ceil(img_size[0] * ratio)),
#         int(math.ceil(img_size[1] * ratio))
#     ]
#     img = img.resize((new_size[0], new_size[1]), resample)
#     img = resize_crop2(img, size)
#     img.format = img_format
#     return img
