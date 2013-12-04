========================
AuShadha-Immunisation
========================

Immunisation Managemen module for AuShadha

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "aushadha-immunisation" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'aushadha-immunisation',
    )

2. Include the aushadha-immunisation URLconf in your project urls.py like this::

    url(r'^immunisation/', include('aushadha-immunisation.urls')),

3. Run `python manage.py migrate` to create the aushadha-immunisation models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Develop the UI around the app ! Good Luck