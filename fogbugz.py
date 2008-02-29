import urllib2

from BeautifulSoup import BeautifulSoup

class FogBugzAPIError(Exception):
    def __init__(self, response):
        self.response = response
        self.message = response.error.string
        self.error_code = int(response.error['code'])

class FogBugzLogonError(FogBugzAPIError):
    pass

class FogBugzConnectionError(Exception):
    pass

class FogBugz:
    def __init__(self, url):
        self.__handlerCache = {}
        if not url.endswith('/'):
            url += '/'
            
        self._token = None
        self._opener = urllib2.build_opener()        
        try:
            soup = BeautifulSoup(self._opener.open(url + 'api.xml'))
        except URLError:
            raise FogBugzConnectionError("Library could not connect to the FogBugz API.  Either this installation of FogBugz does not support the API, or the url, %s, is incorrect." % (self._url,))
        self._url = url + soup.response.url.string
        self.currentFilter = None

    def logon(self, username, password):
        """
        Logs the user on to FogBugz.

        Returns None for a successful login, otherwise returns a list
        of logins to choose from if the username provided is
        ambiguous.
        """
        if self._token:
            logoff()
        try:
            response = self.__makerequest('logon', email=username, password=password)
        except FogBugzAPIError, e:
            raise FogBugzLogonError(e)
        
        self._token = response.token.string
        
    def logoff(self):
        """
        Logs off the current user.
        """
        self.__makerequest('logoff')
        self._token = None

    def __makerequest(self, cmd, **kwargs):
        data = 'cmd=%s' % (cmd,)
        for k in kwargs.keys():
            data += '&%s=%s' % (k, kwargs[k],)
        if self._token:
            data += '&token=%s' % (self._token,)
        try:
            response = BeautifulSoup(self._opener.open(self._url+data)).response
        except urllib2.URLError, e:
            raise FogBugzConnectionError(e)
        if response.error:
            print response
            raise FogBugzAPIError(response)
        # TODO: Remove print for Release
        print response
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

        if not self.__handlerCache.has_key(name):
            def handler(**kwargs):
                return self.__makerequest(name, **kwargs)
            self.__handlerCache[name] = handler
        return self.__handlerCache[name]
        