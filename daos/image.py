
import base64
import os
from rembg import remove
from PIL import Image
import io

from beans_logging.auto import logger


class ImageDao:

  def __init__(self): pass

  # Remove the BG in input image
  def rmbg(input_image: Image.Image) -> Image.Image:

    # Convert the input image to bytes
    img_byte_arr = io.BytesIO()
    input_image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Use rembg to remove the background
    output_data = remove(img_byte_arr)

    # Convert the output bytes back to a PIL Image
    output_image = Image.open(io.BytesIO(output_data)).convert("RGBA")

    return output_image

  def getSize(image: Image.Image):

    if image:
      return image.size

    return 0, 0

  # Save image in Base64
  def savImageBIN(image_base64, filepath):
    # Decode the base64 image string into a PIL Image
    if isinstance(image_base64, str):
      image_data = base64.b64decode(image_base64)
    elif isinstance(image_base64, bytes):
      image_data = image_base64

    image = Image.open(io.BytesIO(image_data))

    # Convert the image to "RGBA" to ensure transparency is preserved, if any
    image = image.convert("RGBA")

    # Save the image as 0.png in the directory
    image.save(filepath, "PNG")

    return f"Image saved successfully at: {filepath}"

  # Save image in PIL.Image
  def savImagePIL(image_PIL, filepath):
    # Convert the image to "RGBA" to ensure transparency is preserved, if any
    image = image.convert("RGBA")

    # Save the image as 0.png in the directory
    image.save(filepath, "PNG")

    return f"Image saved successfully at: {filepath}"
