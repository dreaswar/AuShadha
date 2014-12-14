Introduction to AuShadha Project
================================


AuShadha (औषध): Means medicine in Sanskrit.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a Open Source Electornic Medical Records (EMR) & Public Health Management System for Small Clinics. It might be even suited for speciality medical practice after some customisation. It is developed with Python, Django and Dojo. Development and Deployment will use PostgreSQL. However the option to use sqlite DB is entirely open for small installtions who are not anticipating traffic. 
    

License
^^^^^^^^

AuShadha code is licensed under GNU-GPL Version 3. Django, Dojo, Icons and other thrid party modules are licensed as per their authors. This should be honoured.
    

Aims
^^^^^^

There are many great Open Source EMR and Clinic Management projects, but most of them have very poor front ends. As in life, beauty and usability are key in medical practice. It is natural that more visually appealing it is more you want to use it. AuShadha will strive to achieve a balance between back and front end design. To achieve that aim Django and Dojo has been chosen. AuShadha is designed by me, a Medical Doctor in association with other Developers, so usability and practicability will always be foremost.AuShadha benefits from inputs, feature requests from my medical colleagues as the development progresses.
    
How to Test
^^^^^^^^^^^^^

Setup the PostgreSQL database for your OS
------------------------------------------
Please refer to your OS notes on how to do this.  
AuShadha has been tested with PostgreSQL Server version 9.3  
Once you have installed Postgres server and pgadmin3 client you should be able to run `psql` from terminal and get a prompt

Creating and AuShadha PostgreSQL database
------------------------------------------
Preferred DB for running AuShadha is PostgreSQL. 

1. Set up PG for your OS  
     Please see your OS website for instructions on setting up PG   
     PG should be is setup and accesible from command line as >> psql prompt  


2. Set up a System user with same name as the Postgres user  
     Create an OS user with `<adduser>` command from terminal  
     Create a `/home/<user_name>` directory for the user and run `chown -R <user_name> /home/<user_name>`  
     The username used by default for DB and user is `'aushadha'` with password of `aushadha`  

3. Create an empty DB and Grant permissions
     From terminal run the `createuser` to create and user with username `'aushadha'`  
     Run `psql` to get into the pg command line from the user that is allowed to run `psql`  

4. Run the following  
    `CREATE DATABASE aushadha WITH OWNER aushadha;`  

    `GRANT ALL ON DATABASE aushadha TO <system_os_user> WITH GRANT OPTION;`  



Installing Dependencies for AuShadha
-------------------------------------

1. For AuShadha requirements please refer to REQUIREMENTS.txt in docs/

2. AuShadha has been tested and developed with Python 2.7, Django 1.7x and Dojo 1.9x in Linux. It should work as long as dependencies are satisfied.


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
 
   You may need to create a 'dojo' directory inside `AuShadha/src/AuShadha/AuShadha/media/plugins/` directory


   After extracting the folder structure should be like: dojo/dojo/ dojo/dojox/ dojo/dijit/ 

  
   AuShadha has been tested with Dojo 1.9x



Prepare the database and install the fixtures
-----------------------------------------------


9. run `$ python manage.py makmigrations && python.manage.py migrate`

10. You need to create a superuser for logging in to the Django administration site. 
    Do that with `python manage.py createsuperuser` 

11. Run the server with `python manage.py runserver`

12. Navigate to http://localhost:8000/AuShadha/admin and login with the user you just created. 

13. You will need to add `Users` as needed and assign them Roles & permissions

14. Please note that AuShadha has role and permission based UI. Hence for evaluation, you would need to login as the user with
    appropriate permissions. For a superuser please set the option in Staff's `ausshadha_user_role` to `aushadha_admin` and 
    `clinic_staff_role` to `doctor`. Any other lesser permission setting would shut parts of the UI.



See it in action & login
----------------------------

15. Use your browser to navigate to http://localhost:8000/AuShadha/ 


    You will be greeted with a login page. 



16. Please read the issues, license before using. 


    Currently AuShadha is under active development and is not fit in anyway for real world use.



Project Structure
^^^^^^^^^^^^^^^^^^^

1. docs : Contains the Requirements.txt, License.txt along with Sphinx apidoc

2. src : Project Source Code, Media files(Icons,Images, File uploads), Javscript

3. README.md

4. LICENSE.txt


Plan
^^^^^

AuShadha project is split between AuShadha-stock ( which contains AuShadha-core and some Stock applications) and Au-Pluggable ( the pluggable modules for AuShadha ). 

These two repositories are maintained side by side to encourage a basic application which most users would want to use and also provide an easy way for regional/per-user customisation. User can freely mix and match the modules he wants to create his own AuShadha brew. In other words he is not stuck with what the developer has packaged and is free to repackage it in any way he wants. 

The AuShadha-core will help him / her create pluggable applications that integrate well into AuShadha, but user is also free to create a completely different Django application. As long as he / she sticks to the Django pluggable practices the application can be easily integrated into AuShadha. Of course if he were to use AuShadha-core's API to develop he can do it more easily. AuShadha-core API is very young, mostly untested. It is very thin layer on top of Django. It does not force the developer to re-learn anything that would not be useful outside AuShadha. 



Completed Modules
^^^^^^^^^^^^^^^^^^
1. AuShadha-core  
    - Core of AuShadha, 
    - Providing basic utilities for fast app building and scaffolding

2. AuShadha-PatientRegistration  
    - Registration of Patient to the Clinic

3. AuShadha-Contact  
    - Patient Address management

4. AuShadha-Phone   
    - Phone contact management

5. AuShadha-Guardian   
    - Guardian information

6. AuShadha-Demographics  
    - Management of Demographics Data

7. AuShadha-MedicationList  
    - Management of Prescriptions and Medications

8. AuShadha-AllergyList  
    - Management of Allergies

9. AuShadha-History 
    - Medical History, Surgical History, Social History, Family History

10. AuShadha-Immunisation   
    - Immunisation Status management application

11. AuShadha-OPD_Visit Management 
    - Complaints, HPI, ROS, Physical Exam System Wise
    - Orders, Prescription, Procedures (in progress)

12. AuShadha-ICD10-Disease Code Browser  

13. AuShadha-ICD10-PCS 
    - Procedure Coding System Browser

14. AuShadha-FDA-Drug List Browser integrated with some Drugbank
    - http://drugbank.ca for reference information  

15. AuShadha-vaccine_registry  
     - CDC-Vaccine List(CVX),
     - CDC CVX-MVX mapping, 
     - CDC VIS 
     - CDC Vaccine schedules for Children, Adolescents, Adults
     - Further info at http://cdc.gov/


Pluggable Modules under Developement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- currently under development

1. aushadha_demographics_us 
    -  Patient Demographics data collection as done in USA 
2. aushadha_demographics_in 
    -  Patient Demographics data collection as done in India 
3. icd10_pcs
    -  An alternate implementation of Derek's version of ICD10PCS app by Easwar 

4. dynamic_aushadha_models
    - A solution to autogenerate an app, its files with scaffolding and CRUD 
      from a model structure given as YAML file. This was designed to work with
      South project and before Django1.7 introduced support for migrations. 
      This is just a work in progress as South is no longer relevant for this and
      needs to be removed. 

Pluggable Modules Planned
^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. aushadha_obs_and_gyn_in
2. aushadha_immunisation_in
3. aushadha_neonatal_in


For Developers
^^^^^^^^^^^^^^^^^^^^^

Suggestions and participation are welcome.  

Please email me at dreaswar@gmail.com 

Mailing list : aushadha@googlegroups.com

Website :  http://aushadha.org 

Blog: http://blog.aushadha.org  

Wiki: http://wiki.aushadha.org  

Facebook:  http://www.facebook.com/AuShadha/  

Twitter : @aushadha_emr


Repository
^^^^^^^^^^^^^

1. http://github.com/dreaswar/AuShadha 

2. http://github.com/dreaswar/Au-Pluggables


The Documentation @readTheDocs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

https://readthedocs.org/projects/aushadha/


