import gradio as gr
from PIL import Image
import io
import zipfile

from daos.api.sd import SDAPI
from daos.chara import CharaDao
from daos.emote import EmoteDao

from beans_logging.auto import logger


sdAPI = SDAPI()

emoteDao = EmoteDao()


#
# Functions
#


def genChara(pos, neg, style, seed=-1, wid=512, hgt=512):

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
      with gr.Row(min_height=300):
        with gr.Column(scale=1):
          i_pos = gr.Textbox(label="Positive Prompt", lines=5)
          i_neg = gr.Textbox(
              label="Negative Prompt", lines=3, value="easynegative"
          )

          with gr.Row():
            with gr.Column(scale=1):
              i_sty = gr.Radio(value="Chibi", choices=[
                               "Chibi", "Anime", "Realistic"], label="")
              i_seed = gr.Textbox(value=-1, label="Seed")
            with gr.Column(scale=1):
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
        with gr.Column(scale=1):
          i_ref = gr.Image(
              label="Reference", type="pil", format="png", height=360
          )

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
          inputs=[i_pos, i_neg, i_sty, i_seed, i_wid, i_hgt],
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

      gen_stickers_btn = gr.Button("Generate Emotes")

      sticker_output = gr.Gallery(
          label="Generated Emotes", columns=3, height=300, preview=True
      )

      # def show_emotes(set):
      #   return emoteDao.getEmoteSet(set)

      @gr.render(inputs=s_emoteSet)
      def listEmoteElements(set):

        set = emoteDao.getEmoteSet(set)

        for doc in set:
          """"""
          with gr.Row():
            with gr.Column(scale=1):
              o_img = gr.Image(format="png", type="pil")
            with gr.Column(scale=5):
              with gr.Row():
                i_pos = gr.Textbox(label="Pos",
                                   value=f"{doc['pos']}")
                i_neg = gr.Textbox(label="Neg",
                                   value=f"{doc['neg']}")
              with gr.Row():
                with gr.Column(scale=1):
                  i_gen = gr.Button(
                      value="Generate",
                      icon="./assets/icon/replay_24dp.png",
                  )

                  i_gen.click(fn=genEmote, inputs=[
                              charaInfo, c_ref_base64, i_pos, i_neg], outputs=[o_img])
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

                with gr.Column(scale=1):
                  with gr.Accordion("Advanced"):

                    with gr.Column():
                      with gr.Row():
                        gr.Checkbox(
                            label="IPadapter (This will take much time)", scale=1)
                        # gr.Textbox(value="This will take much time", scale=2)
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
      full_image_output = gr.Image(
          label="All Stickers Together", type="pil", format="png"
      )
      zip_output = gr.File(label="Download All Stickers as Zip")
      export_btn = gr.Button("Export")

      export_btn.click(export_images, outputs=[
                       full_image_output, zip_output])

demo.launch(server_port=18477)
