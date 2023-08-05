from . import _helper as helper
#from ._Comments import Comments


class Video:
    def __init__(self, core, video_id):
        # FIXME: Check if valid videoID
        self._dl = core._dl
        self._video_id = video_id
        self.__get_inital()
        self.__parse_inital()
        self.check_everything()

    # Info:
    _autoplay = False
    _recommended_continuable = False
    _error = []

    # Data:
    _video_id = ""
    _metadata = {}
    _autoplay_data = {}  # has a "type":"video"
    _recommended = []
    _player = {}

    comments = None  # object of Comments

    # Internal Data:
    __request_raw = None
    __continue_raw_recommended = None
    __continue_token_recommended = ""

    def is_recommended_available(self):
        if len(self._recommended) == 0:
            return False
        return True

    def get_recommended(self):
        return self._recommended

    def is_recommended_continuable(self):
        return self._recommended_continuable

    def recommended_continue(self):
        self.__get_recommended_continue()
        return self.__parse_recommended_continue()

    def get(self):
        return self._player

    def is_autoplay_available(self):
        return self._autoplay

    def get_autoplay(self):
        return self._autoplay_data

    def get_metadata(self):
        return self._metadata

    def __get_inital(self):
        self.__request_raw = self._dl.video(self._video_id)

    def __get_recommended_continue(self):
        self.__continue_raw_recommended = self._dl.video_recommended(
            self.__continue_token_recommended)

    def __parse_inital(self):
        def parse_player(player_raw):
            self._player = {
                    "type": "playBack",
                    "Id": self._video_id,
                    "OK": False,
                    "status": "",
                    "video": [],
                    "captions": None  # currently no datatype
                    }

            player_status = player_raw["playabilityStatus"]
            self._player["status"] = player_status["status"]
            if player_status["status"] == "OK":
                player_response = player_raw["streamingData"]
                if "formats" in player_response:
                    # We dont use adaptiveFormats, so were only supporting a small list of options
                    # (adaptiveFormats or something similar is apparently deemed piracy-protection by the RIAA. Thats BS.)
                    video_formats_static = player_response["formats"]
                    if len(video_formats_static) > 0:
                        self._player["OK"] = True
                        # FIXME: do we need to parse this or can we rely on youtube bringing the right format?
                        self._player = video_formats_static

           # def helper():
            #   def resolution():
             #       pass
              #  pass

        def parse_recommended(recommended_raw):
            results = recommended_raw["results"]
            self._recommended, info = helper.parseContent(results)
            for i in info:
                if i["type"] == "autoplay":
                    self._autoplay = True
                    self._autoplay_data = i["autoplay"]
                elif i["type"] == "continuation":
                    self._recommended_continuable = True
                    self.__continue_token_recommended = i["token"]

        def parse_comment(data):
            if "continuations" in data:
                for item in data["continuations"]:
                    if "nextContinuationData" in item:
                        pass
                        #self.comments = Comments(self._dl, token=item["nextContinuationData"]["continuation"])

        def parse_metadata_primary(data):
            out = {
                "title": "",
                "viewCountText":"",
                "likePercentage": 50, 
                "likeDislikeText": "",
                "hashtags": [],
                "dateText": ""
                }
            if "title" in data:
                out["title"] =  helper.getText(data["title"])
            # Legacy: viewCountText is depreacted by youtube. remove me pls in a few weeks
            if "viewCountText" in data:
                out["viewCountText"] = data["viewCount"]["videoViewCountRenderer"]["viewCount"]["simpleText"]
            elif "viewCount" in data:
                out["viewCountText"] = helper.videoViewCountRenderer(data["viewCount"])
            if "sentimentBar" in data:
                out["likePercentage"] = data["sentimentBar"]["sentimentBarRenderer"]["percentIfIndifferent"]
                out["likeDislikeText"] = data["sentimentBar"]["sentimentBarRenderer"]["tooltip"]
            if "superTitleLink" in data:
                for item in data["superTitleLink"]["runs"]:
                    if item["text"] != " ":
                        out["hashtags"].append(item["text"])
            if "dateText" in data:
                out["dateText"] = helper.getText(data["dateText"])
            return out

        def parse_metadata_secondary(data):
            out = {
                    "description": helper.getText(data["description"]),
                    "owner": helper.videoOwnerRenderer(data["owner"]["videoOwnerRenderer"])
            }
            return out

        def parse_metadata(d1, d2):
            out = {
                    "type":"metadata",
                    "metatype": "video",
                    }
            out = {**out, **d1, **d2}
            return out
        
        for i in self.__request_raw:
            if len(self._error) != 0:
                break
            if "preconnect" in i:
                pass  # FIXME: Most likly contains URLs to check for connection
                # (needed if user has bad networking)
            elif "playerResponse" in i:
                parse_player(i["playerResponse"])
            elif "timing" in i:
                pass  # Could be interesting (debug output?)
            elif "response" in i:
                contents = i["response"]["contents"]["twoColumnWatchNextResults"]
                if "results" in contents:  # Metadata like Video Title...
                    # Will break if youtube changes something
                    # Buts its faster.
                    # If we have a dynamic parser for YT_Headers FIXME
                    metadata_raw = contents["results"]["results"]["contents"]
                    metadata_primary = {}
                    metadata_secondary = {}
                    for item in metadata_raw:
                        if "videoPrimaryInfoRenderer" in item:
                            metadata_primary = parse_metadata_primary(item["videoPrimaryInfoRenderer"])
                        if "videoSecondaryInfoRenderer" in item:
                            metadata_secondary = parse_metadata_secondary(item["videoSecondaryInfoRenderer"])
                        elif "merchandiseShelfRenderer" in item:
                            pass
                        elif "itemSectionRenderer" in item:
                            parse_comment(item["itemSectionRenderer"])
                    self._metadata = parse_metadata(metadata_primary, metadata_secondary)
                if "secondaryResults" in contents:  # What to watch next
                    parse_recommended(
                        contents["secondaryResults"]["secondaryResults"])
                
                pass  # needs further parsing in __parseRecommended and __parseMetadata
            else:
                pass  # Unknown keys, # FIXME: log if this case occurs

    def __parse_recommended_continue(self):
        self._recommended_continuable = False
        parsed, info, mode = helper.parse_continue_response(
            self.__continue_raw_recommended)
        if mode == "append":
            self._recommended.append(parsed)
        for i in info:
            if i["type"] == "continuation":
                self._recommended_continuable = True
                self.__continue_token_recommended = i["token"]
        return parsed

    # FIXME

    def check_everything(self):
        pass
    # FIXME

    def check_response(self):
        pass
    # FIXME

    @staticmethod
    def checkId(videoId):
        return True  # FIXME: Currently defaults to True, implement the check
