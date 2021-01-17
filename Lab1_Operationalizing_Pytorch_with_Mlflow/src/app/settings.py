from os import environ
from dotenv import load_dotenv
load_dotenv()

SERVE_URI = environ.get("SERVE_URI")
