
""" 
貼圖生成
"""

from beans_logging.auto import logger
import json
import gradio as gr

from daos.chara import CharaDao
from daos.emote import EmoteDao

from PIL import Image
import os

emoteDao = EmoteDao()
charaDao = CharaDao()


class genEmoteTab():
  def __init__(): pass

  def __load__(c_ref_base64, charaInfo, stateId):
    #
    # Functions
    #
    def genEmote(charaInfo, ref_base64, docpos, docneg):

      pos, neg, style, seed, wid, hgt = charaDao.getChara(charaInfo)

      pos, neg = emoteDao.setPrompt(False, pos, neg, docpos, docneg)

      img = emoteDao.genEmote(ref_base64, pos, neg, style, -1, wid, hgt)

      return img

    def savEmote(img, uuid, seq):
      emoteDao.savEmote(img, uuid, seq)

    #
    # Widgets
    #
    with gr.Tab("Step 2. Gen Sticker") as tab:

      def get_latest_folder() -> str:

        directory = os.path.join('./archive')

        # List all subdirectories in the given directory
        subdirs = [
            d for d in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, d))
        ]

        if not subdirs:
          return None  # No folders found

        # Get the latest folder based on modification time
        latest_folder = max(
            subdirs,
            key=lambda d: os.path.getmtime(os.path.join(directory, d))
        )

        return latest_folder

      # Preview - Chara
      def fetchChara(uuid: str):
        # Define the folder path based on the UUID
        folder_path = os.path.join('./archive', uuid)

        # Define the expected file path for 0.png
        file_path = os.path.join(folder_path, '0.png')

        # Check if 0.png exists in the folder
        if not os.path.isfile(file_path):
          return None  # Return None if the file does not exist

        return file_path

      with gr.Row():
        with gr.Column(scale=7):
          i_uuid = gr.Textbox(label="UUID")

        with gr.Column(scale=3):
          o_demoview = gr.Image(format="png", type="pil", height=256)

      i_uuid.change(fn=fetchChara, inputs=[i_uuid], outputs=[o_demoview])

      # Function - Emote
      s_emoteSet = gr.Radio(
          value="", choices=list(emoteDao.lstEmoteSets()), label="Select Set"
      )

      # gen_stickers_btn = gr.Button("Generate Emotes")

      # sticker_output = gr.Gallery(
      #     label="Generated Emotes", columns=3, height=300, preview=True
      # )

      # def show_emotes(set):
      #   return emoteDao.getEmoteSet(set)

      @gr.render(inputs=s_emoteSet, triggers=[s_emoteSet.change])
      def listEmoteElements(key):

        set = emoteDao.getEmoteSet(key)

        for doc in set[key]:

          """"""
          with gr.Column(variant="panel"):
            with gr.Row():

              # Basic Settings
              with gr.Column(scale=7):

                with gr.Row():

                  with gr.Column():

                    gr.Markdown(value="Pos")

                    i_pos_emo = gr.Textbox(max_lines=1, label="Emotions",
                                           value=f"{doc['pos_emo']}")
                    i_pos_ani = gr.Textbox(max_lines=1, label="Animations",
                                           value=f"{doc['pos_ani']}")
                    i_pos_obj = gr.Textbox(max_lines=1, label="Objects",
                                           value=f"{doc['pos_obj']}")

                  with gr.Column():

                    gr.Markdown(value="Neg")

                    i_neg_emo = gr.Textbox(max_lines=1, label="Emotions",
                                           value=f"{doc['neg_emo']}")
                    i_neg_ani = gr.Textbox(max_lines=1, label="Animations",
                                           value=f"{doc['neg_ani']}")
                    i_neg_obj = gr.Textbox(max_lines=1, label="Objects",
                                           value=f"{doc['neg_obj']}")
                  # with gr.Column(scale=1):
                  #   pass
                    # with gr.Accordion("LoRA"):

                    #   with gr.Column():
                    #     # p_loraDetail = gr.Image()
                    #     gr.Slider(
                    #         minimum=-1,
                    #         maximum=2,
                    #         step=0.1,
                    #         value=0,
                    #         label="Detail Tweaker",
                    #     )

                    # with gr.Column(scale=1):
                    #   with gr.Accordion("Advanced"):

                    #     with gr.Column():
                    #       with gr.Row():
                    #         gr.Checkbox(
                    #             label="IPadapter (This will take much time)", scale=1)
                    #         # gr.Textbox(value="This will take much time", scale=2)

              # Result
              with gr.Column(scale=3):
                o_img = gr.Image(format="png", type="pil", height=256)

                i_seq = gr.Textbox(visible=False, value=f"{doc['seq']}")

                with gr.Row():
                  i_gen = gr.Button(
                      value="Generate",
                      icon="./assets/icon/replay_24dp.png",
                  )
                  i_gen.click(fn=genEmote, inputs=[
                      charaInfo, c_ref_base64, i_pos_emo, i_neg_emo], outputs=[o_img])

                  i_savEmote_btn = gr.Button(
                      value="Save Result", icon="./assets/icon/new_label_24dp.png")
                  i_savEmote_btn.click(
                      fn=savEmote, inputs=[o_img, stateId, i_seq])

            # Advanced Settings
            #
            # - Quick Prompts
            # -- Camera
            # -- Lighting
            # -- Filter
            # - LoRA
            # - OpenPose
            with gr.Accordion(label="Advanced", open=False):
              with gr.Row():
                  # with gr.Column(scale=1):
                  #   pass
                # Quick Prompt
                with gr.Column(scale=7):
                  gr.Markdown(value="Camera")
                  gr.CheckboxGroup(show_label=False, choices=[
                                   "Close Up", "Zoom In", "Zoom Out", "Tilt Left", "Tilt Right", "Wide Angle", "High Angle", "Low Angle", "Overhead"])
                  gr.Radio(show_label=False, choices=[
                           "Side View", "Front View", "Back View"])

                  gr.Markdown(value="Lighting")
                  gr.Radio(show_label=False, choices=['Broad Lighting',
                                                      'Rim Lighting', 'Backlight', 'God Rays', 'Luminescent Effects', 'Caustics'])

                  gr.Markdown(value="Filter")
                  gr.CheckboxGroup(show_label=False, choices=[
                                   'Blue Hour', 'Golden Hour'])

                  # LoRA
                  with gr.Row():

                    pass

                # OpenPose
                with gr.Column(scale=3):
                  gr.Markdown(value="OpenPose")

                  gr.Image(type="pil", format="png", height=256)

          # Divider
          gr.Markdown(value="---")
          """"""

      # s_emoteSet.change(fn=listEmoteElements, inputs=s_emoteSet)

      # # Set up button interaction for generating emotes
      # gen_stickers_btn.click(
      #     genEmote,
      #     inputs=[charaInfo, s_emoteSet],
      #     outputs=[sticker_output],
      # )

      tab.select(fn=get_latest_folder, outputs=[i_uuid])
