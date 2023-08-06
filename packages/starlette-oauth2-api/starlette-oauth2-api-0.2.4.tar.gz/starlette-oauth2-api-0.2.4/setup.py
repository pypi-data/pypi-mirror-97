import os
import setuptools


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='starlette-oauth2-api',
    version='0.2.4',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/jorgecarleitao/starlette-oauth2-api',
    author='Jorge C. Leitao',
    author_email='jorgecarleitao@gmail.com',
    py_modules=['starlette_oauth2_api'],
    install_requires=[
        'starlette>=0.12,<1',
        'python-jose>=3,<4',
    ]
)
