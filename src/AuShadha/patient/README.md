========================
AuShadha-Patient
========================

This is a Patient Registration Application for AuShadha Open Source EMR

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "aushadha-patient" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'aushadha-patient',
    )

2. Include the aushadha-patient URLconf in your project urls.py like this::

    url(r'^patient/', include('aushadha-patient.urls')),

3. Run `python manage.py migrate` to create the aushadha-patient models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Develop the UI around the app ! Good Luck