Python FogBugz API Wrapper

This Python API is simply a wrapper around the FogBugz API, with some help from Leonard Richardson's BeautifulSoup (http://www.crummy.com/software/BeautifulSoup/) and the magic of Python's __getattr__().

Getting Started:
To use the FogBugz API, just put the file fogbugz.py somewhere on your Python path.  It's probably easiest to add this before the import:
>>> import sys
>>> sys.path.append("""c:\code\fbapi""")
>>> from fogbugz import FogBugz

A Quick Example:
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
>>> for case in resp.findAll('case'): # Another way to access the cases
...     print case['operations']
...
edit,assign,resolve,email,remind
edit,spam,assign,resolve,reply,forward,remind
>>> resp = fb.edit(ixbug=1, sEvent="Edit from the API") # Note the named parameters
>>> resp
<response><case ixbug="1" operations="edit,assign,resolve,email,remind"></case></response>

Note that, per API v5.0, all data between tags, such as the token, is now wrapped in CDATA.  BeautifulSoup's implementation of CData generally allows for it to be treated as a string, except for one important case: CData.__str__() (a.k.a. str(CData)) returns the full text, including the CDATA wrapper (e.g. "<![CDATA[foo]]>").  To avoid accidentally including the CDATA tage, use CData.encode('utf-8')

For more info on the API:
http://our.fogbugz.com/help/topics/advanced/API.html

Known Issues:
* File uploading is currently unsupported for both cases and emails.

Much of the API has not been thoroughly tested.  Please assign bugs to Tyler Hicks-Wright.