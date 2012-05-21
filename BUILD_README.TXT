We distribute FogBugzPy in two places: PyPi and developers.fogbugz.com. You'll
need to update PyPi as well as the Windows binaries.

The Python Package Index is a repository of software for the Python programming
language. FogBugzPy is published to http://pypi.python.org/pypi/fogbugz/ and
users who have pip installed can install FogBugz at the command line via:

    pip install fogbugz

If you regularly make changes to FogBugzPy, you'll want to be set up at as
user on the package in PyPi. Talk to Ben McCormack, Ben Pollack, or David 
Hodgson to be added as a user.

Once you're added, do the following to get your changes published:

 1. Bump the version number in setup.py.
 2. Commit the version bump and then tag the new changeset with the same 
    version number. For example:
    
    > hg commit -m "bump version"
    > hg tag 0.9.4
    
 3. Push the changesets to:
    https://developers.kilnhg.com/Code/FogBugz/Group/FogBugzPy

 4. Run the following command. You should only need to do this once on your
    machine:
    
    > python setup.py register
    
 5. Run the following command to upload the updated package to PyPi:
 
    > python setup.py sdist upload
    
 6. Go to http://pypi.python.org/pypi?%3Aaction=pkg_edit&name=fogbugz to
    verify that the package has been uploaded correctly.
    
 7. Although not related to PyPi, it's also helpful to update the Win32 binary
    distribution at https://developers.fogbugz.com/default.asp?W197 and 
    https://developers.fogbugz.com/default.asp?W195. You can run the following
    command to get a win32 installer:
    
    > . .\buildWindows.ps1
    
    This will create a new file in the \dist directory. Edit the wiki pages and
    add the new .exe file as an updated attachment.
    
    NOTE: The buildWindows.ps1 file will include the local copy of Beautiful 
    Soup and will update fogbugz.py to use the local copy. This allows the 
    installer to work without additional dependencies.