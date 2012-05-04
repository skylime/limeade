#!/usr/bin/env python2

import sys
import os


try:
    import settings
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

def run(settings):
    if not os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'third-party') in sys.path:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'third-party'))
    if not os.path.dirname(os.path.dirname(os.path.abspath(__file__))) in sys.path:
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from django.core.management import execute_manager
    execute_manager(settings)


if __name__ == "__main__":
    run(settings)

