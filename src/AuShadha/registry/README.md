========================
AuShadha-Registry
========================

Registry for ICD10, ICD10 PCS, Vaccines, Investigation & Imaging Management module for AuShadha

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "aushadha-registry" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'aushadha-registry',
    )

2. Include the aushadha-registry URLconf in your project urls.py like this::

    url(r'^registry/', include('aushadha-registry.urls')),

3. Run `python manage.py migrate` to create the aushadha-registry models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Develop the UI around the app ! Good Luck