
# The code you were writing anyway, or some good functions.
def get_best_thumbnail_from_list(thumbnails):
    largestWidth = 0
    out = ""
    for x in thumbnails:
        if x["width"] > largestWidth:
            largestWidth = x["width"]
            out = x["url"]
    return out


def get_worst_thumbnail_from_list(thumbnails):
    tiniestWidth = 1000
    out = ""
    for x in thumbnails:
        if x["width"] < tiniestWidth:
            tiniestWidth = x["width"]
            out = x["url"]
        return out
