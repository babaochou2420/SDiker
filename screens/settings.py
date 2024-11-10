
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

    def getEmoteSet(key):
      return emoteDao.getEmoteSet(key)

    #
    # Widgets
    #

    with gr.Tab("Settings") as tab:

      @gr.render(triggers=[tab.select])
      def build():

        list = emoteDao.lstEmoteSets()

        logger.warning(list)

        for doc in list:
          with gr.Column(variant="panel"):
            with gr.Accordion(label=doc, open=False):
              with gr.Row():
                gr.Code(scale=18, show_label=False, container=False, interactive=True,
                        language="json", value=json.dumps(getEmoteSet(doc), indent=4, ensure_ascii=False))

                with gr.Column():
                  gr.Button(scale=1, icon="./assets/icon/save_24dp.png",
                            value="Save Changes")
                  gr.Button(scale=1, icon="./assets/icon/delete_24dp.png",
                            value="Delete")

      # Delete and edit buttons
      with gr.Row():
        delete_button = gr.Button("Delete Selected Emote Set")
        refresh_button = gr.Button("Refresh List")

      # Upload new emote set
      with gr.Row():
        json_upload = gr.File(
            label="Upload New Emote Set (JSON)", type="filepath")
        upload_button = gr.Button("Upload Emote Set")
