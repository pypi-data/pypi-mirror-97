#    This file is part of yt_core.
#
#    yt_core is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    yt_core is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with yt_core.  If not, see <http://www.gnu.org/licenses/>.
#

from .search import _search
# Need to rewrite the following
from .trending import get as _trending
from .video import get as _video

from .api import _continue

from .comments import _comments

from .localization import _get_countries, _get_languages


class Downloader:
    """You really shouldnt use this class outside of yt_core."""
    # FIXME: get latest info from youtube (this could be used to track the use of this library)
    YT_Headers = {
            'x-youtube-client-version': "2.20200918.05.01",
            'x-youtube-client-name': "1",
            "Accept-Language": "de-DE"  # Gets replaced.
            }

    YT_API_Base_URL = "https://www.youtube.com/youtubei/v1/"
    YT_API_Parameters = {"key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"}
    YT_API_Payload = {"context": {"client": {"clientName": "WEB",
                                             "clientVersion": "2.20201029.02.00"}}, "continuation": ""}  # FIXME: GET THIS VALUE DYNAMIC

    YT_Picker_Ajax_URL = "https://www.youtube.com/picker_ajax"
    YT_Picker_Ajax_Language = {'action_language_json': 1}
    YT_Picker_Ajax_Country = {'action_country_json': 1}

    # YT_Search_Parameters & YT_SearchContinue_Payload needs to be modiefied by the search class
    YT_Search_URL = "https://www.youtube.com/results"
    YT_Search_Parameters = {"search_query": "", "pbj": 1}

    YT_Search_Continue = {
            "url": YT_API_Base_URL + "search",
            "parameters": YT_API_Parameters.copy(),
            "payload": YT_API_Payload.copy()
            }

    YT_Trending_URL = "https://www.youtube.com/feed/trending"
    YT_Trending_Parameters = {"pbj": 1}

    YT_Watch_URL = "https://www.youtube.com/watch"
    YT_Watch_Parameters = {"v": "", "pbj": 1}

    YT_Next = {
        "url": YT_API_Base_URL + "next",
        "parameters": YT_API_Parameters.copy(),
        "payload": YT_API_Payload.copy()
    }
    YT_Comments_URL = "https://www.youtube.com/comment_service_ajax"
    YT_Comments_Parameters = {
        "action_get_comments": 1, "pbj": 1, "ctoken": ""}

    def __init__(self, core):
        self.core = core
    # Wrapper for files.

    def search(self, searchterm):
        return _search(self, searchterm)

    def search_continue(self, token):
        return _continue(self, self.YT_Search_Continue, token)

    def trending(self):
        return _trending(self)

    def video(self, videoId):
        return _video(self, videoId)

    def video_recommended(self, token):
        return _continue(self, self.YT_Next, token)

    def comments(self, token):
        return _comments(self, token)

    def local_language(self):
        return _get_languages(self)

    def local_country(self):
        return _get_countries(self)
