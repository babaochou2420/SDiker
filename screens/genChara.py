
""" 
底圖生成
"""

from utils.config import Config
import gradio as gr

import uuid

from beans_logging.auto import logger

from daos.api.sd import SDAPI

sdAPI = SDAPI()


config = Config.get_config()


class genCharaTab:
  # def __init__(self, c_ref_base64, charaInfo):
  #   self.c_ref_base64 = c_ref_base64
  #   self.charaInfo = charaInfo

  def __init__(): pass

  def __load__(c_ref_base64, charaInfo, stateId):

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
        case "Semi-Realistic":

          pos += "<lora:add_detail:1>"
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
          uuid.uuid4()
      )

    def genRefTag(imgPath):
      # Your function logic here
      result = sdAPI.genRefTag(imgPath)
      return result

    def returnData(data):
      return data

    def load_lora_model(lora_file):
      # Function to load LoRA model (to be implemented)
      return "LoRA model loaded."

    #
    # Widgets
    #

    with gr.Tab("Step 1. Gen Chara"):
      with gr.Row():

        def genRefTag(imgPath):

          result = sdAPI.genRefTag(imgPath)

          return result

        with gr.Column():
          o_baseRef_txt = gr.Textbox()

          i_baseRef_btn = gr.Button(
              value="IMG-2-TXT", icon="./assets/icon/quick_reference_all_24dp.png")

          s_baseRef_btn = gr.Button(
              value="Use as Pos-Prompt", icon="./assets/icon/swipe_left_24dp.png")

        with gr.Column():
          i_baseRef_img = gr.Image(
              label="Reference", type="pil", format="png", height=360
          )

        i_baseRef_btn.click(fn=genRefTag, inputs=[
                            i_baseRef_img], outputs=[o_baseRef_txt])

      with gr.Row(min_height=300):
        with gr.Column(scale=1):
          i_pos = gr.Textbox(label="Positive Prompt", lines=5)

          def returnData(data): return data

          s_baseRef_btn.click(fn=returnData, inputs=[
              o_baseRef_txt], outputs=[i_pos])

          i_neg = gr.Textbox(
              label="Negative Prompt", lines=3, value=config['PROMPT']['fixed']['NEG_T']
          )

          with gr.Row():
            # Style
            with gr.Column(scale=1):

              f_demo = gr.Image(interactive=False,
                                value="./assets/demo/style_chibi.png",
                                label="ex", show_download_button=False, show_fullscreen_button=False,
                                width=192, height=192)

              # @gr.render(inputs=[i_sty], triggers=[i_sty.change])
              def x(style):

                imgPath = ""

                match style:
                  case "Chibi":
                    imgPath = "./assets/demo/style_chibi.png"
                  case "Anime 1":
                    imgPath = "./assets/demo/style_anime_1.png"
                  # case "Anime 2":
                  #   imgPath = "./assets/demo/style_anime_2.png"
                  # case "Semi-Realstic":
                  #   imgPath = "./assets/demo/style_anime_2.png"
                  # case "Realistic":
                  #   imgPath = "./assets/demo/style_chibi.png"
                  case _:
                    imgPath = ""

                return gr.update(value=imgPath)

              i_sty = gr.Radio(value="Chibi", choices=[
                               "Chibi", "Anime 1"], show_label=False)

              i_sty.change(x, i_sty, f_demo)

              # # DEMO
              # with gr.Row():
              #   gr.Image(interactive=False)

              # Second radio button for Chibi-specific options, initially hidden
              i_proportion = gr.Radio(
                  choices=["2-heads-tall"], value="2-heads-tall", label="Chibi Proportions", visible=True)

              def toggle_chibi_options(style):
                # Show options only if "Chibi" is selected
                if style == "Chibi":
                  return gr.update(visible=True)
                else:
                  return gr.update(visible=False)

              # Add the callback to update the visibility of the chibi options
              i_sty.change(toggle_chibi_options, i_sty, i_proportion)

            # Settings
            with gr.Column(scale=1):

              i_seed = gr.Textbox(value=-1, label="Seed")

              i_wid = gr.Slider(
                  minimum=256,
                  maximum=512,
                  value=512,
                  step=256,
                  label="Width",
              )
              i_hgt = gr.Slider(
                  minimum=256,
                  maximum=512,
                  value=512,
                  step=256,
                  label="Height",
              )
        # Passing reference image to SD-Tagger
        with gr.Column(scale=1):

          pass

      gen_chara_btn = gr.Button("Generate Character")

      with gr.Row():
        with gr.Column():
          o_seeds = gr.Textbox(label="Seed")
          with gr.Row():
            o_sty = gr.Textbox(label="Style")
            o_wid = gr.Textbox(label="Width")
            o_hgt = gr.Textbox(label="Height")
        o_chara = gr.Image(type="pil", format="png")

      lora_upload = gr.File(
          label="Upload LoRA for SD1.5",
          file_types=[".pt", ".ckpt", ".safetensors"],
      )
      lora_status = gr.Textbox(
          label="LoRA Model Status", interactive=False)

      # Button interactions
      gen_chara_btn.click(
          genChara,
          inputs=[i_pos, i_neg, i_sty, i_proportion, i_seed, i_wid, i_hgt],
          outputs=[o_chara, o_seeds, o_sty, o_wid,
                   o_hgt, charaInfo, c_ref_base64, stateId],
      )
      lora_upload.upload(
          load_lora_model, inputs=lora_upload, outputs=lora_status)
