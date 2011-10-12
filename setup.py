from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

setup(name='fogbugz',
      version='0.9.1',
      py_modules=['fogbugz'],
      description='Python library for interacting with the FogBugz API',
      author='Tyler G. Hicks-Wright',
      author_email='customer-service@fogcreek.com',
      maintainer='Fog Creek Software',
      maintainer_email='customer-service@fogcreek.com',
      url='https://developers.kilnhg.com/Repo/FogBugz/Group/FogBugzPy',
      download_url='https://developers.kilnhg.com/Repo/FogBugz/Group/FogBugzPy',
      install_requires=['BeautifulSoup==3.2'],
)
