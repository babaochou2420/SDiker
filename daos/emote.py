from beans_logging.auto import logger
import shutil
import zipfile
import uuid
import os
import io
import json
from daos.api.sd import SDAPI

import requests
import base64

from PIL import Image

from daos.image import ImageDao
from utils.config import Config

config = Config.get_config()


class EmoteDao:
  def __init__(self):
    self.json_dir = './assets/json'

  def setPrompt(self, closeup, pos, neg, docpos, docneg):

    pos = pos + "emote, "

    if closeup:
      pos = pos + "(close up:1.2), "

    pos += docpos
    neg += docneg

    return pos, neg

  #
  # Emote
  #

  def genEmote(self, ref_base64, pos, neg, style, seed, wid, hgt):

    # First time using old seed
    # Afterwards time using random seed

    # Define the WebUI API URL for txt2img
    api_url = config["API"]["SDWebUI"] + "/sdapi/v1/txt2img"

    ref_base64 = base64.b64encode(ref_base64).decode("utf-8")

    # Prepare the payload with ControlNet parameters for the 'reference' module using 'adain+attn'
    payload = {
        "prompt": pos,
        "negative_prompt": neg,
        "styles": [style],
        "width": wid,
        "height": hgt,
        #
        "seed": seed,
        #
        "steps": 20,
        "sampler_name": "Euler a",
        "cfg_scale": 7.0,
        #
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "enabled": True,
                        "image": ref_base64,
                        "weight": 1,
                        "resize_mode": "Envelope (Outer Fit)",
                        "module": "reference_adain+attn",
                        "processor_res": wid,
                        "control_mode": "My prompt is more important",
                    }
                ]
            }
        },
    }

    image, _, _ = SDAPI.genTXT2IMG(payload)

    return image

  def savEmote(self, image: Image.Image, uuid, seq: int) -> str:

    filPath = os.path.join('./archive', str(uuid), f'{seq}.png')

    ImageDao.savImagePIL(image, uuid, filPath)

  #
  # Export
  #

  # Output the pack as zip
  def savEmoteZip(self, uuid):
    # Define the folder path based on the UUID
    folder_path = os.path.join('./archive', uuid)

    # Check if the folder exists
    if not os.path.isdir(folder_path):
      return f"Directory not found for UUID: {uuid}"

    export_folder = os.path.join('./archive', uuid, '# export')
    os.makedirs(export_folder, exist_ok=True)

    # Define the zip file path
    zip_path = os.path.join(export_folder, f"SDiker_{uuid}.zip")

    # Create a zip file and add all PNG files from the directory
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
      for root, _, files in os.walk(folder_path):
        for file in files:
          if file.endswith(".png"):
            file_path = os.path.join(root, file)
            # Add file to zip with relative path to avoid full path structure
            zipf.write(file_path, os.path.relpath(file_path, folder_path))

    # Return the path to the zip file for download
    return zip_path

  # Output the pack as grids
  def savEmoteGrid(self, uuid, col, row):
    # Define the folder path based on the UUID
    folder_path = os.path.join('./archive', uuid)

    # Check if the folder exists
    if not os.path.isdir(folder_path):
      return f"Directory not found for UUID: {uuid}"

    export_folder = os.path.join('./archive', uuid, '# export')
    os.makedirs(export_folder, exist_ok=True)

    # Collect all PNG files, sort by name
    png_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith('.png')], key=lambda x: int(x.rstrip('.png')))

    # Calculate the total number of grids required
    total_images = len(png_files)
    max_per_grid = col * row
    # Round up to ensure all images fit
    grid_count = (total_images + max_per_grid - 1) // max_per_grid

    output_paths = []

    for grid_index in range(grid_count):
      # Start and end indices for the images in this grid
      start_idx = grid_index * max_per_grid
      end_idx = min(start_idx + max_per_grid, total_images)

      # Create a blank canvas based on image dimensions and grid size
      first_image = Image.open(os.path.join(folder_path, png_files[start_idx]))
      img_width, img_height = first_image.size
      grid_width = col * img_width
      grid_height = row * img_height
      grid_image = Image.new('RGBA', (grid_width, grid_height))

      # Place images into the grid
      for i, img_name in enumerate(png_files[start_idx:end_idx]):
        img = Image.open(os.path.join(folder_path, img_name))
        x = (i % col) * img_width
        y = (i // col) * img_height
        grid_image.paste(img, (x, y))

      # Save the grid image
      grid_filename = os.path.join(
          export_folder, f"SDiker_grid_{uuid}_{grid_index + 1}.png")
      grid_image.save(grid_filename, "PNG")
      output_paths.append(grid_filename)

    return output_paths

  #
  # Emote Set
  #

  def lstEmoteSets(self):

    logger.warning("# RUN - lstEmoteSets()")

    if not os.path.isdir(self.json_dir):
      return []

    result = [os.path.splitext(filename)[0] for filename in os.listdir(
        self.json_dir) if filename.endswith(".json")]

    logger.info(result)

    logger.warning("# END - lstEmoteSets()")

    return result

  def getEmoteSets(self):
      # Log start of function
    logger.warning("# RUN - getEmoteSets()")

    # Get list of JSON filenames (without extension)
    filenames = self.lstEmoteSets()

    # Initialize a dictionary to hold all JSON contents
    combined_data = {}

    # Loop through filenames and add each JSON content to the combined_data dictionary
    for name in filenames:
      data = self.getEmoteSet(name)
      if data is not None:
        # Store each JSON content under its filename key
        combined_data[name] = data

    # Log end of function
    logger.warning("# END - getEmoteSets()")

    return combined_data

  # Fetch the emote-set
  def getEmoteSet(self, keyname):
    """
    Load the JSON file and return its content as a dictionary.
    """
    file_path = os.path.join(self.json_dir, f"{keyname}.json")

    if not os.path.isfile(file_path):
      return f"File not found for keyname: {keyname}"

    with open(file_path, 'r', encoding='utf-8') as file:
      data = json.load(file)

    return data

  # Update the emote-set
  def updEmoteSet(self, keyname, json_string):
    """
    Update the JSON file with the provided JSON string.
    """
    file_path = os.path.join(self.json_dir, f"{keyname}.json")

    try:
      # Parse JSON string
      data = json.loads(json_string)

      # Write the updated data to the file
      with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

      return f"{keyname}.json has been updated successfully."

    except json.JSONDecodeError:
      return "Invalid JSON format."

  # Delete the emote-set
  def delEmoteSet(self, keyname):
    """
    Delete the specified JSON file.
    """
    file_path = os.path.join(self.json_dir, f"{keyname}.json")

    if os.path.isfile(file_path):
      os.remove(file_path)
      return f"{keyname}.json has been deleted successfully."
    else:
      return f"File not found for keyname: {keyname}"

  # Upload the emote-set
  def setEmoteSet(self, uploaded_file):
    """
    Upload a JSON file, saving a copy in the same directory with the key name from the JSON content.
    """
    # Ensure the file is in JSON format
    if not uploaded_file.name.endswith('.json'):
      return "Please upload a JSON file."

    try:
      # Load the content of the JSON file to extract the key name
      with open(uploaded_file.name, 'r', encoding='utf-8') as file:
        data = json.load(file)

      # Assuming the JSON is in the format {"key_name": ...}
      key_name = list(data.keys())[0]

      # Construct the new file path with the key name as the file name
      new_file_path = os.path.join(self.json_dir, f"{key_name}.json")

      # Copy the uploaded file to the specified directory with the new name
      shutil.copy(uploaded_file.name, new_file_path)

      return f"{key_name}.json has been created successfully in {self.json_dir}."

    except json.JSONDecodeError:
      return "Uploaded file is not a valid JSON."
    except Exception as e:
      return f"Error saving file: {e}"
