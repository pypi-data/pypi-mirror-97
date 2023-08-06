from abc import ABCMeta, abstractmethod


class Generator(metaclass=ABCMeta):
    def __init__(self, http_request, language=None):
        self.code = ''
        self.http_request = http_request
        self.language = language

    @abstractmethod
    def generate_code(self):
        pass

    def new_lines(self, n):
        return '\n' * n

    def add(self, code):
        self.code += code

    def sanitize_input(self):
        self.http_request.url = self.replace_quotes(self.http_request.url)
        self.http_request.data = self.replace_quotes(self.http_request.data)
        self.http_request.url = self.replace_quotes(self.http_request.url)

        d = self.http_request.headers
        if d:
            for key, val in d.items() or []:
                d[key] = self.replace_quotes(d[key])

        d = self.http_request.cookies
        if d:
            for key, val in d.items() or []:
                d[key] = self.replace_quotes(d[key])
        # todo params as well

    def replace_quotes(self, text):
        if not isinstance(text, str):
            return text
        if self.language and self.language.startswith('PYTHON'):
            return text.replace("'", "\\'")
        return text.replace('"', '\\"')
