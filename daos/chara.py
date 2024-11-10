from beans_logging.auto import logger


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
