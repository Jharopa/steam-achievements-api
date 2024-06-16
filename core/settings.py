import os
from dotenv import load_dotenv

load_dotenv()

# Postgresql connection details
POSTGRES_DB=os.environ.get('POSTGRES_DB')
POSTGRES_USER=os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST=os.environ.get('POSTGRES_HOST')
POSTGRES_PORT=int(os.environ.get('POSTGRES_PORT'))

STEAM_API_KEY=os.environ.get('STEAM_API_KEY')