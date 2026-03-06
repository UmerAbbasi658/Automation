from dotenv import load_dotenv
load_dotenv()
import os
import requests
from offorte_client import OfforteAutomation
from google_service import get_pending_rows, mark_row_done

PROPOSAL_ID = "344878"
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
WEBHOOK_URL = os.getenv("ZAPIER_WEBHOOK_URL")

def main():
    pending_rows = get_pending_rows(SPREADSHEET_ID, "Sheet1!A:B")
    if not pending_rows:
        print("✅ No pending rows found.")
        return

    for row in pending_rows:
        page_id = row["page_id"]
        row_number = row["row_number"]

        print(f"🚀 Processing Page: {page_id}")

        try:
            automation = OfforteAutomation(PROPOSAL_ID, page_id)
            proposal_data = automation.run()

            response = requests.post(WEBHOOK_URL, json=proposal_data)
            if response.status_code in [200, 201]:
                print(f"✅ Sent Page {page_id} data to webhook")
                mark_row_done(SPREADSHEET_ID, row_number)
            else:
                print(f"❌ Failed to send Page {page_id}. Status: {response.status_code}")

        except Exception as e:
            print(f"❌ Failed for Page {page_id}: {str(e)}")

if __name__ == "__main__":
    main()