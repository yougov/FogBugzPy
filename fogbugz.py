from __future__ import print_function
import sys
try:
    from email.generator import _make_boundary
except ImportError:
    from mimetools import choose_boundary as _make_boundary
try:
    import urllib.request as urllib_request
except ImportError:
    import urllib2 as urllib_request
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

try:
    basestring
except NameError:
    basestring = str

from bs4 import BeautifulSoup, CData

DEBUG = False # Set to True for debugging output.

class FogBugzAPIError(Exception):
    pass

class FogBugzLogonError(FogBugzAPIError):
    pass

class FogBugzConnectionError(FogBugzAPIError):
    pass

class FogBugzAPIVersionError(FogBugzAPIError):
    pass

class FogBugz:
    def __init__(self, url, token=None, api_version=8):
        self.__handlerCache = {}
        if not url.endswith('/'):
            url += '/'

        if token:
            self._token = token
        else:
            self._token = None

        self._opener = urllib_request.build_opener()
        try:
            stream = self._opener.open(url + 'api.xml')
            soup = BeautifulSoup(stream, 'xml')
        except (urllib_request.URLError, urllib_request.HTTPError):
            e = sys.exc_info()[1]
            raise FogBugzConnectionError("Library could not connect to the FogBugz API.  Either this installation of FogBugz does not support the API, or the url, %s, is incorrect.\n\nError: %s" % (url, e))

        # check API version
        self._minversion = int(soup.response.minversion.string)
        self._maxversion = int(soup.response.version.string)
        if api_version and type(api_version) is int:
            if api_version < self._maxversion:
                print("There is a newer version of the FogBugz API available. Please update to version %d to avoid errors in the future" % self._maxversion, file=sys.stderr)
            elif api_version > self._maxversion:
                raise FogBugzAPIVersionError("This script requires API version %d and the maximum version supported by %s is %d." % (api_version, url, self._maxversion))
            if api_version < self._minversion:
                raise FogBugzAPIVersionError("This script requires API version %d and the minimum version supported by %s is %d. Please update to use the latest API version" % (api_version, url, self._minversion))
        else:
            raise FogBugzAPIVersionError("api_version parameter must be an int")

        self._url = url + soup.response.url.string
        self.currentFilter = None

    def logon(self, username, password):
        """
        Logs the user on to FogBugz.

        Returns None for a successful login.
        """
        if self._token:
            self.logoff()
        try:
            response = self.__makerequest('logon', email=username, password=password)
        except FogBugzAPIError:
            e = sys.exc_info()[1]
            raise FogBugzLogonError(e)

        self._token = response.token.string
        if type(self._token) == CData:
                self._token = self._token.encode('utf-8')

    def logoff(self):
        """
        Logs off the current user.
        """
        self.__makerequest('logoff')
        self._token = None

    def token(self,token):
        """
        Set the token without actually logging on.  More secure.
        """
        self._token = token

    def __encode_multipart_formdata(self, fields, files):
        """
        fields is a sequence of (key, value) elements for regular form fields.
        files is a sequence of (filename, filehandle) files to be uploaded
        returns (content_type, body)
        """
        BOUNDARY = _make_boundary()

        if len(files) > 0:
            fields['nFileCount'] = str(len(files))

        crlf = '\r\n'
        buf = BytesIO()

        for k, v in fields.items():
            if DEBUG:
                print("field: %s: %s"% (repr(k), repr(v)))
            lines = [
                '--' + BOUNDARY,
                'Content-disposition: form-data; name="%s"' % k,
                '',
                str(v),
                '',
            ]
            buf.write(crlf.join(lines).encode('utf-8'))

        n = 0
        for f, h in files.items():
            n += 1
            lines = [
                '--' + BOUNDARY,
                'Content-disposition: form-data; name="File%d"; '
                    'filename="%s"' % (n, f),
                '',
            ]
            buf.write(crlf.join(lines).encode('utf-8'))
            lines = [
                'Content-type: application/octet-stream',
                '',
                '',
            ]
            buf.write(crlf.join(lines).encode('utf-8'))
            buf.write(h.read())
            buf.write(crlf.encode('utf-8'))

        buf.write(('--' + BOUNDARY + '--' + crlf).encode('utf-8'))
        content_type = "multipart/form-data; boundary=%s" % BOUNDARY
        return content_type, buf.getvalue()

    def __makerequest(self, cmd, **kwargs):
        kwargs["cmd"] = cmd
        if self._token:
            kwargs["token"] = self._token

        fields = kwargs
        files = fields.get('Files', {})
        if 'Files' in fields:
            del fields['Files']

        content_type, body = self.__encode_multipart_formdata(fields, files)
        if DEBUG:
            print(body)
        headers = { 'Content-Type': content_type,
                    'Content-Length': str(len(body))}

        try:
            url = self._url
            if sys.version_info < (3,):
                url = self._url.encode('utf-8')
            request = urllib_request.Request(url, body, headers)
            resp_stream = self._opener.open(request)
            response = BeautifulSoup(resp_stream, "xml").response
        except urllib_request.URLError:
            e = sys.exc_info()[1]
            raise FogBugzConnectionError(e)
        except UnicodeDecodeError:
            e = sys.exc_info()[1]
            print(kwargs)
            raise

        if response.error:
            raise FogBugzAPIError('Error Code %s: %s' % (response.error['code'], response.error.string,))
        return response

    def __getattr__(self, name):
        """
        Handle all FogBugz API calls.

        >>> fb.logon(email@example.com, password)
        >>> response = fb.search(q="assignedto:email")
        """

        # Let's leave the private stuff to Python
        if name.startswith("__"):
            raise AttributeError("No such attribute '%s'" % name)

        if name not in self.__handlerCache:
            def handler(**kwargs):
                return self.__makerequest(name, **kwargs)
            self.__handlerCache[name] = handler
        return self.__handlerCache[name]
