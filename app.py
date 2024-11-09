import gradio as gr
from PIL import Image
import io
import zipfile

from daos.api.sd import SDAPI
from daos.chara import CharaDao
from daos.emote import EmoteDao

from beans_logging.auto import logger


from utils.config import Config

from screens.genChara import genCharaTab
from screens.genEmote import genEmoteTab
from screens.savEmote import savEmoteTab

from screens.settings import settingsTab


sdAPI = SDAPI()

emoteDao = EmoteDao()

config = Config.get_config()


#
# Functions
#


def genChara(pos, neg, style, porportion, seed=-1, wid=512, hgt=512):

  logger.warning(f"Calling style: {style}")

  match porportion:
    case "2-Heads-Tall":
      pos += "2-heads-tall"

  match style:
    case "Chibi":

      pos += "<lora:chibi_emote_v1:1>, chibi emote, "
    case "Anime 1":
      pass
    case "Anime 2":
      pass
    case "Realistic":
      pass
    case _:
      pass

  image, ref_base64, seed = sdAPI.genChara(pos, neg, style, seed, wid, hgt)

  return (
      image,
      seed,
      style,
      wid,
      hgt,
      {"pos": pos, "neg": neg, "style": style,
          "seed": seed, "wid": wid, "hgt": hgt},
      ref_base64,
  )


# def getChara(pos, neg, style, seeds, wid, hgt):
#   return CharaDao.getChara(pos, neg, style, seeds, wid, hgt)





#
# Interface
#

#
# i_ : input
# o_ : output
# s_ : system
# c_ : cache
# f_ : fixed
#
with gr.Blocks() as demo:
  #
  # State
  #

  c_ref_base64 = gr.State(value=None)

  charaInfo = gr.State(value=None)

  with gr.Tabs():
    
    genCharaTab.__load__(c_ref_base64, charaInfo)

    genEmoteTab.__load__(c_ref_base64, charaInfo)

    savEmoteTab.__load__()

    settingsTab.__load__()


demo.launch(server_port=18477)
