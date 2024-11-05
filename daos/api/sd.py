import json
from PIL import Image
import io
import base64

import requests

from utils.config import Config

config = Config.get_config()


class SDAPI:
    def __init__(self):
        pass

    def genChara(self, pos, neg, style="chibi", seed=-1, width=512, height=512):

        # Step 1. Changing the base-model based on style
        self.setBase(style)

        url = config["API"]["SDWebUI"] + "/sdapi/v1/txt2img"

        # Step 2. Strengthen the prompt
        pos = config["PROMPT"]["fixed"]["POS_T"] + pos + ""
        neg = config["PROMPT"]["fixed"]["NEG_T"] + neg + ""

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

            image = Image.open(
                io.BytesIO(base64.b64decode(response.json().get("images", [None])[0]))
            )
            seeds = json.loads(response.json().get("info")).get("seed", -1)

            return image, seeds
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def genTag():
        None

    # def getBase(style):
    #     match style:
    #         case "Anime":
    #             return config['BASEMODEL']['style']['anime']
    #         case "Chibi":
    #             return config['BASEMODEL']['style']['chibi']

    # Changing the Base-Model
    def setBase(self, style):

        url = config["API"]["SDWebUI"] + "/sdapi/v1/options"

        # Get request template
        opt_json = requests.get(url=url).json()

        # Matching the name of base-model
        opt_json["sd_model_checkpoint"] = config["BASEMODEL"]["style"][style]

        # Update the setup
        requests.post(url=url, json=opt_json)
