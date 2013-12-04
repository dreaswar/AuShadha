========================
AuShadha-Contact
========================

Maintains the Contact Functionality of a AuShadha project

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "aushadha-contact" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'aushadha-contact',
    )

2. Include the aushadha-contact URLconf in your project urls.py like this::

    url(r'^contact/', include('aushadha-contact.urls')),

3. Run `python manage.py migrate` to create the aushadha-contact models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Develop the UI around the app ! Good Luck