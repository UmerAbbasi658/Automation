from dotenv import load_dotenv
import os

load_dotenv()  # <-- Make sure this is here to load .env

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = "https://gov-recruitment-marketing.offorte.com"

# Optional: debug print
print("EMAIL loaded:", EMAIL)
print("PASSWORD loaded:", PASSWORD)