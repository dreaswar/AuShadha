import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

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
        'Django==1.5.4',
        'Jinja2==2.7.1',
        'MarkupSafe==0.18',
        'PIL==1.1.7',
        'Pillow==2.0.0',
        'PyYAML==3.10',
        'Pygments==1.6',
        'South==0.8.1',
        'Sphinx==1.2b2',
        'argparse==1.2.1',
        'autopep8==0.9.3',
        'django-tinymce==1.5.1',
        'docformatter==0.5.5',
        'docutils==0.11',
        'html5lib==1.0b1',
        'jsbeautifier==1.4.0',
        'pep8==1.4.6',
        'pisa==3.0.33',
        'pyPdf==1.13',
        'reportlab==2.7',
        'six==1.3.0',
        'untokenize==0.1',
        'wsgiref==0.1.2',
        'xhtml2pdf==0.0.5',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU-GPL Version 3 License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # replace these appropriately if you are using Python 3
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
