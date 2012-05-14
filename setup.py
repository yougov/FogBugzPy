try:
  from ez_setup import use_setuptools
  use_setuptools()

  from setuptools import setup
except ImportError:
  from distutils.core import setup

from textwrap import dedent

setup(name='fogbugz',
      version='0.9.5',
      py_modules=['fogbugz'],
      license=dedent("""\
        Copyright (c) 2011, Fog Creek Software, Inc.
        All rights reserved.

        Redistribution and use in source and binary forms, with or without modification,
        are permitted provided that the following conditions are met:

        Redistributions of source code must retain the above copyright notice, this list
        of conditions and the following disclaimer.  Redistributions in binary form must
        reproduce the above copyright notice, this list of conditions and the following
        disclaimer in the documentation and/or other materials provided with the
        distribution.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
        ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
        WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
        ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
        (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
        LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
        ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
        (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
        SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
        """),
      description='Python library for interacting with the FogBugz API',
      long_description=dedent("""\
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
          <response>
            <cases count="2">
              <case ixbug="1" operations="edit,assign,resolve,email,remind"></case>
              <case ixbug="2" operations="edit,spam,assign,resolve,reply,forward,remind"></case>
            </cases>
          </response>
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
          >>> # To upload files, just pass a `Files` parameter that is a dictionary of filename and file handle. New in 0.9.2.
          >>> resp = fb.edit(ixbug=2, sEvent="Add a file from the API", Files={'filename': open('filename', 'r')}) # Note the named parameters
          >>> resp
          <response><case ixbug="2" operations="edit,assign,resolve,email,remind"></case></response>

        Note that, per API v5.0, all data between tags, such as the token, is now wrapped in CDATA.  BeautifulSoup's implementation of CData generally allows for it to be treated as a string, except for one important case: CData.__str__() (a.k.a. str(CData)) returns the full text, including the CDATA wrapper (e.g. "<![CDATA[foo]]>").  To avoid accidentally including the CDATA tage, use CData.encode('utf-8')

        For more info on the API:
        http://our.fogbugz.com/help/topics/advanced/API.html
        """),
      author='Fog Creek Software',
      author_email='customer-service@fogcreek.com',
      maintainer='Fog Creek Software',
      maintainer_email='customer-service@fogcreek.com',
      url='https://developers.kilnhg.com/Repo/FogBugz/Group/FogBugzPy',
      download_url='https://developers.kilnhg.com/Repo/FogBugz/Group/FogBugzPy',
      install_requires=['BeautifulSoup==3.2'],
      requires='BeautifulSoup',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Operating System :: POSIX :: BSD',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Software Development',
          'Topic :: Software Development :: Bug Tracking',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: Version Control',
          'Topic :: Utilities',
      ],
)
