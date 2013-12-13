========================
AuShadha-Admission
========================

AuShadha-Admission is an Admission management application for AuShadha Open Source EMR

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "aushadha-admission" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'aushadha-admission',
    )

2. Include the aushadha-admission URLconf in your project urls.py like this::

    url(r'^admission/', include('aushadha-admission.urls')),

3. Run `python manage.py migrate` to create the aushadha-admission models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Develop the UI around the app ! Good Luck