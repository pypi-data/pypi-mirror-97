#
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
from . import _helper as helper
from ._BaseClass import BaseClass
from ._BaseClass import InvalidFilterError

_filter_dict = {
        "upload": [
            "lasthour",
            "today",
            "week",
            "month",
            "year"
            ],
        "type": [
            "video",
            "channel",
            "playlist",
            "movie",
            "show"
            ],
        "length": [
            "short",
            "long"
            ],
        "features": [
            "live",
            "4K",
            "HD",
            "Subtitles",
            "Creative Commons",
            "360",
            "VR180",
            "3D",
            "HDR",
            "Location",
            "Purchased"
            ],
        "sorting": [
            "relevance",
            "upload",
            "view",
            "rating"
            ],
        "other": [
            "force"
            ]
    }


class Search(BaseClass):
    def __init__(self, core, searchterm="", filters=list()):
        self._dl = core._dl
        self.searchterm = searchterm
        error, invalid_filter = self.check_filter(filters)
        # FIXME: CUSTOM ERROR CLASSES
        if not error:
            self._filter = filters
        else:
            self._error_invalid_filter(invalid_filter)

    def _soft_reset(self):
        # User-Info:
        self._searched = False
        self._continueable = False
        self._suggestedSearch = False
        self._replacedSearch = False
        self._suggestedQuery = ""
        self._recommendedAvailable = False
        self._recommendedSearchTerms = []
        self._estimatedResults = 0

        # Interal
        self.__applied_filters = dict()
        self.__request_raw = None
        self.__continue_raw = None
        self.__continue_token = ""

        # Data
        self._response = []

    def is_searched(self):
        return self._searched

    def is_continuable(self):
        return self._continueable

    def is_suggesting_query(self):
        return self._suggestedSearch

    def is_replaced_with_suggestion(self):
        return self._replacedSearch

    def get_suggestion_query(self):
        return self._suggestedQuery

    def has_recommended_queries(self):
        return self._recommendedAvailable

    def get_recommended_queries(self):
        return self._recommendedSearchTerms

    def get_results_count_total(self):
        return self._estimatedResults

    def get_results(self):
        return self._response

    def has_errors(self):
        if len(self._error) > 0:
            return True
        else:
            return False

    def get_errors(self):
        return self._error

    searchterm = ""
    _filter = None

    _core = None

    def _get_response(self, parameters=dict()):
        self.__request_raw = self._dl.search(self.searchterm)
        # We do a bit of parsing here:

    def _get_continue(self):
        self.__continue_raw = self._dl.search_continue(self.__continue_token)

    __applied_filters = dict()

    # Recommendation: use vim and :q!
    def _parse_response(self):
        def responseRaw():
            for i in self.__request_raw:
                if "response" in i:
                    responseRaw = i["response"]
            if "refinements" in responseRaw:
                self._recommendedAvailable = True
                self._recommendedSearchTerms = responseRaw["refinements"]
            return responseRaw

        def sectionListRaw():
            contentRaw = raw["contents"]
            primaryContentRaw = contentRaw["twoColumnSearchResultsRenderer"]["primaryContents"]
            sectionListRaw = primaryContentRaw["sectionListRenderer"]
            return sectionListRaw, raw

        raw = responseRaw()
        sec_list, raw = sectionListRaw()
        sectionListContentsRaw = sec_list["contents"]
        self._response, info = helper.parseContent(sectionListContentsRaw)
        for i in info:
            # switch; case; break; thats one feature i miss in python
            if i["type"] == "suggestedQuery":
                self._suggestedSearch = True
                self._suggestedQuery = i["suggestion"]
            elif i["type"] == "replacedQuery":
                self._replacedSearch = True
                self._suggestedQuery = i["suggestion"]
            elif i["type"] == "continuation":
                self._continueable = True
                self.__continue_token = i["token"]
            elif i["type"] == "error":
                # If we have an error, just give all the info the parser returns with it
                self._error_parsing_failure(info)

    def _parse_continue_response(self):
        self._continueable = False
        parsed, info, mode = helper.parse_continue_response(
            self.__continue_raw)
        if mode == "append":
            for p in parsed:
                self._response.append(p)
        elif mode == "error":
            if self.__continue_raw["estimatedResults"] == 0:
                self._error_no_more_results()
            return list()
        for i in info:
            if i["type"] == "continuation":
                self._continueable = True
                self.__continue_token = i["token"]
        return parsed

    # FIXME: CHECKS FOR VALID RESULT
    # FIXME: More checks.
    # FIXME: Write into self.errormsg
    # Returns True if everything is valid. Otherwise False
    def _check_inital(self):
        error = False
        if not self.check_searchterm(self.searchterm):
            self._error_invalid_input(self.searchterm)
            error = True
        if not self.check_filter(self._filter):
            self._error_invalid_filter(self._filter)
            error = True
        if error:
            self.throw_error()

    def _check_inital_end(self):
        if(self._check_response()):
            return True
        return False

    def _check_response(self):
        if(len(self._response) > 0):
            return True
        return False

    # Methods

    def search(self):
        self._soft_reset()
        self._check_inital()
        self._get_response()
        self._parse_response()
        self._searched = True
        return self._response

    def search_continue(self):
        self._get_continue()
        response = self._parse_continue_response()
        return response

    def throw_error(self):
        if self._error:
            out = ""
            for i in self._error:
                out += "+ " + i
            Exception(out)

    @staticmethod
    def check_searchterm(searchterm):
        if(len(searchterm) > 0):
            return True
        return False

    @staticmethod
    def check_filter(filters):
        invalid = list()
        for i in filters:
            for u in _filter_dict:
                if not i in u:
                    invalid.append(i)
        if len(invalid) == 0:
            return False, invalid
        else:
            return True, invalid

    @staticmethod
    def get_filters_by_category(category):
        return _filter_dict[category.lower()]

    @staticmethod
    def get_filters():
        out = []
        for i in _filter_dict:
            for u in i:
                out.append(u)
        return out

    @staticmethod
    def get_categories():
        return list(_filter_dict)
