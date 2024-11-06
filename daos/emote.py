import io
import json
from daos.api.sd import SDAPI

import requests
import base64

from PIL import Image

from utils.config import Config

config = Config.get_config()


class EmoteDao:
  def __init__(self):
    self.set = {
        "": [],
        "set1": [
            {"code": "1", "pos": "(angry:1.1)", "neg": "blush"},
            {"code": "2", "pos": "(happy:1.2)", "neg": ""},
            {"code": "3", "pos": "(sleeping:1.2)", "neg": ""},
            {"code": "4", "pos": "(crying:0.8)", "neg": ""},
            {"code": "5", "pos": "(blush:1.2), (shy)", "neg": ""},
            {
                "code": "6",
                "pos": "(blush:1.2), (embarassed), flying sweatdrop",
                "neg": "",
            },
            {"code": "7", "pos": "(panicking:1.2)", "neg": ""},
            {"code": "8", "pos": "(terrified:1.2)", "neg": ""},
            {"code": "9", "pos": "(drooling)", "neg": ""},
            {"code": "10",
             "pos": "(waving hello:1.2), (smiling:1.2)", "neg": ""},
            {"code": "11", "pos": "sad, frowning, gloomy, downcast", "neg": ""},
        ],
        "set2": [
            {"code": "11", "pos": "sad, frowning, gloomy, downcast", "neg": ""}, {
                "code": "11", "pos": "sad, frowning, gloomy, downcast", "neg": ""}
        ],
    }

  def getEmoteSetList(self):
    return list(self.set.keys())

  def getEmoteSet(self, set):

    return list(self.set[set])

  def setPrompt(self, closeup, pos, neg, docpos, docneg):

    pos = pos + "<lora:chibi_emote_v1:1>, emote, "

    if closeup:
      pos = pos + "(close up:1.2), "

    pos += docpos
    neg += docneg

    return pos, neg

  # def genEmote(
  #     self, pos, neg, closeup, set="set1", style="chibi", seed=-1, wid=512, hgt=512
  # ):

  #   sdAPI = SDAPI()

  #   gallery = []

  #   pos = pos + "<lora:chibi_emote_v1:1>, emote, "

  #   if closeup:
  #     pos = pos + "(close up:1.2), "

  #   for doc in self.set[set]:
  #     # For each,
  #     docpos = pos + doc["pos"]
  #     docneg = neg + doc["neg"]

  #     img, seed = sdAPI.genChara(docpos, docneg, style, seed, wid, hgt)

  #     gallery.append(img)

  #   return gallery

  def genEmote(self, ref_base64, pos, neg, style, seed, wid, hgt):

    # First time using old seed
    # Afterwards time using random seed

    # Define the WebUI API URL for txt2img
    api_url = config["API"]["SDWebUI"]+"/sdapi/v1/txt2img"

    ref_base64 = base64.b64encode(ref_base64).decode("utf-8")

    # Prepare the payload with ControlNet parameters for the 'reference' module using 'adain+attn'
    payload = {
        "prompt": pos,
        "negative_prompt": neg,
        "styles": [style],
        "width": wid,
        "height": hgt,
        #
        "seed": seed,
        #
        "steps": 20,
        "sampler_name": "Euler a",
        "cfg_scale": 7.0,
        #
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "enabled": True,
                        "image": ref_base64, "weight": 1, "resize_mode": "Envelope (Outer Fit)",
                        "module": "reference_adain+attn", "lowvram": True, "processor_res": wid, "control_mode": "Balanced"}
                ]
            }
        }
    }

    # Make the API request
    response = requests.post(api_url, json=payload)

    # Check if request was successful
    if response.status_code == 200:

      image = Image.open(
          io.BytesIO(base64.b64decode(
              response.json().get("images", [None])[0]))
      )

      return image
    else:
      print(f"Error: {response.status_code}")
      print(response.text)
