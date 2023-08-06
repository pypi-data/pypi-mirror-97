from dataclasses import dataclass


@dataclass
class HttpRequest:
    url: str = None
    method: str = None
    headers: dict = None
    data: str = None
    params: str = None
    authentication: str = None
    cookies: dict = None

    # def set_url(self, url):
    #     self.url = url
    #     return self
    #
    # def set_method(self, method):
    #     self.method = method
    #     return self
    #
    # def set_headers(self, headers):
    #     self.headers = headers
    #     return self
    #
    # def set_params(self, params):
    #     self.params = params
    #     return self
    #
    # def set_body(self, body):
    #     self.body = body
    #     return self
    #
    # def set_authentication(self, authentication):
    #     self.authentication = authentication
    #     return self
