#   https://www.youtube.com/comment_service_ajax?action_get_comments=1&pbj=1&ctoken=EkMSC2JuVGQ2aTVrSzRVMgDIAQDgAQGiAg0o____________AUAAwgIbGhdodHRwczovL3d3dy55b3V0dWJlLmNvbSIAGAY%3D&continuation=EkMSC2JuVGQ2aTVrSzRVMgDIAQDgAQGiAg0o____________AUAAwgIbGhdodHRwczovL3d3dy55b3V0dWJlLmNvbSIAGAY%3D&itct=CJEBEMm3AiITCNeXs_eUuu0CFQjaVQod940Dsg==

import json
from ._download import post as HTTP_Post


def _comments(self, token):
    try:
        raw_json = _get_raw(self, token)
        continue_json = _parse_continue(self, raw_json)
    except:
        raise
    return continue_json


def _get_raw(self, token):
    parameters = self.YT_Comments_Parameters.copy()
    parameters["ctoken"] = token
    return HTTP_Post(self.YT_Comments_URL, parameters=parameters, headers=self.YT_Headers)

def _parse_continue(self, raw_json):
    # FIXME : implement checks if valid response (if not throw error)
    result = json.loads(raw_json)
    return result
