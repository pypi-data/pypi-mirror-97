from requestgen.generator.generator import Generator
from requestgen.parser.curl_parser import CurlParser


class PythonGenerator(Generator):
    cookies_template = "cookies = {{\n{text}}}"
    headers_template = "headers = {{\n{text}}}"
    data_template = "data = '{text}'"
    tab = '    '

    def __init__(self, http_request):
        super().__init__(http_request, language='PYTHON')

    def generate_import_statement(self):
        self.code += 'import requests'
        self.code += self.new_lines(2)

    def generate_headers_or_cookie(self, headers):
        if headers:
            d = self.http_request.headers
            template = self.headers_template
        else:
            d = self.http_request.cookies
            template = self.cookies_template
        if not d:
            return
        data = ''
        for key, val in d.items():
            data += f"{self.tab}'{key}': '{val}',\n"
        self.code += template.format(text=data)
        self.code += self.new_lines(2)

    def generate_data(self):
        data = self.http_request.data
        if not data:
            return
        self.code += self.data_template.format(text=data)
        self.code += self.new_lines(2)

    def generate_function_call(self):

        method = self.http_request.method
        l = [f"'{self.http_request.url}'"]
        # headers
        if self.http_request.headers:
            l.append('headers=headers')
        # params
        if self.http_request.params:
            l.append('params=params')
        # cookies
        if self.http_request.cookies:
            l.append('cookies=cookies')
        # data
        if self.http_request.data:
            l.append('data=data')
        fn_call = f"response = requests.{method.lower()}({', '.join(l)})"
        self.code += fn_call
        self.code += self.new_lines(1)

    def generate_print_response_stmt(self):
        self.code += 'print(response.content)'

    def generate_code(self):
        self.sanitize_input()
        self.generate_import_statement()
        self.generate_headers_or_cookie(headers=False)
        self.generate_headers_or_cookie(headers=True)
        self.generate_data()
        self.generate_function_call()
        self.generate_print_response_stmt()
        return self.code


def main():
    curl_command = '''curl -H "Content-Type:application/json" 
    -H "Authorization:Basic token" 
    -H "Cookie: cookie1=cookie_val; cookie2=cookie2_val; "
    -X POST 
    -d "test body" --data-raw "test body2"
    http://example.com/example?a=1&b=2'''
    with open('../input.txt', 'r') as f:
        curl_command = f.read()
    http_request = CurlParser(curl_command).parse()
    generator = PythonGenerator(http_request)
    code = generator.generate_code()
    print(code)
    pass


if __name__ == '__main__':
    main()

# todo Improvements
# curl -o myfile.css https://cdn.keycdn.com/css/animate.min.css download this file and save it
