"""WSGI entrypoint for production servers (e.g. Gunicorn).

Creates the Flask application instance as the variable `app` so WSGI servers can
import it using `wsgi:app`.
"""
from app import create_app

app = create_app()
