Python FogBugz API Wrapper

This Python API is simply a wrapper around the FogBugz API, with some help from Leonard Richardson's BeautifulSoup (http://www.crummy.com/software/BeautifulSoup/) and the magic of Python's __getattr__().

A quick example:

>>> from fogbugz import FogBugz
>>> fb = FogBugz("http://example.fogbugz.com/") # URL is to your FogBugz install
>>> fb.logon("logon@example.com", "password")
>>> resp = fb.search(q="assignedto:tyler") # All calls take named parameters, per the API
>>> resp # Responses are BeautifulSoup objects of the response XML.
<response><cases count="2"><case ixbug="1" operations="edit,assign,resolve,email,remind"></case><case ixbug="2" operations="edit,spam,assign,resolve,reply,forward,remind"></case></cases></response>
>>> # You shouldn't need to know too much about BeautifulSoup, but the documentation can be found here:
>>> # http://www.crummy.com/software/BeautifulSoup/documentation.html
>>> for case in resp.cases.childGenerator(): # One way to access the cases
...     print case['ixbug']
...
1
2
>>> for case in resp.findAll('case'):
...     print case['operations']
...
edit,assign,resolve,email,remind
edit,spam,assign,resolve,reply,forward,remind
>>> resp = fb.edit(ixbug=1, sEvent="Edit from the API")
>>> resp
<response><case ixbug="1" operations="edit,assign,resolve,email,remind"></case></response>

For more info on the API
http://our.fogbugz.com/help/topics/advanced/API.html

Known Issues:
* File uploading is currently unsupported for both cases and emails.

Much of the API has not been thoroughly tested.  Please assign bugs to Tyler Hicks-Wright.