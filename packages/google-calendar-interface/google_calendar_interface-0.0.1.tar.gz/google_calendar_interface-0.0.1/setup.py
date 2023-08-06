from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['google_calendar']
print('packages=', packages)

setup(
    name="google_calendar_interface",

    version="0.0.1",
    # 0.0.1 - bug fixes, bad imports and other dumb stuff

    packages=packages,
    install_requires=[
        'calendar_base',
        'requests',
    ],
    # metadata to display on PyPI
    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="An easy interface for Google Calendar",
    long_description=long_description,
    license="PSF",
    keywords="google calendar interface oauth flask grant miller",
    url="https://github.com/GrantGMiller/google_calendar_interface",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/google_calendar_interface",
    }

    # could also include long_description, download_url, classifiers, etc.
)

# to push to PyPI

# python -m setup.py sdist bdist_wheel
# twine upload dist/*