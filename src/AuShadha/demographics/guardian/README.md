========================
AuShadha-Guardian
========================

Guardian Contact and management application for AuShadha Open Source EMR
Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "aushadha-guardian" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'aushadha-guardian',
    )

2. Include the aushadha-guardian URLconf in your project urls.py like this::

    url(r'^guardian/', include('aushadha-guardian.urls')),

3. Run `python manage.py migrate` to create the aushadha-guardian models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Develop the UI around the app ! Good Luck