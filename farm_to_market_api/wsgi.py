"""
WSGI config for farm_to_market_api project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_to_market_api.settings')

application = get_wsgi_application() 