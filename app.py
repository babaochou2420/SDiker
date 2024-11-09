import gradio as gr
from PIL import Image
import io
import zipfile

from daos.api.sd import SDAPI
from daos.chara import CharaDao
from daos.emote import EmoteDao

from beans_logging.auto import logger

from utils.config import Config


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


def genEmote(charaInfo, ref_base64, docpos, docneg):

  pos, neg, style, seed, wid, hgt = CharaDao.getChara(charaInfo)

  pos, neg = emoteDao.setPrompt(False, pos, neg, docpos, docneg)

  img = emoteDao.genEmote(ref_base64, pos, neg, style, seed, wid, hgt)

  return img


def update_emote_prompt(index, new_prompt):
  return None


def load_lora_model(lora_file):
  # Function to load LoRA model (to be implemented)
  return "LoRA model loaded."


def export_images():
  # Export function (to be implemented)
  return None, None


#
# State
#


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
    with gr.Tab("Step 1. Gen Chara"):

      gr.Markdown("### Step 1. Generate Character")

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
                  case "Anime 2":
                    imgPath = "./assets/demo/style_anime_2.png"
                  case "Realistic":
                    imgPath = "./assets/demo/style_chibi.png"
                  case _:
                    imgPath = ""

                return gr.update(value=imgPath)

              i_sty = gr.Radio(value="Chibi", choices=[
                               "Chibi", "Anime 1", "Anime 2", "Realistic"], label="")

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
                   o_hgt, charaInfo, c_ref_base64],
      )
      lora_upload.upload(
          load_lora_model, inputs=lora_upload, outputs=lora_status)

    with gr.Tab("Step 2. Gen Sticker"):

      s_emoteSet = gr.Dropdown(
          value="", choices=list(emoteDao.getEmoteSetList()), label="Select Set"
      )

      gr.Markdown("### Step 2. Generate Stickers")

      # gen_stickers_btn = gr.Button("Generate Emotes")

      # sticker_output = gr.Gallery(
      #     label="Generated Emotes", columns=3, height=300, preview=True
      # )

      # def show_emotes(set):
      #   return emoteDao.getEmoteSet(set)

      @gr.render(inputs=s_emoteSet)
      def listEmoteElements(set):

        set = emoteDao.getEmoteSet(set)

        for doc in set:
          """"""
          with gr.Row(variant="panel"):
            with gr.Column(scale=2):
              # with gr.Row():
              #   f_seq = gr.Textbox(
              #       value=f"Seq: {doc['code']}", container=False)

              o_img = gr.Image(format="png", type="pil",
                               label=f"{doc['code']}")

            with gr.Column(scale=6):
              with gr.Row():

                i_pos = gr.Textbox(label="Pos",
                                   value=f"{doc['pos']}")
                i_neg = gr.Textbox(label="Neg",
                                   value=f"{doc['neg']}")
              with gr.Row():
                with gr.Column(scale=1):
                  with gr.Row():
                    i_gen = gr.Button(
                        value="Generate",
                        icon="./assets/icon/replay_24dp.png",
                    )
                    i_gen.click(fn=genEmote, inputs=[
                                charaInfo, c_ref_base64, i_pos, i_neg], outputs=[o_img])
                    i_savImage = gr.Button(
                        value="Save Result", icon="./assets/icon/new_label_24dp.png")
                with gr.Column(scale=1):
                  gr.Checkbox(label="Close Up")

                with gr.Column(scale=1):
                  with gr.Accordion("LoRA"):

                    with gr.Column():
                      # p_loraDetail = gr.Image()
                      gr.Slider(
                          minimum=-1,
                          maximum=2,
                          step=0.1,
                          value=0,
                          label="Detail Tweaker",
                      )

                # with gr.Column(scale=1):
                #   with gr.Accordion("Advanced"):

                #     with gr.Column():
                #       with gr.Row():
                #         gr.Checkbox(
                #             label="IPadapter (This will take much time)", scale=1)
                #         # gr.Textbox(value="This will take much time", scale=2)
          """"""

      s_emoteSet.change(fn=listEmoteElements, inputs=s_emoteSet)

      # # Set up button interaction for generating emotes
      # gen_stickers_btn.click(
      #     genEmote,
      #     inputs=[charaInfo, s_emoteSet],
      #     outputs=[sticker_output],
      # )

    with gr.Tab("Step 3. Output"):
      gr.Markdown("### Step 3. Output")

      with gr.Row():
        # Grid
        with gr.Column(variant="panel"):
          with gr.Row():
            grid_button = gr.Button(
                "Grid Layout", icon="./assets/icon/grid_view_24dp.png", scale=3)
            grid_layout_dropdown = gr.Dropdown(
                choices=["3x3", "3x4", "4x4"],
                value="3x3", scale=1, show_label=False, container=False
            )
          grid_image_output = gr.Image(
              label="Grid Layout Preview",
              type="pil",
              format="png"
          )

        # File
        with gr.Column(variant="panel"):
          compress_button = gr.Button(
              "File Output", icon="./assets/icon/output_circle_24dp.png")
          zip_image_output = gr.Image(
              label="Compressed Images Preview",
              type="pil",
              format="png"
          )

      # # Define button click actions
      # grid_button.click(
      #     fn=generate_grid_layout,
      #     inputs=[grid_layout_dropdown],
      #     outputs=[grid_image_output]
      # )

      # compress_button.click(
      #     fn=compress_images,
      #     outputs=[zip_image_output]
      # )

    with gr.Tab("Settings"):
        # # Emote set list display
        # emote_set_list = gr.Dropdown(choices=list(emote_sets.keys()), label="Select Emote Set")

        # Display and edit JSON content of selected emote set
      json_editor = gr.Textbox(
          label="Emote Set Content", lines=20, interactive=True)
      save_button = gr.Button("Save Changes")

      # Delete and edit buttons
      with gr.Row():
        delete_button = gr.Button("Delete Selected Emote Set")
        refresh_button = gr.Button("Refresh List")

      # Upload new emote set
      with gr.Row():
        json_upload = gr.File(
            label="Upload New Emote Set (JSON)", type="filepath")
        upload_button = gr.Button("Upload Emote Set")

      # # Set up interactions
      # emote_set_list.change(
      #     lambda emote_set_name: show_emote_set(emote_set_name),
      #     inputs=emote_set_list,
      #     outputs=json_editor
      # )
      # save_button.click(
      #     lambda emote_set_name, content: save_emote_set(
      #         emote_set_name, content),
      #     inputs=[emote_set_list, json_editor],
      #     outputs=json_editor
      # )
      # delete_button.click(
      #     lambda emote_set_name: delete_emote_set(emote_set_name),
      #     inputs=emote_set_list,
      #     outputs=gr.Textbox(label="Action Status", interactive=False)
      # )
      # upload_button.click(
      #     upload_emote_set,
      #     inputs=json_upload,
      #     outputs=gr.Textbox(label="Upload Status", interactive=False)
      # )
      # refresh_button.click(
      #     lambda: load_emote_sets(),
      #     outputs=emote_set_list
      # )

demo.launch(server_port=18477)
