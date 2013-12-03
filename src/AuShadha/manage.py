#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AuShadha.settings")

    
    print "Trying to run custom code at startup..."
    print "Loading apps and roles from configure.yaml"
    import AuShadha.startup as startup
    startup.run()
    print "Roles for UI loaded"

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
