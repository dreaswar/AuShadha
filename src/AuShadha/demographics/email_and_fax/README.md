========================
AuShadha-EmailAndFax
========================

Email and Fax managmeent application for AuShadha Open Source EMR

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "aushadha-email_and_fax" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'aushadha-email_and_fax',
    )

2. Include the aushadha-email_and_fax URLconf in your project urls.py like this::

    url(r'^email_and_fax/', include('aushadha-email_and_fax.urls')),

3. Run `python manage.py migrate` to create the aushadha-email_and_fax models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Develop the UI around the app ! Good Luck