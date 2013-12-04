========================
AuShadha-MedicationList
========================

MedicationList management application for AuShadha Open Source EMR

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "aushadha-medication_list" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'aushadha-medication_list',
    )

2. Include the aushadha-medication_list URLconf in your project urls.py like this::

    url(r'^medication_list/', include('aushadha-medication_list.urls')),

3. Run `python manage.py migrate` to create the aushadha-medication_list models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Develop the UI around the app ! Good Luck