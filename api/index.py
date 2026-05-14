import os
import sys
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard_project.settings')

# Setup Django
import django
django.setup()

# Import the WSGI application
from dashboard_project.wsgi import application

# Vercel expects the app to be named 'app'
app = application