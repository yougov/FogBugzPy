import io

import setuptools


with io.open('README.txt', encoding='utf-8') as readme:
    long_description = readme.read()

with io.open('LICENSE', encoding='utf-8') as readme:
    license = readme.read()


setup_params = dict(
    name='fogbugz_bis',
    use_scm_version=True,
    py_modules=['fogbugz'],
    license=license,
    description='Python library for interacting with the FogBugz API',
    long_description=long_description,
    author='Fog Creek Software',
    author_email='customer-service@fogcreek.com',
    maintainer='YouGov, Plc.',
    maintainer_email='open-source@yougov.com',
    url='https://github.com/yougov/FogBugzPy',
    install_requires=[
        'BeautifulSoup4',
        'lxml',
        'six',
    ],
    requires=['BeautifulSoup', 'lxml'],
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
    setup_requires=[
      'setuptools_scm',
    ],
)

if __name__ == '__main__':
    setuptools.setup(**setup_params)
