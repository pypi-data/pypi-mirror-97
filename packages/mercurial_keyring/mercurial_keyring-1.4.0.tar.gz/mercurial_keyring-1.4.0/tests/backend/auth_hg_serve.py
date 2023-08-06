# Extended version of Mercurial WSGI wrapper, adding
# some minimal HTTP auth.

from base64 import b64decode
from wsgiref.simple_server import make_server
from mercurial import demandimport; demandimport.enable()
from mercurial.hgweb import hgweb

PORT = 8080
CONFIG_PATH = 'auth_hg_serve.cfg'


class TrivialAuth(object):
    """Authorizes if user==password + user starts from abc"""

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        if self.is_authenticated(environ.get('HTTP_AUTHORIZATION')):
            return self.application(environ, start_response)
        return self.password_prompt(environ, start_response)

    def is_authenticated(self, header):
        if not header:
            return False
        _, encoded = header.split(None, 1)
        decoded = b64decode(encoded).decode('utf-8')
        username, password = decoded.split(':', 1)
        return username == password and username.startswith("abc")

    def password_prompt(self, environ, start_response):
        start_response(
            '401 Authentication Required',
            [
                ('Content-Type', 'text/html'),
                ('WWW-Authenticate', 'Basic realm="HGLogin"'),
            ])
        return [b'Please login']


def dummy_app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'Hello, world!']


if __name__ == '__main__':
    # httpd = make_server('', PORT, TrivialAuth(dummy_app))

    httpd = make_server('', PORT, TrivialAuth(hgweb(CONFIG_PATH)))
    # application = hgweb(config_path)

    # httpd = make_server('', 8080, TrivialAuth(application))
    print('Serving on port 8080...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
