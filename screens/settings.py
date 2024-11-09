
import gradio as gr


class settingsTab():

  def __init__(): pass

  def __load__():

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
