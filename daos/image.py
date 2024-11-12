
from rembg import remove
from PIL import Image
import io


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
