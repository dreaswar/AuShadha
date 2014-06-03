README File for the JS directory of ICD10 application
==========================================================

Introduction:
--------------

All custom JS codes, Dojo custom classes can be put here  

This is bootstrapped as a custom Dojo Module by its AMD at runtime  

The configuration file has to be loaded when the `render_icd10_pane` in `dijit_widgets/pane.py` is called  

Since the `pane` is parent view for any app, `dojoConfig` attribute which tell dojo to load the module is configured in `pane.yaml`  

- `dojoConfig` attribute set in `pane.yaml` provides three variables which are necessary for the AMD loader to push the `dojoConfig`  

- `dojoConfig` has three key attributes in pane.yaml: 
    1. `location` -- location of the JS file
    2. `main` -- name of the `main.js` or alternate JS file that identifies the module
    3. `name` -- name of the module

Appropriate settings to `{{STATIC_URL}}` has to be provided in the `AuShadha/settings.py` so that `icd10` is recognised as a module  







