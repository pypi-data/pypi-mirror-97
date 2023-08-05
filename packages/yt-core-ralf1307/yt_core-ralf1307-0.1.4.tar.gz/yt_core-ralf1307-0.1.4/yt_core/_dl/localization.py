import json
from ._download import get as HTTP_Get


def _get_languages(self):
    try:
        # Including the youtube headers could reduce tracking potential?
        raw_json = HTTP_Get(url=self.YT_Picker_Ajax_URL,
                            parameters=self.YT_Picker_Ajax_Language, headers=self.YT_Headers)
        return json.loads(raw_json)
    except:
        raise


def _get_countries(self):
    try:
        raw_json = HTTP_Get(url=self.YT_Picker_Ajax_URL,
                            parameters=self.YT_Picker_Ajax_Country, headers=self.YT_Headers)
        return json.loads(raw_json)
    except:
        raise
