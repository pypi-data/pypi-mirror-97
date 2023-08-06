import ssl
ssl._create_default_https_context = ssl._create_unverified_context


from http.client import HTTPSConnection
from http.client import HTTPConnection


class Response:
    def __init__(self, response):
        self.result = str(response.read().decode())
        self.status = int(response.getcode())
        self.headers = {}
        for i in list(response.getheaders()):
            header, value = (i)
            self.headers[header] = value


def UrlParser(url):
    protocol = "https"
    if url[:8] == "https://":
        protocol = "https"
        url = url[8:]

    elif url[:7] == "http://":
        protocol = "http"
        url = url[7:]

    path = "/"
    domain = url
    if "/" in url:
        path = url[url.find("/"):]
        domain = url[:url.find("/")]

    return protocol, domain, path


def NetRequest(url, data='', method='GET', **kwargs):
    protocol, domain, path = UrlParser(url)
    if protocol == "https":
        server = HTTPSConnection(domain)

    else:
        server = HTTPConnection(domain)

    server.request(method, path, data, **kwargs)

    response = server.getresponse()

    return Response(response)
