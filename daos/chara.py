import base64
import io
import os
from beans_logging.auto import logger
from PIL import Image

from daos.image import ImageDao


class CharaDao:
  def __init__(self):
    pass

  def getChara(self, charaInfo):
    # # Debugging
    # logger.warning(charaInfo)
    # logger.warning(type(charaInfo))

    return (
        charaInfo["pos"],
        charaInfo["neg"],
        charaInfo["style"],
        charaInfo["seed"],
        charaInfo["wid"],
        charaInfo["hgt"],
    )

  def genChara():
    pass

  def savChara(image_bin, uuid):

    dirPath = os.path.join('./archive', str(uuid))

    os.makedirs(dirPath, exist_ok=True)

    filPath = os.path.join(dirPath, '0.png')

    ImageDao.savImageBIN(image_bin, filPath)
