import os
from datetime import timedelta


class Config:
    """Конфігурація Flask-додатка."""
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'flask-super-secret-key-cybersec-lab56'
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # Час життя токена в секундах
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
