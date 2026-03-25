from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Credentials
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = "https://gov-recruitment-marketing.offorte.com"  # hardcoded as requested

# Optional: debug prints (does not expose sensitive info)
print("✅ EMAIL loaded:", EMAIL is not None)
print("✅ PASSWORD loaded:", PASSWORD is not None)
print("✅ BASE_URL set to:", BASE_URL)

# Helper function to construct a dynamic proposal URL
def get_proposal_url(proposal_id):
    """Return the full URL for a given proposal ID."""
    return f"{BASE_URL}/viewer/{proposal_id}"