from requestgen.generator.generator import Generator
from requestgen.parser.curl_parser import CurlParser


class HttpUrlConnectionGenerator(Generator):
    cookies_template = "cookies = {{\n{text}}}"
    headers_template = "headers = {{\n{text}}}"
    data_template = "data = '{text}'"
    tab = '    '

    def __init__(self, http_request):
        super().__init__(http_request)

    def generate_import_statement(self):
        self.code += 'import java.io.*;\nimport java.net.*;'
        self.code += self.new_lines(2)

    def generate_headers(self):
        d = self.http_request.headers
        if not d:
            return
        for key, val in d.items():
            self.code += f'con.setRequestProperty("{key}", "{val}");\n'
        self.code += self.new_lines(1)

    def generate_cookies(self):
        d = self.http_request.cookies
        if not d:
            return
        cookie_val = ''
        for key, val in d.items():
            cookie_val += f'{key}={val}; '
        cookie_val = cookie_val[:-2]
        self.code += f'con.setRequestProperty("Cookie", "{cookie_val}");'
        self.code += self.new_lines(2)

    def generate_call_and_result(self):
        result = '''int responseCode = con.getResponseCode();
System.out.println("Response code: " + responseCode);

InputStreamReader inputStreamReader = null;
if (responseCode >= 200 && responseCode < 400) {
    inputStreamReader = new InputStreamReader(con.getInputStream());
} else {
    inputStreamReader = new InputStreamReader(con.getErrorStream());
}
BufferedReader in = new BufferedReader(inputStreamReader);
String inputLine;
StringBuilder response = new StringBuilder();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();

System.out.println(response.toString());'''
        self.add(result)

    def generate_connection_statements(self):
        self.code += f'''URL url = new URL("{self.http_request.url}");
HttpURLConnection con = (HttpURLConnection) url.openConnection();'''
        self.code += self.new_lines(2)

    def generate_method_and_data(self):
        method = self.http_request.method
        body = self.http_request.data

        # add the method
        self.add(f'con.setRequestMethod("{method}");')
        self.add(self.new_lines(2))

        # add body if exists
        body_template = '''String jsonInputString = "{}";
try (OutputStream os = con.getOutputStream()) {{
    byte[] input = jsonInputString.getBytes("utf-8");
    os.write(input, 0, input.length);
}}'''
        if body:
            self.add('con.setDoOutput(true);\n')
            self.add(body_template.format(body))
            self.add(self.new_lines(2))

    def generate_code(self):
        self.sanitize_input()
        self.generate_import_statement()
        self.generate_connection_statements()
        self.generate_headers()
        self.generate_cookies()
        self.generate_method_and_data()
        self.generate_call_and_result()
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
    generator = HttpUrlConnectionGenerator(http_request)
    code = generator.generate_code()
    print(code)
    pass


if __name__ == '__main__':
    main()

# todo Improvements
# curl -o myfile.css https://cdn.keycdn.com/css/animate.min.css download this file and save it
