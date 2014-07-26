import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='aushadha',
    version='0.01',
    packages=['src'],
    include_package_data=True,
    license='GNU-GPL Version 3',  
    description='This is the Core AuShadha Open Source EMR application',
    long_description=README,
    url='http://www.aushadha.org/',
    author='Dr. Easwar T.R',
    author_email='dreaswar@gmail.com',
    install_requires=[
        'Django>=1.6',
        'PyYAML>=3.10',
        'Sphinx>=1.2b2',
        'psycopg2',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU-GPL Version 3 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # replace these appropriately if you are using Python 3
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
