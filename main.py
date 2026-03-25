from dotenv import load_dotenv
import os
import requests
from offorte_client import OfforteAutomation
from google_service import get_pending_rows, mark_row_done
from credentials import get_proposal_url  # optional helper, not required

# Load environment variables
load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
WEBHOOK_URL = os.getenv("ZAPIER_WEBHOOK_URL")

def main():
    pending_rows = get_pending_rows(SPREADSHEET_ID, "Sheet1!A:B")
    if not pending_rows:
        print("✅ No pending rows found.")
        return

    for row in pending_rows:
        proposal_id = row["page_id"]  # used internally for API matching
        page_id = row["page_id"]      # used for constructing the Offorte URL
        row_number = row["row_number"]

        # Construct the Offorte URL dynamically using page_id
        page_url = f"https://gov-recruitment-marketing.offorte.com/viewer/{page_id}"
        print(f"🚀 Processing Proposal URL: {page_url}")

        try:
            # Initialize automation with proposal_id and page_id
            automation = OfforteAutomation(proposal_id, page_id)
            proposal_data = automation.run()

            # Send data to webhook
            response = requests.post(WEBHOOK_URL, json=proposal_data)
            if response.status_code in [200, 201]:
                print(f"✅ Sent Proposal {proposal_id} data to webhook")
                mark_row_done(SPREADSHEET_ID, row_number)
            else:
                print(f"❌ Failed to send Proposal {proposal_id}. Status: {response.status_code}")

        except Exception as e:
            print(f"❌ Failed for Proposal {proposal_id}: {str(e)}")

if __name__ == "__main__":
    main()