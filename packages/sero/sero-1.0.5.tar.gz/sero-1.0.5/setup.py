import setuptools

with open('./README.md', 'r') as readme_file:
    long_description = str(readme_file.read())

with open('./sero/VERSION', 'r') as version_file:
    version = str(version_file.read())

NAME = 'sero'
DESCRIPTION = 'A simple module for concurrently running tasks.'
LISCENCE = 'GPL-3.0'
AUTHOR = 'z3c0'
AUTHOR_EMAIL = 'z3c0@21337.tech'
PYTHON_VERSION = '>=3.9.1'
GITHUB_URL = 'https://github.com/z3c0/sero'

KEYWORDS = ['pipeline']

CLASSIFIERS = \
    ['License :: OSI Approved :: GNU General Public License v3 (GPLv3)']

setup_kwargs = {'name': NAME,
                'author': AUTHOR,
                'author_email': AUTHOR_EMAIL,
                'packages': setuptools.find_packages(),
                'include_package_data': True,
                'version': version,
                'license': LISCENCE,
                'description': DESCRIPTION,
                'long_description': long_description,
                'long_description_content_type': 'text/markdown',
                'url': GITHUB_URL,
                'keywords': KEYWORDS,
                'classifiers': CLASSIFIERS,
                'python_requires': PYTHON_VERSION,
                'install_requires': []}

setuptools.setup(**setup_kwargs)
