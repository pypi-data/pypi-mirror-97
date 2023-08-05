class BaseClass:
    _error = list()

    def _reset_error(self):
        self._error = list()

    def throw_error(self):
        for i in self._error:
            if i["type"] == "InvalidFilterError":
                raise InvalidFilterError(i["msg"])
            elif i["type"] == "NoMoreResultsError":
                raise NoMoreResultsError()

    def _error_invalid_filter(self, invalid_filter=list()):
        self._error.add({"type": "InvalidFilterError", "msg": invalid_filter})

    def _error_no_more_results(self):
        self._error.add({"type": "NoMoreResultsError"})

    def _error_parsing_failure(self, data):
        self._error.add({"type": "ParsingFailureError", "data": data})

    def _error_invalid_input(self, data):
        self._error.add({"type": "InvalidInputError", "input": data})


class Error(Exception):
    message = str()


class InvalidFilterError(Error):
    def __init__(self, invalid_filter):
        self.message = "Invalid filter used:"
        self.invalid_filter = invalid_filter


class NoMoreResultsError(Error):
    def __init__(self):
        self.message = "There are no more results."
