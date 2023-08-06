from setuptools import find_packages, setup


setup(
    name = 'authenticating-python',
    packages = ['authenticating', 'authenticating.utils'],
    version = '0.1.2',
    description = 'authenticating.com-python',
    author = 'SmokingGoaT',
    license = 'MIT',
    url = 'https://github.com/SmokingTheGoaT/authenticating.com-python',
    zip_safe = False,
    install_requires = [
        'requests',
        'requests_oauthlib',
        'simplejson',
    ]
)