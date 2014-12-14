Installation of AuShadha
========================

How to Test
^^^^^^^^^^^^^

1. For AuShadha requirements please refer to REQUIREMENTS.txt in docs/

2. AuShadha has been tested and developed with Python 2.7, Django 1.6x and Dojo 1.8x in Linux. It should work as long as dependencies are satisfied.

Creating a Virtual Environment to run:
---------------------------------------
3. Ideally create a Python Virtual Environment. If virtualenv is not installed, please run in Debian systems sudo easy_install virtualenv

4. After installing virtualenv, Create a Python Virtual Environment virtualenv python_env

5. Change the working directory to the virtualenv folder cd python_env and activate it source bin/activate


Installing Dependencies:
--------------------------

6. With Python pip installed, run pip install -r ../docs/REQUIREMENTS.txt if you are in python_env directory . This will install all the necessary dependencies you need.

7. You may need to install Python development libraries if you are on Linux.


    `$ apt-get install python-dev` #in debian systems.


    `$ yum install python-devel` #in Redhat-like systems.


8. cd into src/AuShadha directory  `cd src/AuShadha`


Prepare and Download Dojo Javascript Library
----------------------------------------------

9. Latest Dojo Library can be downloaded at : http://dojotoolkit.org/download/


   Download the latest Dojo library and extract it into `AuShadha/src/AuShadha/AuShadha/media/plugins/dojo/`


   After extracting the folder structure should be like: dojo/dojo/ dojo/dojox/ dojo/dijit/ 

  
   AuShadha has been tested with Dojo 1.8.1



Prepare the database and install the fixtures
-----------------------------------------------


9. run `$ python manage.py syncdb && python manage.py runserver`



See it in action & login
----------------------------

10. Use your browser to navigate to http://localhost:8000/AuShadha/ 


    You will be greeted with a login page. Use username = admin, password = admin for a trial run.


11. Please read the issues, license before using. 


    Currently AuShadha is under active development and is not fit in anyway for real world use.
