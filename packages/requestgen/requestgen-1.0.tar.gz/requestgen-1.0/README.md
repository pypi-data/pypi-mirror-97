# HTTP Request Generator and Converter
Converts CURL code to its equivalent in other programming languages

You can convert the code from ```CURL``` to
- Python requests
- Java - HttpUrlConnection
- Java - Apache HttpClient

More languages will be added shortly

### Install
```pip install requestgen```
or clone the repo and run the command
```python install setup.py```

### Usage
Convert from Curl to Apache HttpClient Request
```shell script
convert CURL JAVA_APACHE_HTTP_CLIENT, 'curl google.com'
```
or takes input from stdin
```shell script
convert CURL PYTHON_REQUESTS
```

Usage via API
```python
import requestgen

print(requestgen.convert(from_language='CURL', to_language='JAVA_HTTP_URL_CONNECTION',
 input_code='curl google.com'))
```


