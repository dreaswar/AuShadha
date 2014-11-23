#!/usr/bin/env python
import os
import sys

def fix_reload(v):
    if '--noreload' in v: return v
    if v[1] == 'runserver':
        return v[:2] + ['--noreload'] + v[2:]
    return v

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AuShadha.settings")

    
    print "Trying to run custom code at startup..."
    print "Loading apps and roles from configure.yaml"
    import AuShadha.startup as startup
    startup.run()
    print "Roles for UI loaded"

    from django.core.management import execute_from_command_line

    sys.argv = fix_reload(sys.argv)
    execute_from_command_line(sys.argv)
