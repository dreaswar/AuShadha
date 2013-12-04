========================
AuShadha-SurgicalHistory
========================

SurgicalHistory management application for AuShadha Open Source EMR

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "aushadha-surgical_history" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'aushadha-surgical_history',
    )

2. Include the aushadha-surgical_history URLconf in your project urls.py like this::

    url(r'^surgical_history/', include('aushadha-surgical_history.urls')),

3. Run `python manage.py migrate` to create the aushadha-surgical_history models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Develop the UI around the app ! Good Luck