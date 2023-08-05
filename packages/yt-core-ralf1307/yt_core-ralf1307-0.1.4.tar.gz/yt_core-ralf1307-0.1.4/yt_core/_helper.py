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

# helps parsing stuff:
def decodeCharacters(data):
    # FIXME: decode Characters. currently hardcoded to fix specific case.
    # return data.removesuffix("%3D") #python 3.9 and im not using it yet
    return data.replace("%3D%3D", "%3D")


def getText(text, navpoint_enable=True):
    out = ""
    navpoint = dict()
    if "runs" in text:
        u = text["runs"]
        for i in u:
            out += i["text"]
            if "navigationEndpoint" in i:
                navpoint = i["navigationEndpoint"]
    elif "simpleText" in text:
        out = text["simpleText"]
    else:
        raise Exception
    if len(navpoint) == 0:
        return out
    else:
        if navpoint_enable:
            return out, navpoint
        else:
            return out

# Needed for Search.metadata


def videoOwnerRenderer(videoOwnerRenderer):
    out = {
        "type": "owner",
        "Id": videoOwnerRenderer["navigationEndpoint"]["browseEndpoint"]["browseId"],
        "title": getText(videoOwnerRenderer["title"], navpoint_enable=False),
        "thumbnail": thumbnail(videoOwnerRenderer["thumbnail"]["thumbnails"]),
        "subscriberCountText": getText(videoOwnerRenderer["subscriberCountText"])
    }
    return out


def thumbnail(thumbnail):
    array = {
        "type": "thumbnail",
        "width": 0,
        "height": 0,
        "url": ""
    }
    out = []
    for x in thumbnail:
        a = array.copy()
        a["width"] = x["width"]
        a["height"] = x["height"]
        a["url"] = x["url"]  # FIXME: parse URL to remove tracking info if any
        out.append(a)
    return out

# Response block


def videoRenderer(videoRenderer, compact):
    out = {
        "type": "video",
        "Id": videoRenderer["videoId"],
        "thumbnail": thumbnail(videoRenderer["thumbnail"]["thumbnails"]),
        "title": getText(videoRenderer["title"]),
        "description": "",
        "viewCountText": getText(videoRenderer["viewCountText"]),
        "publishedTimeText": "",
        "lengthText": "",
        "ownerText": "",
        "ownerId": "",
    }
    # videos of a special kind dont include publishedTimeText and some other stuff
    try:
        out["publishedTimeText"] = getText(videoRenderer["publishedTimeText"])
    except:
        pass
    try:
        out["lengthText"] = getText(videoRenderer["lengthText"])
    except:
        pass
    if compact is True:
        # Got removed from YT while development
        if "longBylineText" in videoRenderer:
            out["ownerText"], navpoint = getText(
                videoRenderer["longBylineText"])
    else:
        if "descriptionSnippet" in videoRenderer:
            out["description"] = getText(videoRenderer["descriptionSnippet"])
        out["ownerText"], navpoint = getText(videoRenderer["ownerText"])
    out["ownerId"] = navpoint["browseEndpoint"]["browseId"]
    return out


def channelRenderer(channelRenderer):
    out = {
        "type": "channel",
        "Id": channelRenderer["channelId"],
        "thumbnail": thumbnail(channelRenderer["thumbnail"]["thumbnails"]),
        "title": channelRenderer["title"]["simpleText"],
        "subscriberCountText": channelRenderer["subscriberCountText"]["simpleText"],
        "videoCountText": getText(channelRenderer["videoCountText"])
    }
    if "descriptionSnippet" in channelRenderer:
        out["description"] = getText(channelRenderer["descriptionSnippet"])

    return out


def playlistRenderer(playlistRenderer):
    out = {
        "type": "playlist",
        "Id": playlistRenderer["playlistId"],
        "thumbnail": thumbnail(playlistRenderer["thumbnails"][0]["thumbnails"]),
        "title": playlistRenderer["title"]["simpleText"],
        "ownerText": getText(playlistRenderer["shortBylineText"]),
        "videoCountText": playlistRenderer["videoCount"]
    }
    return out


def compactAutoplayRenderer(autoplayRenderer):
    out = {
        "type": "autoplay",
        "autoplay": videoRenderer(autoplayRenderer["contents"][0]["compactVideoRenderer"], True)
    }
    return out


# Info block

def didYouMeanRenderer(didYouMeanRenderer):
    out = {
        "type": "suggestedQuery",
        "suggestion": getText(didYouMeanRenderer["correctedQuery"])
    }
    return out


def showingResultsForRenderer(showingResultsForRenderer):
    out = {
        "type": "replacedQuery",
        "suggestion": getText(showingResultsForRenderer["correctedQuery"]),
    }
    return out


def continuationItemRenderer(continuationItemRenderer):
    out = {
        "type": "continuation",
        "token": continuationItemRenderer["continuationEndpoint"]["continuationCommand"]["token"]
        }
    return out

def videoViewCountRenderer(videoViewCountRenderer):
    out = "No Views detected"
    if "videoViewCountRenderer" in videoViewCountRenderer:
        videoViewCountRenderer = videoViewCountRenderer["videoViewCountRenderer"]
    if "viewCount" in videoViewCountRenderer:
        out = getText(videoViewCountRenderer["viewCount"])
    return out

def error_parse(msg):
    out = {
            "type": "error",
            "part": "parse",
            "msg": error_msg
        }
    return out


def warning_parse(msg):
    out = {"type": "warning",
           "part": "parse",
           "msg": msg
           }
    return out


def info_parse(msg):
    out = {
            "type": "info",
            "part": "parse",
            "msg": msg
            }
    return out


def parseContent(contentRaw):
    result = []
    info = []
    for x in contentRaw:
        # Goddamit youtube team. Im trying to write an program
        if "itemSectionRenderer" in x:
            to_parse = None
            if "contents" in x:
                to_parse = x["itemSectionRenderer"]["contents"]
            else:
                info.append(warning_parse(
                    "Found an itemSectionRenderer, but not the key 'contents'. Keys: " + str(x["itemSectionRenderer"].keys())))
                for y in x["itemSectionRenderer"]:
                    if type(x["itemSectionRenderer"][y]) == type(list()):
                        info.append(info_parse(
                            "Found a list inside the key '" + y + "'. Trying to parse this. "))
                        to_parse = x["itemSectionRenderer"][y]
            if to_parse is not None:
                res, inf = parseContent(to_parse)
                result = [*result, *res]
                info = [*info, *inf]
            else:
                info.append(error_parse(
                    "Couldn't parse an itemSectionRenderer. (No lists found)"))
        # Results Block:
        if "videoRenderer" in x:
            result.append(videoRenderer(x["videoRenderer"], False))
        elif "compactVideoRenderer" in x:
            result.append(videoRenderer(x["compactVideoRenderer"], True))

        elif "channelRenderer" in x:
            result.append(channelRenderer(x["channelRenderer"]))
        elif "playlistRenderer" in x:
            result.append(playlistRenderer(x["playlistRenderer"]))
        # Info Block:
        elif "compactAutoplayRenderer" in x:
            info.append(compactAutoplayRenderer(x["compactAutoplayRenderer"]))
        elif "didYouMeanRenderer" in x:
            info.append(didYouMeanRenderer(x["didYouMeanRenderer"]))
        elif "showingResultsForRenderer" in x:
            info.append(showingResultsForRenderer(
                x["showingResultsForRenderer"]))
        elif "continuationItemRenderer" in x:
            info.append(continuationItemRenderer(
                x["continuationItemRenderer"]))
    return result, info


def parse_continue_response(request):
    def __successful(commands):
        for a in commands:
            if "appendContinuationItemsAction" in a:
                mode = "append"
                items = a["appendContinuationItemsAction"]["continuationItems"]
        parsed, info = parseContent(items)
        return parsed, info, mode

    if "onResponseReceivedEndpoints" in request:
        parsed, info, mode = __successful(
            request["onResponseReceivedEndpoints"])
    elif "onResponseReceivedCommands" in request:
        parsed, info, mode = __successful(
            request["onResponseReceivedCommands"])
    else:
        parsed = list()
        info = list()
        mode = "error"
    return parsed, info, mode
