
""" 
成品輸出
"""

import gradio as gr

from daos.emote import EmoteDao

emoteDao = EmoteDao()


class expEmoteTab():

  def __init__(): pass

  def __load__():

    #
    # Functions
    #
    def savEmoteGrid(uuid, col, row):
      return emoteDao.savEmoteGrid(uuid, col, row)

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
            i_grd_btn = gr.Button(
                "Grid Layout", icon="./assets/icon/grid_view_24dp.png", scale=3)
            i_col = gr.Dropdown(
                choices=[3, 4],
                value=3, scale=1, show_label=False, container=False
            )
            i_row = gr.Dropdown(
                choices=[3, 4],
                value=3, scale=1, show_label=False, container=False
            )

          o_grd_img = gr.Gallery(
              label="Grid Layout Preview",
              show_label=True,
          )

          i_grd_btn.click(fn=savEmoteGrid, inputs=[
              i_uuid, i_col, i_row], outputs=[o_grd_img])

        # File
        with gr.Column(variant="panel"):
          i_zip_btn = gr.Button(
              "File Output", icon="./assets/icon/output_circle_24dp.png")

          o_zip = gr.File(value=None)

      # # Define button click actions
      # grid_button.click(
      #     fn=generate_grid_layout,
      #     inputs=[grid_layout_dropdown],
      #     outputs=[grid_image_output]
      # )

      i_zip_btn.click(
          fn=savEmoteZip,
          inputs=[i_uuid],
          outputs=[o_zip]
      )
