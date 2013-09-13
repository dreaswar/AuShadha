AuShadha  (औषध)
========

AuShadha (औषध): Means medicine in Sanskrit. 

This is a Open Source Electornic Medical Records (EMR) & Public Health Management System for Small Clinics.

It might be even suited for speciality medical practice after some customisation. 

It is developed with Python, Django and Dojo 

For Development the code uses sqlite3 database, but with Django DB backend we can extend this to any database ( PostgresSQL is preferred ).

AuShadha code is licensed under GNU-GPL Version 3. Django, Dojo, Icons and other thrid party modules are licensed as per their authors. This should be honoured.


Aims
====

There are many great Open Source EMR and Clinic Management projects, but most of them have very poor front ends. 

As in life, beauty and usability are key in medical practice.

It is natural that more visually appealing it is more you want to use it. 

AuShadha will strive to achieve a balance between back and front end design. 

To achieve that aim Django and Dojo has been chosen. 

AuShadha is designed by me, a Medical Doctor in association with other Developers, so usability and practicability will always be foremost. 

AuShadha benefits from inputs, feature requests from my medical colleagues as the development progresses. 


How to Test
===========

1) For AuShadha requirements please refer to REQUIREMENTS.txt in docs/

2) AuShadha has been tested and developed with Python 2.7, Django 1.4.1 and Dojo 1.7.2 in Linux. It should work as long as dependencies are satisfied.

3) Ideally create a Python Virtual Environment. If virtualenv is not installed, please run in Debian systems <code> sudo easy_install virtualenv </code>

4) After installing virtualenv, Create a Python Virtual Environment <code> virtualenv python_env </code>

5) Change the working directory to the virtualenv folder <code> cd python_env</code> and activate it <code> source bin/activate </code>

6) With Python pip installed, run <code> pip install -f ../docs/REQUIREMENTS.txt </code> if you are in python_env directory . This will install all the necessary dependencies you need. 

You may need to install Python development libraries if you are on Linux. Required to compile PIL. 

`$ apt-get install python-dev #in debian systems.` 

`$ yum install python-devel #in Redhat-like systems.`

7) cd into src/AuShadha directory <code> cd src/AuShadha </code> 

8) run <code> python manage.py runserver </code>

9) Use your browser to navigate to <link> http://localhost:8000/AuShadha/ </link> . You will be greeted with a login page. Use username = admin, password = admin for a trial run.

10) Please read the issues, license before using. Currently AuShadha is under active development and is not fit in anyway for real world use.

Project Structure
=================

1) AuShadha_logo : Contains the logo, with SVG and .png file along with License.  

2) docs : Contains the Requirements.txt, License.txt  

3) src : Project Source Code, Media files(Icons,Images, File uploads), Javscript (custom and Dojo)  

4) README.md  

5) LICENSE.txt  



Development Status
==================
Patient Registration Module done  
Patient History, Medication Module completed  
Allergy Module completed  
Outpatient Visit Module in progress, nearing completion  
  
ICD 10, ICD 10 PCS parser's output incorporated as a fixture  
FDA medication list included as a fixture after parsing from FDA xml file  



Developement Roadmap    
====================
Surgical Procedure module will be next  
In-patient Admission management module along with Progress notes  
Pharmacy, Billing and Inventory to follow  
  
Specific public health modules like Paediatrics, Neonatology, Gynaecology/ Obstetrics will be last as by then
 he interdependencies will be solved  


Want to participate ?
====================

Suggestions and participation are welcome.   

Please email me at dreaswar@gmail.com  
Visit me at http://www.dreaswar.com  
Follow me at http://www.twitter.com/aushadhaemr/
Follow the Project news at http://www.facebook.com/AuShadha/  

