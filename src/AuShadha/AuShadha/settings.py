# Django settings for AuShadha project.

import sys
import os
import yaml

ROOT_PATH = os.path.dirname(__file__)
PARENT_ROOT=os.path.abspath(os.path.join(ROOT_PATH, os.pardir))

APP_ROOT_URL = u"/AuShadha/"
LOGIN_URL = APP_ROOT_URL + u"login/"
LOGIN_REDIRECT_URL = APP_ROOT_URL


SERIALIZATION_MODULES = {
    'yml': "django.core.serializers.pyyaml"
}

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Dr.Easwar T.R', 'dreaswar@gmail.com'),
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Or path to database file if using sqlite3.
        'NAME': 'AuShadha.db',
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(ROOT_PATH, 'media')

CUSTOM_SCRIPT_ROOT = os.path.join(MEDIA_ROOT, 'custom/js/')
CUSTOM_STYLE_ROOT = os.path.join(MEDIA_ROOT, 'custom/styles/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = APP_ROOT_URL + 'media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(ROOT_PATH, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = APP_ROOT_URL + 'static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(ROOT_PATH, 'media/images'),
    os.path.join(ROOT_PATH, 'media'),
    os.path.join(ROOT_PATH, 'media/plugins'),
    #os.path.join(ROOT_PATH, 'media/custom/js'),
    os.path.join(ROOT_PATH, 'media/custom/styles'),
    os.path.join(ROOT_PATH, 'apps/ui/media'),

    # LIST ALL ADD - ON MODULE PATHS HERE USING FORMAT BELOW
    #os.path.join(PARENT_ROOT, '<PATH TO THE ADD-ON MEDIA DIRECTORY>'),
    #os.path.join(PARENT_ROOT, 'aushadha_demographics_us/demographics/media'),

)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 's25nwc+6sai0li&amp;g*0a97jjukn_(#sm1!8ublq%$1@o0c%@_^x'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'AuShadha.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'AuShadha.wsgi.application'

TEMPLATE_DIRS = (

    os.path.join(ROOT_PATH, 'templates'),
    os.path.join(ROOT_PATH, 'media/custom/js/'),
    os.path.join(ROOT_PATH, 'media/custom/styles'),

    os.path.join(ROOT_PATH, 'apps/search/templates/'),

    os.path.join(ROOT_PATH, 'apps/ui/templates/ui/'),
    os.path.join(ROOT_PATH, 'apps/ui/media/ui/'),
    
    os.path.join(ROOT_PATH, 'patient/templates/'),

    os.path.join(ROOT_PATH, 'demographics/demographics/templates/'),

    os.path.join(ROOT_PATH, 'history/medical_history/templates/'),
    os.path.join(ROOT_PATH, 'history/surgical_history/templates/'),
    os.path.join(ROOT_PATH, 'history/family_history/templates/'),
    os.path.join(ROOT_PATH, 'history/social_history/templates/'),
    #os.path.join(ROOT_PATH, 'history/obs_and_gyn/templates/'),    

    os.path.join(ROOT_PATH, 'immunisation/templates/'),
    os.path.join(ROOT_PATH, 'medication_list/templates/'),    
    os.path.join(ROOT_PATH, 'allergy_list/templates/'),    

    os.path.join(ROOT_PATH, 'visit/visit/templates/'),
    os.path.join(ROOT_PATH, 'visit/visit_complaints/templates/'),
    os.path.join(ROOT_PATH, 'visit/visit_hpi/templates/'),
    os.path.join(ROOT_PATH, 'visit/visit_ros/templates/'),
    os.path.join(ROOT_PATH, 'visit/visit_phyexam/templates/'),
    os.path.join(ROOT_PATH, 'visit/visit_assessment_and_plan/templates/'),
    os.path.join(ROOT_PATH, 'visit/visit_soap/templates/'),

#    os.path.join(ROOT_PATH, 'visit/visit_imaging/templates/'),
#    os.path.join(ROOT_PATH, 'visit/visit_inv/templates/'),
#    os.path.join(ROOT_PATH, 'visit/visit_procedures/templates/'),

    os.path.join(ROOT_PATH, 'admission/admission/templates/'),
#    os.path.join(ROOT_PATH, 'admission/admission_complaints/templates/'),
#    os.path.join(ROOT_PATH, 'admission/admission_hpi/templates/'),
#    os.path.join(ROOT_PATH, 'admission/admission_ros/templates/'),    
#    os.path.join(ROOT_PATH, 'admission/admission_phyexam/templates/'),
#    os.path.join(ROOT_PATH, 'admission/admission_imaging/templates/'),
#    os.path.join(ROOT_PATH, 'admission/admission_inv/templates/'),
#    os.path.join(ROOT_PATH, 'admission/admission_procedures/templates/'),    

    #os.path.join(ROOT_PATH, 'phyexam/templates/'),    

    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

)

INSTALLED_APPS = (

    # Core Django Apps used 
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # Core AuShadha Apps, base_models, custom_users:
    'AuShadha.apps.ui',
    'AuShadha.apps.aushadha_base_models',
    'AuShadha.apps.aushadha_users',
    'AuShadha.apps.clinic',
    'AuShadha.apps.search',

    # Core AuShadha Registry for ICD 10 codes, ICD 10 PCS codes, Drug Database
    #   and Vaccine Registry
    'registry.icd10',
    'registry.icd10_pcs',
    'registry.drug_db',
    'registry.inv_and_imaging',
    'registry.vaccine_registry',    

    # Custom Apps for Patient Registration
    'patient',

    #AuShadha Stock apps for Admission and OPD Visits
    'admission.admission',
#    'admission.admission_complaints',
#    'admission.admission_hpi',
#    'admission.admission_ros',
#    'admission.admission_phyexam',
#    'admission.admission_procedures',
#    'admission.admission_imaging',
#    'admission.admission_inv',

    # Custom Apps for Patient Demographics
    'demographics.demographics',
    'demographics.contact',
    'demographics.phone',
    'demographics.guardian',
    #'demographics.email_and_fax',

    # AuShadha stock apps for History
    'history.medical_history',
    'history.surgical_history',
    'history.social_history',
    'history.family_history',
    #'history.obs_and_gyn',

    #AuShadha Stock apps for Medication List, Allergy, Immunisaion
    'medication_list',
    'allergy_list',
    'immunisation',

    'visit.visit',
    'visit.visit_complaints',
    'visit.visit_hpi',
    'visit.visit_ros',
    'visit.visit_phyexam',
    'visit.visit_assessment_and_plan',
    'visit.visit_soap',    

#    'visit.visit_inv',
#    'visit.visit_imaging',
#    'visit.visit_procedures',


    #AuShadha Stock for Physical Examination Management
    #'phyexam',
)

ENABLED_APPS = yaml.load( open('AuShadha/configure.yaml').read() ) # This settings doesnt do anything now. 


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

UI_INITIALIZED = False
