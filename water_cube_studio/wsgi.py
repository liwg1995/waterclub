"""
WSGI config for water_cube_studio project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'water_cube_studio.settings')

application = get_wsgi_application()
