
"""
系統設定
"""

from beans_logging.auto import logger
import json
import gradio as gr

from daos.emote import EmoteDao

emoteDao = EmoteDao()


class settingsTab():

  def __init__(): pass

  def __load__():
    #
    # Functions
    #

    def setEmoteSet(file):
      return emoteDao.setEmoteSet(file)

    def delEmoteSet(key):
      return emoteDao.delEmoteSet(key)

    def updEmoteSet(key, jsonString):
      return emoteDao.updEmoteSet(key, jsonString)

    def getEmoteSet(key):
      return emoteDao.getEmoteSet(key)

    #
    # Widgets
    #

    i_setEmoteSet_btn = gr.Button(render=False, value="Upload Emote Set")
    # i_delEmoteSet_btn = gr.Button(render=False, scale=1,
    #                               icon="./assets/icon/delete_24dp.png", value="Delete")

    with gr.Tab("Settings") as tab:

      # Settings for emote-sets
      @gr.render(triggers=[tab.select, i_setEmoteSet_btn.click])
      def lstEmoteSetWidget():

        list = emoteDao.lstEmoteSets()

        logger.warning(list)

        for doc in list:
          with gr.Column(variant="panel"):
            with gr.Accordion(label=doc, open=False):
              with gr.Row():

                i_getEmoteSet_key = gr.Textbox(visible=False, value=doc)

                i_getEmoteSet_txt = gr.Code(scale=18, show_label=False, container=False, interactive=True,
                                            language="json", value=json.dumps(getEmoteSet(doc), indent=2, ensure_ascii=False))

                with gr.Column():
                  i_updEmoteSet_btn = gr.Button(scale=1, icon="./assets/icon/save_24dp.png",
                                                value="Save Changes")

                  i_updEmoteSet_btn.click(fn=updEmoteSet, inputs=[i_getEmoteSet_key,
                                          i_getEmoteSet_txt])

                  # i_delEmoteSet_btn.render()

                  i_delEmoteSet_btn = gr.Button(
                      scale=1, icon="./assets/icon/delete_24dp.png", value="Delete")

                  i_delEmoteSet_btn.click(
                      fn=delEmoteSet, inputs=[i_getEmoteSet_key])

      # setEmoteSet
      with gr.Row():
        with gr.Column():
          i_set_fil = gr.File(
              label="Upload New Emote Set (JSON)", type="filepath")

          i_setEmoteSet_btn.render()

          i_setEmoteSet_btn.click(fn=setEmoteSet, inputs=[i_set_fil])

        with gr.Column():

          s_set_example = {"set_name": [{"seq": "SEQUANCE in SET",
                                         "pos_emo": "EMOTION", "pos_ani": "ANIMATION", "pos_obj": "OBJECT",
                                         "neg_emo": "EMOTION", "neg_ani": "ANIMATION", "neg_obj": "OBJECT",
                                         },
                                        {"seq": "SEQUANCE in SET",
                                         "pos_emo": "EMOTION", "pos_ani": "ANIMATION", "pos_obj": "OBJECT",
                                         "neg_emo": "EMOTION", "neg_ani": "ANIMATION", "neg_obj": "OBJECT",
                                         },
                                        ]}

          gr.Code(value=json.dumps(s_set_example, indent=2,
                  ensure_ascii=False), label="ex")
