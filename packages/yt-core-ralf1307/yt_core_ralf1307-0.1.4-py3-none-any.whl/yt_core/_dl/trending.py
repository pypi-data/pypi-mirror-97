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


def get(self):
    raw_json = getRawTrendingFeed()
    trending_json = parseTrendingFeedInitial(raw_json)
    return trending_json


def getRawTrendingFeed(self):
    return HTTP_Get(self.YT_Trending_URL, self.YT_Trending_Parameters, "", self.YT_Headers)


def parseTrendingFeedInitial(self, raw):
    trending_json = json.loads(raw)
    return trending_json
