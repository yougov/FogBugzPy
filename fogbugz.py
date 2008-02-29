import urllib2

from BeautifulSoup import BeautifulSoup

class FogBugzAPIError(Exception):
    def __init__(self, response):
        self.response = response
        self.message = response.error.string
        self.error_code = int(response.error['code'])

class FogBugzConnectionError(Exception):
    pass

class FBType:
    """
    Base FogBugz object from which all other objects inherit.
    """
    def __init__(self, fb):
        self._fb = fb

    def __new__(cls, name, bases, dct):
        return type.__new__(cls, name, bases, dict)

class FBFilter:
    TYPE_BUILTIN = 1
    TYPE_SAVED = 2
    TYPE_SHARED = 3
    
    def __init__(self, fb, filter):
        FBObject.__init__(self, fb)

        id = filter['sfilter']
        name = filter.string
        current = filter.get('status', None) == 'current'        
        
        if filter['type'] == 'builtin':
            self.type = TYPE_BUILTIN
        if filter['type'] == 'saved':
            self.type = TYPE_SAVED
        if filter['type'] == 'shared':
            self.type = TYPE_SHARED

    def setCurrent(self):
        self._fb.setCurrentFilter(self.id)

    def listCases(self):
        currentFilter = self._fb.currentFilter
        response = self.makeRequest('search')
                    

class FogBugz:
    def __init__(self, url):
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

    def makeRequest(self, cmd, **kwargs):
        data = 'cmd=%s' % (cmd,)
        for k in kwargs.keys():
            data += '&%s=%s' % (k, kwargs[k],)
        if self._token:
            data += '&token=%s' % (self._token,)
        try:
            response = BeautifulSoup(self._opener.open(self._url, data)).response
        except URLError, e:
            raise FogBugzConnectionError(e)
        if response.error:
            raise FogBugzAPIError(response)
        print self._url, data
        print response
        return response
        
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
            response = self.makeRequest('logon', email=username, password=password)
        except FogBugzAPIError, e:
            if e.error_code == 2:
                return [person.string for person in response.people.findall('person')]
            else:
                raise e
        self._token = response.token.string
        return None
        
    def logoff(self):
        """
        Logs off the current user.
        """
        self.makeRequest('logoff')
        self._token = None
        
    def listFilters(self):
        """
        Returns a list of FBFilters.
        """
        response = self.makeRequest('listFilters')
        filters = []
        for filter in response.filters.findAll(name='filter'):
            filters.append(FBFilter(self, filter))
            if current:
                self.currentFilter = id
        return filters

    def setCurrentFilter(self, id):
        self.makeRequest('saveFilter', sFilter=self.id)

    def search(self):
        response = self.makeRequest('search')

    def new(self):
        response = self.makeRequest('new')

    def edit(self):
        response = self.makeRequest('edit')

    def assign(self):
        response = self.makeRequest('assign')

    def reactivate(self):
        response = self.makeRequest('reactivate')

    def reopen(self):
        response = self.makeRequest('reopen')

    def resolve(self):
        response = self.makeRequest('resolve')

    def close(self):
        response = self.makeRequest('close')

    def email(self):
        response = self.makeRequest('email')

    def reply(self):
        response = self.makeRequest('reply')

    def forward(self):
        response = self.makeRequest('forward')

    def listMailboxes(self):
        response = self.makeRequest('listMailboxes')

    def listProjects(self):
        response = self.makeRequest('listProjects')

    def listAreas(self):
        response = self.makeRequest('listAreas')

    def listCategories(self):
        response = self.makeRequest('listCategories')

    def listPriorities(self):
        response = self.makeRequest('listPriorities')

    def listPeople(self):
        response = self.makeRequest('listPeople')

    def listStatuses(self):
        response = self.makeRequest('listStatuses')

    def listFixFors(self):
        response = self.makeRequest('listFixFors')

    def viewProject(self):
        response = self.makeRequest('viewProject')

    def viewArea(self):
        response = self.makeRequest('viewArea')

    def viewCategory(self):
        response = self.makeRequest('viewCategory')

    def viewPriority(self):
        response = self.makeRequest('viewPriority')

    def viewPerson(self):
        response = self.makeRequest('viewPerson')

    def viewStatus(self):
        response = self.makeRequest('viewStatus')

    def viewFixFor(self):
        response = self.makeRequest('viewFixFor')

    def viewMailbox(self):
        response = self.makeRequest('viewMailbox')

    def listWorkingSchedule(self):
        response = self.makeRequest('listWorkingSchedule')

    def wsDateFromHours(self):
        response = self.makeRequest('wsDateFromHours')

    def startWork(self):
        response = self.makeRequest('startWork')

    def stopWork(self):
        response = self.makeRequest('stopWork')

    def newInterval(self):
        response = self.makeRequest('newInterval')

    def listIntervals(self):
        response = self.makeRequest('listIntervals')

    def newCheckin(self):
        response = self.makeRequest('newCheckin')

    def listCheckins(self):
        response = self.makeRequest('listCheckins')

    def listDiscussGroups(self):
        response = self.makeRequest('listDiscussGroups')

    def listDiscussion(self):
        response = self.makeRequest('listDiscussion')

    def listDiscussTopic(self):
        response = self.makeRequest('listDiscussTopic')

    def listScoutCase(self):
        response = self.makeRequest('listScoutCase')

    def subscribe(self):
        response = self.makeRequest('subscribe')

    def unsubscribe(self):
        response = self.makeRequest('unsubscribe')

    def view(self):
        response = self.makeRequest('view')

    def viewSettings(self):
        response = self.makeRequest('viewSettings')

    def list(self):
        response = self.makeRequest('list')