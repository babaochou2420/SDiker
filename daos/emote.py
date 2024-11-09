import zipfile
import uuid
import os
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
        "": [{"code": "1", "pos": "", "neg": ""}],
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
            {"code": "11", "pos": "sad, frowning, gloomy, downcast", "neg": ""},
            {"code": "11", "pos": "sad, frowning, gloomy, downcast", "neg": ""},
        ],
        "set3": [
            {
                "code": "1",
                "pos": "(sparkle:1.2), +_+, emote, blush, smile, open mouth, sparkling eyes",
                "neg": "",
            },
            {"code": "1",
             "pos": "(angry:1.2), blush, open mouth, ", "neg": ""},
            {"code": "2",
             "pos": "(laughing:1.2), >_<, closed eyes, fang, open mouth, (pointing up:1.2)", "neg": ""},
            {"code": "3",
             "pos": "(laughing:1.2), fang, open mouth, thumb up,", "neg": ""},
            {"code": "4",
             "pos": "(laughing:1.2), wink, (one eye closed:1.1), playful smile, ", "neg": ""},
            {"code": "5",
             "pos": "(laughing:1.2), (open mouth:1.2), (upper teeth:1.2), (both eyes open:1.6), blush, ", "neg": ""},
            {"code": "6",
             "pos": "(wide open eyes:1.2), raised eyebrows, slightly open mouth, (surprised:1.2), (shocked:1.2), ", "neg": ""},
            {"code": "7",
             "pos": "(pout:1.2), closed eyes, (look away:1.2)", "neg": ""},
            {"code": "8",
             "pos": "(annoyed:1.2), unhappy, (angry:1.1), ", "neg": "blush, "},
            {"code": "9",
             "pos": "(panicking:1.2), (flying sweatdrops:1.1), (wavy mouth:1.1), open mouth, ", "neg": ""},
            {"code": "10",
             "pos": "(terrified:1.2), (scared), (shrinking:1.2), cowering, downcast, (flying sweatdrops:1.1), slightly open mouth, ", "neg": ""},
            {"code": "11", "pos": "(smug:1.2), looking at viewer,", "neg": ""},
            {"code": "12",
             "pos": "(laughing), pointing at viewer, open mouth, (tears at eye corners:0.9), (small tears:0.9)", "neg": ""},
            {"code": "1", "pos": "", "neg": ""},
            {"code": "1", "pos": "", "neg": ""},
            {"code": "1", "pos": "", "neg": ""},
            {"code": "1",
             "pos": "", "neg": ""},
        ],
        "set4": [
            {"code": "1",
             "pos": "(crossed arm:1.2), (angry:1.1), grit teeth", "neg": ""},
            {"code": "1", "pos": "", "neg": ""},
            {"code": "1", "pos": "", "neg": ""},
            {"code": "1", "pos": "", "neg": ""},
            {"code": "1", "pos": "", "neg": ""},
            {"code": "1", "pos": "", "neg": ""},
        ],
        "set7": [
            {"code": "1", "pos": "ecstatic, thrilled, overjoyed, elated, jumping up and down, raising arms in the air", "neg": ""},
            {"code": "2", "pos": "relieved, reassured, comforted, soothed, sighing, slumping shoulders", "neg": ""},
            {"code": "3",
             "pos": "(curious:1.1), inquisitive, fascinated, interested, (leaning forward:1.2), (tilting head:1.5)", "neg": ""},
            {"code": "4", "pos": "confident, secure, self-assured, bold, standing up straight, chest out, looking directly at camera", "neg": ""},
            {"code": "5", "pos": "bitter, resentful, indignant, enraged, gnashing teeth, clenching fists, glaring at someone", "neg": ""},
            {"code": "6",
             "pos": "(cautious:1.1), vigilant, attentive, watchful, holding head back, (narrowed eyes:1.2), (squint:1.2)", "neg": ""},
            {"code": "7", "pos": "euphoric, ecstatic, jubilant, triumphant, twirling around, throwing arms up in the air, grinning", "neg": ""},
            {"code": "8", "pos": "fearful, alarmed, apprehensive, scared, tensing up, dry mouth, avoiding eye contact",
             "neg": ""},  # trying to improve
            {"code": "9", "pos": "apologetic, remorseful, contrite, sorrowful, bowed head, slumped shoulders, clasped hands", "neg": ""},
            {"code": "10", "pos": "exhilarated, thrilled, invigorated, energized, pumping fist, jumping up and down, beaming smile", "neg": ""},
            {"code": "11", "pos": "indifferent, neutral, disconnected, apathetic, shrugging shoulders, looking away, slouching", "neg": ""},
            {"code": "12", "pos": "sympathetic, compassionate, empathetic, supportive, placing hand on shoulder, listening intently, nodding", "neg": ""},
            {"code": "13", "pos": "amused, entertained, delighted, tickled, laughing, giggling, winking", "neg": ""},
            {"code": "14", "pos": "disappointed, letdown, crushed, crestfallen, slumping shoulders, drooping head, frowning", "neg": ""},
            {"code": "15", "pos": "exasperated, frustrated, irritated, annoyed, scratching head, growling, rolling eyes", "neg": ""},
            {"code": "16", "pos": "inspired, motivated, driven, impassioned, thrusting forward, gesticulating, flashing a determined look", "neg": ""},
            {"code": "17",
             "pos": "melancholy, somber, contemplative, (mournful:1.2), (sitting with head in hands:1.2), (gazing downward:1.2), slow blinking, (tears:0.8)", "neg": ""},
            {"code": "18", "pos": "(coughing:1.2)", "neg": ""}
        ]
    }

    #  (arms outstretched), (reaching forward:1.2), (open hands), (inviting expression:1.2), (asking for a hug:1.2)

  def getEmoteSetList(self):
    return list(self.set.keys())

  def getEmoteSet(self, set):

    return list(self.set[set])

  def setPrompt(self, closeup, pos, neg, docpos, docneg):

    pos = pos + "emote, "

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
    api_url = config["API"]["SDWebUI"] + "/sdapi/v1/txt2img"

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
                        "image": ref_base64,
                        "weight": 1,
                        "resize_mode": "Envelope (Outer Fit)",
                        "module": "reference_adain+attn",
                        "lowvram": True,
                        "processor_res": wid,
                        "control_mode": "My prompt is more important",
                    }
                ]
            }
        },
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

  def savEmote(self, image: Image.Image, uuid, seq: int) -> str:
    # Generate a unique folder path with UUIDv4
    folder_path = os.path.join('./archive', str(uuid))
    # Create the folder if it doesn’t exist
    os.makedirs(folder_path, exist_ok=True)

    # Define the full path with the given sequence number as the filename
    file_path = os.path.join(folder_path, f"{seq}.png")

    # # Check if file already exists
    # if os.path.exists(file_path):
    #   # Ask for confirmation to override
    #   user_confirm = input(
    #       f"File '{file_path}' already exists. Do you want to override it? (y/n): ")
    #   if user_confirm.lower() != 'y':
    #     return "Save operation canceled by user."

    # Save the image as a PNG file
    image.save(file_path, "PNG")

    return f"Image saved successfully at: {file_path}"

  def savEmoteZip(self, uuid):
    # Define the folder path based on the UUID
    folder_path = os.path.join('./archive', uuid)

    # Check if the folder exists
    if not os.path.isdir(folder_path):
      return f"Directory not found for UUID: {uuid}"

    # Define the zip file path
    zip_path = os.path.join(folder_path, f"SDiker_{uuid}.zip")

    # Create a zip file and add all PNG files from the directory
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
      for root, _, files in os.walk(folder_path):
        for file in files:
          if file.endswith(".png"):
            file_path = os.path.join(root, file)
            # Add file to zip with relative path to avoid full path structure
            zipf.write(file_path, os.path.relpath(file_path, folder_path))

    # Return the path to the zip file for download
    return zip_path
