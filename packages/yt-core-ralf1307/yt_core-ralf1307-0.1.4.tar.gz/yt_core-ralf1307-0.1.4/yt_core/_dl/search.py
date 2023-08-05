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

import json

from ._download import get as HTTP_Get
from ._download import post as HTTP_Post


def _search(self, searchterm):
    try:
        _check_search_term(self, searchterm)
        raw_json = _get_raw_initial(self, searchterm)
        search_json = _parse_inital(self, raw_json)
    except:
        raise
    return search_json


def _search_continue(self, continue_token):
    try:
        raw_json = _get_raw_continue(self, continue_token)
        continue_json = _parse_continue(self, raw_json)
    except:
        raise
    return continue_json


def _check_search_term(self, searchterm):
    # Returns true if searchterm is valid

    # This code shouldnt fail. If it does, someone is programming wrong.
    if(len(searchterm) == 0):
        raise ValueError
    return True


def _get_raw_initial(self, searchterm):
    search_parameters = self.YT_Search_Parameters.copy()
    search_parameters["search_query"] = searchterm
    return HTTP_Get(self.YT_Search_URL, search_parameters, "", self.YT_Headers)


def _get_raw_continue(self, continueToken):
    payload = self.YT_SearchContinue_Payload.copy()
    payload["continuation"] = continueToken
    return HTTP_Post(self.YT_SearchContinue_URL, self.YT_SearchContinue_Parameters, json.dumps(payload), self.YT_Headers)


def _parse_inital(self, raw_json):
    # FIXME : implement checks if valid response (if not throw error)
    result = json.loads(raw_json)
    return result


def _parse_continue(self, raw_json):
    # FIXME : implement checks if valid response (if not throw error)
    result = json.loads(raw_json)
    return result
