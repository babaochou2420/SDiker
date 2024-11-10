
""" 
貼圖生成
"""

from beans_logging.auto import logger
import json
import gradio as gr

from daos.chara import CharaDao
from daos.emote import EmoteDao

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

      img = emoteDao.genEmote(ref_base64, pos, neg, style, seed, wid, hgt)

      return img

    def savEmote(img, uuid, seq):
      emoteDao.savEmote(img, uuid, seq)

    #
    # Widgets
    #
    with gr.Tab("Step 2. Gen Sticker") as tab:

      s_emoteSet = gr.Dropdown(
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
          with gr.Row(variant="panel"):
            with gr.Column(scale=2):
              # with gr.Row():
              #   f_seq = gr.Textbox(
              #       value=f"Seq: {doc['code']}", container=False)

              o_img = gr.Image(format="png", type="pil")

              i_seq = gr.Textbox(value=f"{doc['code']}")

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
                    i_savEmote_btn = gr.Button(
                        value="Save Result", icon="./assets/icon/new_label_24dp.png")

                    i_savEmote_btn.click(
                        fn=savEmote, inputs=[o_img, stateId, i_seq])
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

      # s_emoteSet.change(fn=listEmoteElements, inputs=s_emoteSet)

      # # Set up button interaction for generating emotes
      # gen_stickers_btn.click(
      #     genEmote,
      #     inputs=[charaInfo, s_emoteSet],
      #     outputs=[sticker_output],
      # )
