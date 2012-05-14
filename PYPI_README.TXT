The Python Package Index is a repository of software for the Python programming
language. FogBugzPy is published to http://pypi.python.org/pypi/fogbugz/ and
users who have pip installed can install FogBugz at the command line via:

    pip install fogbugz

If you regularly make changes to FogBugzPy, you'll want to be set up at as
user on the package in PyPi. Talk to Ben McCormack, Ben Pollack, or David Hodgson
to be added as a user.

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