import os
import sys
import json
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard_project.settings')

# Import Django
import django
from django.core.wsgi import get_wsgi_application

# Setup Django
django.setup()

# Get the WSGI application
app = get_wsgi_application()

def handler(event, context):
    """Netlify function handler for Django"""
    try:
        from django.core.handlers.wsgi import WSGIHandler

        # Log the incoming request for debugging
        print(f"Netlify function called: {event['httpMethod']} {event['path']}")

        # Convert Netlify event to WSGI environ
        environ = {
            'REQUEST_METHOD': event['httpMethod'],
            'SCRIPT_NAME': '',
            'PATH_INFO': event['path'],
            'QUERY_STRING': event.get('queryStringParameters', '') or '',
            'CONTENT_TYPE': event['headers'].get('content-type', ''),
            'CONTENT_LENGTH': str(len(event.get('body', '') or '')),
            'SERVER_NAME': event['headers'].get('host', 'netlify'),
            'SERVER_PORT': '443',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': event.get('body', '') or '',
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }

        # Add all headers
        for header, value in event.get('headers', {}).items():
            key = f'HTTP_{header.upper().replace("-", "_")}'
            environ[key] = value

        # Handle the request
        handler = WSGIHandler()

        # Collect response
        status_code = None
        headers = []
        body_parts = []

        def start_response(status, response_headers, exc_info=None):
            nonlocal status_code, headers
            status_code = int(status.split()[0])
            headers = response_headers

        # Get the response
        response = handler(environ, start_response)

        # Read the response body
        if hasattr(response, 'read'):
            body_parts.append(response.read())
        else:
            for part in response:
                body_parts.append(part)

        body = b''.join(body_parts)

        # Convert headers to Netlify format
        response_headers = {}
        for header, value in headers:
            response_headers[header] = value

        # Ensure we have a status code
        if status_code is None:
            status_code = 200

        print(f"Response: {status_code}, body length: {len(body)}")

        return {
            'statusCode': status_code,
            'headers': response_headers,
            'body': body.decode('utf-8') if isinstance(body, bytes) else str(body),
        }

    except Exception as e:
        print(f"Error in Netlify function: {str(e)}")
        import traceback
        traceback.print_exc()

        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Internal Server Error',
                'message': str(e)
            })
        }