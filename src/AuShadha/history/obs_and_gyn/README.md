==========================
AuShadha-ObsAndGynHistory
==========================

Obstetric and Gynaecology Management Application for AuShadha

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "aushadha-obs_and_gyn_history" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'aushadha-obs_and_gyn_history',
    )

2. Include the aushadha-obs_and_gyn_history URLconf in your project urls.py like this::

    url(r'^obs_and_gyn_history/', include('aushadha-obs_and_gyn_history.urls')),

3. Run `python manage.py migrate` to create the aushadha-obs_and_gyn_history models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Develop the UI around the app ! Good Luck