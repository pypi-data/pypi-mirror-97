class ExtractionHandlers(object):
    """Generic implementation of handler class."""

    _cursor_position = None

    def handle_response(self, response):
        print(response.text)

    def handle_error(self, exception):
        print(repr(exception))

    def get_cursor_position(self):
        return self._cursor_position

    def record_cursor_position(self, cursor):
        self._cursor_position = cursor
