========================
Aushadha-Allergy_list
========================

This app is part of AuShadha Open Source EMR.
This manages the Allergy of a patient

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "allergy_list" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'allergy_list',
    )

2. Include the allergy_list URLconf in your project urls.py like this::

    url(r'^allergy_list/', include('allergy_list.urls')),

3. Run `python manage.py migrate` to create the allergy_list models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Develop the UI around the app ! Good Luck