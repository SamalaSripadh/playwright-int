import os

from dotenv import load_dotenv


load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")
API_BASE_URL = os.getenv("API_BASE_URL", f"{BASE_URL}/api")
AUTH_EMAIL = os.getenv("AUTH_EMAIL")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")
AUTH_FILE = os.getenv("AUTH_FILE", ".auth/user.json")
