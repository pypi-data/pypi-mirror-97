"""
Pip.Services Elasticsearch
------------------

Pip.Services is an open-source library of basic microservices.
pip_services3_elasticsearch  contains logging components with data storage on the Elasticsearch server.

Links
`````

* `website <http://github.com/pip-services/pip-services>`_
* `development version <http://github.com/pip-services3-python/pip-services3-elasticsearch-python>`

"""

from setuptools import setup
from setuptools import find_packages

readme = ''

try:
    readme = open('readme.md').read()
except:
    readme = __doc__

setup(
    name='pip_services3_elasticsearch',
    version='3.1.0',
    url='http://github.com/pip-services3-python/pip-services3-elasticsearch-python',
    license='MIT',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    description='ElasticSearch components for Pip.Services in Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'iso8601',
        'pytest',
        'pytz',
        'PyYAML',
        'moment',
        'elasticsearch',

        'pip-services3-commons',
        'pip-services3-components',
        'pip-services3-rpc'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]    
)
