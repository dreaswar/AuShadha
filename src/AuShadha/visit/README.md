========================
AuShadha-Visit
========================

This is a Patient Registration Application for AuShadha Open Source EMR

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "aushadha-visit" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'aushadha-visit',
    )

2. Include the aushadha-visit URLconf in your project urls.py like this::

    url(r'^visit/', include('aushadha-visit.urls')),

3. Run `python manage.py migrate` to create the aushadha-visit models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Develop the UI around the app ! Good Luck