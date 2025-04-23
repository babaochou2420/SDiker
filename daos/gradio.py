
import gradio as gr


class GradioDao:
  def __init__(self): pass

  # Reverse the visibility status
  def revVisiblility(state: bool):

    rev = (not state)

    return gr.update(visible=rev), (not rev)

  def setValue(value):
    return gr.update(value=value)
