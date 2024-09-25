import re
from re import Pattern

from requests import Response


class GithubRequestApiError(Exception):
    def __init__(self, response: Response, message: str = ''):
        self.response: Response = response
        self.message: str = message
        self.__token_obfuscer: Pattern = re.compile(r'\'token [\w]*\'')

    def __str__(self):
        return """
----------------------------------------------------
The request to Github Api Failed
----------------------------------------------------
url : {4!s}
request :
{5!s}
status code : {1!s}
----------------------------------------------------
content :
{2!s}

----------------------------------------------------

json : 
{3!s}

----------------------------------------------------

{0!s}
""".format(
            self.message,
            self.response.status_code,
            self.response.content,
            self.response.json(),
            self.response.url,
            ','.join([self.response.request.method, self.response.request.url, str(self.response.request.body),
                      self.__token_obfuscer.sub('\'token ********\'',str(self.response.request.headers))]),
        )
