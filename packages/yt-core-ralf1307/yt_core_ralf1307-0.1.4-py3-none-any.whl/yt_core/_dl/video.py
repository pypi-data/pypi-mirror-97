import json
from ._download import get as HTTP_Get


def get(self, Id):
    try:
        checkId(self, Id)
        raw_json = getRawResponse(self, Id)
        parsed_json = parseInital(self, raw_json)
    except:
        raise
    return parsed_json


def checkId(self, Id):
    return True


def getRawResponse(self, Id):
    video_parameters = self.YT_Watch_Parameters.copy()
    video_parameters["v"] = Id
    return HTTP_Get(self.YT_Watch_URL, video_parameters, "", self.YT_Headers)


def parseInital(self, raw_json):
    # FIXME: implement checks if valid response (if not throw error)
    result = json.loads(raw_json)
    return result
