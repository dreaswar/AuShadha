========================
{{app_name.capitalize}}
========================

This is an app stub..

< Your description of the app and its functions should go here >

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "{{app_name}}" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        '{{app_name}}',
    )

2. Include the {{app_name}} URLconf in your project urls.py like this::

    url(r'^{{app_name}}/', include('{{app_name}}.urls')),

3. Run `python manage.py migrate` to create the {{app_name}} models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Develop the UI around the app ! Good Luck