Introduction to AuShadha Project
================================


AuShadha (औषध): Means medicine in Sanskrit.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a Open Source Electornic Medical Records (EMR) & Public Health Management System for Small Clinics. It might be even suited for speciality medical practice after some customisation. It is developed with Python, Django and Dojo. For Development the code uses sqlite3 database. Deployment will use PostgreSQL. 
    

License
^^^^^^^^

AuShadha code is licensed under GNU-GPL Version 3. Django, Dojo, Icons and other thrid party modules are licensed as per their authors. This should be honoured.
    

Aims
^^^^^^

There are many great Open Source EMR and Clinic Management projects, but most of them have very poor front ends. As in life, beauty and usability are key in medical practice. It is natural that more visually appealing it is more you want to use it. AuShadha will strive to achieve a balance between back and front end design. To achieve that aim Django and Dojo has been chosen. AuShadha is designed by me, a Medical Doctor in association with other Developers, so usability and practicability will always be foremost.AuShadha benefits from inputs, feature requests from my medical colleagues as the development progresses.
    
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


Project Structure
^^^^^^^^^^^^^^^^^^^

2. docs : Contains the Requirements.txt, License.txt


3. src : Project Source Code, Media files(Icons,Images, File uploads), Javscript


4. README.md


5. LICENSE.txt


Plan
^^^^^

AuShadha project is split between AuShadha-stock ( which contains AuShadha-core and some Stock applications) and Au-Pluggable ( the pluggable modules for AuShadha ). 

User can freely mix and match the modules he wants to create his own AuShadha brew. 

In other words he is not stuck with what the developer has packaged and is free to repackage it in any way he wants. 

The AuShadha-core will help him / her create pluggable applications that integrate well into AuShadha, but user is also free to create a completely different Django application. 

As long as he / she sticks to the Django pluggable practices the application can be easily integrated into AuShadha. 

Of course if he were to use AuShadha-core's API to develop he can do it more easily. 

AuShadha-core API is very young, mostly untested. It is very thin layer on top of Django. 

It does not force the developer to re-learn anything that would not be useful outside AuShadha. 



Completed Modules
^^^^^^^^^^^^^^^^^^

1. AuShadha ( or AuShadha-core ) with its bundled core-apps
2. AuShadha-PatientRegistration (aushadha_patient )
3. AuShadha-Contact ( aushadha_demographics_contact )
4. AuShadha-Phone  ( aushadha_demographics_phone )
5. AuShadha-Guardian ( aushadha_demographics_guardian )
6. AuShadha-Demographics ( aushadha_demographics )
7. AuShadha-MedicationList ( aushadha_medication_list )
8. AuShadha-AllergyList ( aushadha_allergy_list )
9. AuShadha-History ( aushadha_history )
10. AuShadha-OPD_Visit ( aushadha_visit )


Pluggable Modules under Developement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- currently under development

1. aushadha_demographics_us
2. aushadha_demographics_in


Pluggable Modules Planned
^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. aushadha_obs_and_gyn_in
2. aushadha_immunisation_in
3. aushadha_neonatal_in


For Developers
^^^^^^^^^^^^^^^^^^^^^

Suggestions and participation are welcome.  

Please email me at dreaswar@gmail.com or Google Groups at aushadha@googlegroups.com

Visit project website at http://aushadha.org. 

Follow the Project news at http://www.facebook.com/AuShadha/


Repository
^^^^^^^^^^^^^

1. http://github.com/dreaswar/AuShadha 

2. http://github.com/dreaswar/Au-Pluggables


The Documentation @readTheDocs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

https://readthedocs.org/projects/aushadha/


