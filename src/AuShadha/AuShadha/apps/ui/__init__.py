################################################################################
# Project     : AuShadha
# Description : Provides the UI app for AuShadha. The Core UI and its elements. 
# Date        : 15-10-2013
#
# This code is generously borrowed from Django's own admin app 
#
# See django.contrib.admin.__init__.py for details on how the parent applications
# sets it up
################################################################################

UI_INITIALIZED = False

def autodiscover():
    """
    Autogenerate registry
    """

    import copy
    from AuShadha import settings
    from AuShadha.apps.ui.ui import ui
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    global UI_INITIALIZED

    def load_modules():
      for app in settings.ENABLED_APPS:
          role = app['role']
          app_class = app['class_name']
          app = import_module( app['app'] )

          # Attempt to import the app's aushadha module.
          before_import_registry = copy.copy(ui.registry)
          print "Evaluating ", app, " for importing to UI"
          try:
              print "Printing Registry so far: "
              for k, v in before_import_registry.items(): 
                print k , '-->',  v ,'\n'
              import_module('%s.aushadha' % app)
          except:
              print "WARNING! Could not import:: ", app
              # Reset the model registry to the state before the last import as
              # this import will have to reoccur on the next request and this
              # could raise NotRegistered and AlreadyRegistered exceptions
              # (see #8245).
              ui.registry = before_import_registry

              # Decide whether to bubble up this error. If the app just
              # doesn't have an admin module, we can ignore the error
              # attempting to import it, otherwise we want it to bubble up.
              if module_has_submodule(app, 'aushadha'):
                  raise
      UI_INITIALIZED = True

    if not UI_INITIALIZED:
      load_modules()

#if not UI_INITIALIZED:
  #autodiscover()