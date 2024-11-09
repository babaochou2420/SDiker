
import gradio as gr

from daos.emote import EmoteDao

emoteDao = EmoteDao()


class savEmoteTab():

  def __init__(): pass

  def __load__():

    #
    # Functions
    #
    def savEmoteZip(uuid):
      return emoteDao.savEmoteZip(uuid)

    #
    # Widgets
    #
    with gr.Tab("Step 3. Output"):

      i_uuid = gr.Textbox(label="UUID")

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

      compress_button.click(
          fn=savEmoteZip,
          inputs=[i_uuid],
          outputs=[zip_image_output]
      )
