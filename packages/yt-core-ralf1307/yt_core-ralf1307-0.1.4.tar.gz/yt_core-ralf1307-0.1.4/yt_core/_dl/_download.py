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

import requests
# It's my intention not to use Requests.json, as i had some bugs (or most likly user error)
# (i want to replace Requests later (in a long future), as i want to reduce the dependencies)


def get(url=str(), parameters=dict(), data=str(), headers=dict()):
    # example: https://example.org/someurl?parameterone=1234  HTTP-Header
    #          ----------url-------------- ---parameters----  --headers--
    request = requests.get(url, params=parameters, headers=headers)
    request.raise_for_status()  # Raises Expetion if not OK
    return request.text


def post(url=str(), parameters=dict(), data=str(), headers=dict()):
    request = requests.post(url, data=data, params=parameters, headers=headers)
    request.raise_for_status()
    return request.text
