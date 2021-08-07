import os

from dotenv import load_dotenv

load_dotenv()

# Set a fixed string for development. Not suitable for production!
os.environ.setdefault('B_DJANGO_SECRET_KEY', 'development-key')

DJANGO_SECRET_KEY = os.environ['B_DJANGO_SECRET_KEY']
MONGO_URI = os.environ['B_MONGO_URI']