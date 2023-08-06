import sys

from requestgen.generator.language_java import (apache_http_client,
                                                http_url_connection)
from requestgen.generator.language_python import python_generator
from requestgen.parser import curl_parser


class CodeConversionException(Exception):
    pass


from_languages_mapping = {'CURL': curl_parser.CurlParser}
to_languages_mapping = {'PYTHON_REQUESTS': python_generator.PythonGenerator,
                        'JAVA_APACHE_HTTP_CLIENT': apache_http_client.ApacheHttpClientCodeGenerator,
                        'JAVA_HTTP_URL_CONNECTION': http_url_connection.HttpUrlConnectionGenerator}


class Converter:

    def __init__(self, from_language, to_language):
        self.code_parser, self.code_generator = from_languages_mapping.get(
            from_language), to_languages_mapping.get(
            to_language)
        if not self.code_parser:
            message = f'Language {from_language} not supported\n'
            l = [key for key in from_languages_mapping.keys()]
            message += f'Supported languages to convert from are {", ".join(l)}'
            raise CodeConversionException(message)
        if not self.code_generator:
            message = f'Language {to_language} not supported\n'
            l = [key for key in to_languages_mapping.keys()]
            message += f'Supported languages to convert to are {", ".join(l)}'
            raise CodeConversionException(message)

    def convert(self, input_code):
        # with open('generator/input.txt', 'r') as f:
        #     curl_command = f.read()
        http_request = self.code_parser(input_code).parse()
        generator = self.code_generator(http_request)
        code = generator.generate_code()
        return code


def get_usage():
    message = 'Usage: converter from_language to_language [from_code]\n\n'
    from_languages = ', '.join([key for key in from_languages_mapping.keys()])
    to_languages = ', '.join([key for key in to_languages_mapping.keys()])
    message += f'Currently you can convert from {from_languages}\nto {to_languages}\n\n'
    message += 'Try python converter.py CURL PYTHON_REQUESTS'
    return message


def convert(from_language='CURL', to_language=None, input_code=None):
    converter = Converter(from_language=from_language, to_language=to_language)
    return converter.convert(input_code)


def main():
    arg_length = len(sys.argv)
    if arg_length == 2 and sys.argv == '--help':
        print(get_usage())
        exit(0)
    if arg_length < 3:
        print(get_usage())
        exit(1)
    from_language = sys.argv[1]
    to_language = sys.argv[2]
    converter = Converter(from_language=from_language, to_language=to_language)
    if arg_length != 4:
        input_code = input(f'Paste the {from_language} code')
    else:
        input_code = sys.argv[3]
    code = converter.convert(input_code)
    print(code)


if __name__ == '__main__':
    main()
