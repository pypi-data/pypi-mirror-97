_filters_dict = {
        "top": "url",
        "newest": "url"
        }


class Comments:
    __continue_token = str()
    _comments_list = list()
    _initalized = False
    _filters = dict()
    _current_filter = ""
    _comments_available = False

    def __init__(self, yt_core_dl, token=str(), comment_filter=str()):
        self._dl = yt_core_dl
        self.__continue_token = token
        self._filters = _filters_dict.copy()
        if not filters == "":
            self._set_filter(comment_filter)

    def _soft_reset(self):
        self._comments_available = False
        self._initalized = False
        self._comments_list = list()

    def _set_filter(self, comment_filter):
        if comment_filter in self._filters:
            self._current_filter = comment_filter
            self._soft_reset()

    def get_comments(self):
        return _comments_list

    def comments(self, comment_filter=str()):
        self._set_filter(comment_filter)
        if not self._initalized:
            self._initalized = True
        else:
            self._soft_reset()
        return out

    def comments_continue(self):
        return []
