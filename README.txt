Python FogBugz API Wrapper
--------------------------

This Python API is simply a wrapper around the FogBugz API, with some help from Leonard Richardson's BeautifulSoup (http://www.crummy.com/software/BeautifulSoup/) and the magic of Python's __getattr__().

Getting Started:
----------------

To use the FogBugz API, install the package either by downloading the source and running

  $ python setup.py install

or by using pip

  $ pip install fogbugz

A Quick Example:
----------------

::

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

Additional Details:
-------------------

If your script requires a certain version of the FogBugz API, make sure to pass it as an argument to the constructor. This will protect you from unexpected differences should we make backwards-incompatible changes.

  >>> from fogbugz import FogBugz
  >>> fb = FogBugz("http://example.fogbugz.com", api_version=5)

For more info on the API:
http://help.fogcreek.com/the-fogbugz-api

Much of the API has not been thoroughly tested.  Please report bugs to customer-service@fogcreek.com

``fogbugz_bis`` is a fork of the FogCreek codebase to support Python 3 and
BeautifulSoup 4. You should install/require only one of ``fogbugz`` or
``fogbugz_bis`` as they both implement the same module.
