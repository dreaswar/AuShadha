##########################################################################
# Project     : AuShadha
# Description : Sets up the applications to be loaded. Registers the applications for a role
# Date        : 15-10-2013
#
# This code is generously borrowed from Django's own admin app
#
# See django.contrib.admin.__init__.py for details on how the parent applications
# sets it up
##########################################################################


import importlib
import copy

from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

from AuShadha import settings
print 'starting up'
from AuShadha.apps.ui.ui import ui as UI


def autoload():
    """
    Autogenerate application registry.
    Iterates through the application's aushadha.py and
    registers apps for various roles in AuShadha
    """
    def load_modules():

        for app in settings.INSTALLED_APPS:
            app_module = import_module(app)
            # print app_module
            try:
                try:
                    import_module("{}.aushadha".format(app))
                except (ImportError):
                    continue
                import_module("{}.models".format(app))

            except:
                if module_has_submodule(app_module, 'aushadha'):
                    raise
                if module_has_submodule(app_module, 'models'):
                    raise

        for app in settings.ENABLED_APPS:
            app_module = import_module(app['app'])
            role = app['role']
            class_name = app['class_name']

            try:
                module = import_module(
                    "{}.{}".format(
                        app['app'], app['module']))
                class_obj = getattr(module, class_name)
                UI.registry[role] = ''
                UI.registry[role] = class_obj

            except (AttributeError, ImportError) as err:
                settings.UI_INITIALIZED = False
                raise Exception(err)

            except:
                if module_has_submodule(app_module, app['module']):
                    raise

        settings.UI_INITIALIZED = True
        # print "*" * 100
        # print UI.registry
        # print "*" * 100

    if not settings.UI_INITIALIZED:
        load_modules()


def run():
    if not settings.UI_INITIALIZED:
        autoload()
    else:
        return
