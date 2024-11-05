from daos.api.sd import SDAPI


class EmoteDao:
    def __init__(self):
        self.set = {
            "set1": [
                {"code": "1", "pos": "(angry:1.1)", "neg": "blush"},
                {"code": "2", "pos": "(happy:1.2)", "neg": ""},
                {"code": "3", "pos": "(sleeping:1.2)", "neg": ""},
                {"code": "4", "pos": "(crying:0.8)", "neg": ""},
                {"code": "5", "pos": "(blush:1.2), (shy)", "neg": ""},
                {
                    "code": "6",
                    "pos": "(blush:1.2), (embarassed), flying sweatdrop",
                    "neg": "",
                },
                {"code": "7", "pos": "(panicking:1.2)", "neg": ""},
                {"code": "8", "pos": "(terrified:1.2)", "neg": ""},
                {"code": "9", "pos": "(drooling)", "neg": ""},
                {"code": "10", "pos": "(waving hello:1.2), (smiling:1.2)", "neg": ""},
                {"code": "11", "pos": "sad, frowning, gloomy, downcast", "neg": ""},
            ]
        }

    def getEmoteSetList(self):
        return {self.set.keys()}

    def genEmote(
        self, pos, neg, closeup, set="set1", style="chibi", seed=-1, wid=512, hgt=512
    ):

        sdAPI = SDAPI()

        gallery = []

        pos = pos + "<lora:chibi_emote_v1:1>, emote, "

        if closeup:
            pos = pos + "(close up:1.2), "

        for doc in self.set[set]:
            # For each,
            docpos = pos + doc["pos"]
            docneg = neg + doc["neg"]

            img, seed = sdAPI.genChara(docpos, docneg, style, seed, wid, hgt)

            gallery.append(img)

        return gallery

    # Append the positive prompt for emote generation
    def getPosByEmote(code, pos):
        None
