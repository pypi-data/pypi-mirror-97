#!/usr/bin/env python
if __name__ == "__main__":
    import sys
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = \
        'lino_welfare.projects.mathieu.settings.demo'
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
