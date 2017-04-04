try:
  from ez_setup import use_setuptools
  use_setuptools()

  from setuptools import setup
except ImportError:
  from distutils.core import setup

from textwrap import dedent
with io.open('README.txt', encoding='utf-8') as readme:
    long_description = readme.read()

with io.open('LICENSE', encoding='utf-8') as readme:
    license = readme.read()

setup(name='fogbugz',
      version='1.0.5',
      py_modules=['fogbugz'],
      packages=['BeautifulSoup'],
      license=license,
      description='Python library for interacting with the FogBugz API',
      long_description=long_description,
      author='Fog Creek Software',
      author_email='customer-service@fogcreek.com',
      maintainer='Fog Creek Software',
      maintainer_email='customer-service@fogcreek.com',
      url='https://developers.kilnhg.com/Repo/FogBugz/Group/FogBugzPy',
      download_url='https://developers.kilnhg.com/Repo/FogBugz/Group/FogBugzPy',
      install_requires=['BeautifulSoup4', 'lxml'],
      requires=['BeautifulSoup', 'lxml']
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
