import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='aushadha-phyexam',
    version='0.01',
    packages=['dijit_widgets'],
    include_package_data=True,
    license='GNU-GPL Version 3',  
    description='Physical Examination Application for AuShadha',
    long_description=README,
    url='http://www.aushadha.org/',
    author='Dr. Easwar T.R',
    author_email='dreaswar@gmail.com',
    install_requires=[
        "aushadha >= 0.01",
        "aushadha-registry >= 0.01",        
        "aushadha-patient >= 0.01",
        "aushadha-medical_history >= 0.01",
        "aushadha-surgical_history >= 0.01",
        "aushadha-social_history >= 0.01",
        "aushadha-family_history >= 0.01",
        "aushadha-demographics >= 0.01",
        "aushadha-contact >= 0.01",
        "aushadha-phone >= 0.01",
        "aushadha-guardian >= 0.01",
        "aushadha-admission >= 0.01",
        "aushadha-visit >= 0.01",
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
