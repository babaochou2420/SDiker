import json
from io import BytesIO
from PIL import Image
import io
import base64

import requests

from utils.config import Config

from beans_logging.auto import logger

config = Config.get_config()


class SDAPI:
  def __init__(self):
    pass

  def genTXT2IMG(payload):

    url = config["API"]["SDWebUI"] + "/sdapi/v1/txt2img"

    response = requests.post(url, json=payload)

    if response.status_code == 200:

      ref_base64 = base64.b64decode(response.json().get("images", [None])[0])

      image = Image.open(
          io.BytesIO(ref_base64)
      )
      seed = json.loads(response.json().get("info")).get("seed", -1)

      return image, ref_base64, seed
    else:
      print(f"Error {response.status_code}: {response.text}")
      return None

  def genChara(self, pos, neg, style="chibi", seed=-1, width=512, height=512):
    # Step 1. Changing the base-model based on style
    self.setBaseModel(style)

    url = config["API"]["SDWebUI"] + "/sdapi/v1/txt2img"

    # Step 2. Strengthen the prompt
    pos = config["PROMPT"]["fixed"]["POS_T"] + pos + ""
    # neg = config["PROMPT"]["fixed"]["NEG_T"] + neg + ""

    # Step 3. Setup the payload
    payload = {
        "prompt": pos,
        "negative_prompt": neg,
        "styles": [style],
        "width": width,
        "height": height,
        "send_images": True,
        #
        "seed": seed,
        #
        "steps": 20,
        "sampler_index": "Euler",
    }

    # Step 4. HTTP Request
    response = requests.post(url, json=payload)

    if response.status_code == 200:

      ref_base64 = base64.b64decode(response.json().get("images", [None])[0])

      image = Image.open(
          io.BytesIO(ref_base64)
      )
      seed = json.loads(response.json().get("info")).get("seed", -1)

      return image, ref_base64, seed
    else:
      print(f"Error {response.status_code}: {response.text}")
      return None

  def genRefTag(self, image, threshold=0.4, queue="", name_in_queue=""):

    def extract_tags(response):
      # Access the 'tag' dictionary within 'caption'
      tags = response.get('caption', {}).get('tag', {})

      # Sort tags by confidence score in descending order
      sorted_tags = sorted(
          tags.items(), key=lambda item: item[1], reverse=True)

      # ex: 1girl, solo, long_hair
      result = ', '.join([tag for tag, _ in sorted_tags])

      return result

    logger.warning("# RUN - genRefTag()")

    buffered = BytesIO()
    image.save(buffered, format="PNG")

    # Encode image in base64 format
    encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Define the payload
    payload = {
        "image": encoded_image,
        "model": "wd-v1-4-moat-tagger.v2",
        "threshold": threshold,
        "queue": queue,
        "name_in_queue": name_in_queue
    }

    # Send POST request to the endpoint
    try:
      response = requests.post(
          "http://127.0.0.1:7860/tagger/v1/interrogate", json=payload)
      response.raise_for_status()  # Check for HTTP errors

      logger.warning(response.json())

      logger.warning("# END - genRefTag()")

      # Parse and return the JSON response
      return extract_tags(response.json())
    except requests.exceptions.RequestException as e:
      print(f"Request failed: {e}")
      return None

  # def getBase(style):
  #   match style:
  #   case "Anime":
  #   return config['BASEMODEL']['style']['anime']
  #   case "Chibi":
  #   return config['BASEMODEL']['style']['chibi']

  # Changing the Base-Model
  def setBaseModel(self, style):
    url = config["API"]["SDWebUI"] + "/sdapi/v1/options"

    # Get request template
    opt_json = requests.get(url=url).json()

    # Matching the name of base-model
    opt_json["sd_model_checkpoint"] = config["BASEMODEL"]["style"][style]

    # Update the setup
    requests.post(url=url, json=opt_json)
