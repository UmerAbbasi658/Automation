import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Scopes for Google Sheets
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

def get_credentials():
    """
    Load service account credentials from environment variable
    """
    service_account_info = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT"))
    return service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    )

def get_sheets_service():
    """
    Return authorized Google Sheets service
    """
    creds = get_credentials()
    return build("sheets", "v4", credentials=creds)

def get_pending_rows(spreadsheet_id, range_name="Sheet1!A:B"):
    """
    Get rows where status is not 'Done'
    Returns a list of dictionaries with row_number and page_id
    """
    service = get_sheets_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()

    values = result.get("values", [])
    pending = []

    # Enumerate actual sheet rows starting from 1
    for i, row in enumerate(values, start=1):
        if i == 1:
            continue  # skip header
        page_id = row[0].strip() if len(row) > 0 else None
        status = row[1].strip().lower() if len(row) > 1 else ""
        if page_id and status != "done":
            pending.append({
                "row_number": i,  # actual sheet row number
                "page_id": page_id
            })
        else:
            print(f"Skipping row {i}, status is already '{status}'")

    return pending

def mark_row_done(spreadsheet_id, row_number):
    """
    Mark a specific row's status as 'Done'
    """
    service = get_sheets_service()
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"Sheet1!B{row_number}",
        valueInputOption="RAW",
        body={"values": [["Done"]]}
    ).execute()
    updated = result.get("updatedCells", 0)
    if updated > 0:
        print(f"✅ Row {row_number} marked as Done")
    else:
        print(f"⚠️ Row {row_number} could not be updated")