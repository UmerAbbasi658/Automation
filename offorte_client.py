import json
from playwright.sync_api import sync_playwright
from config import EMAIL, PASSWORD, BASE_URL  # using credentials.py

class OfforteAutomation:
    def __init__(self, proposal_id, page_id):
        self.proposal_id = proposal_id
        self.page_id = page_id
        self.proposal_data = {}

    def login(self, page):
        if not EMAIL or not PASSWORD:
            raise ValueError("EMAIL or PASSWORD is not set in .env")
        page.goto(BASE_URL)
        page.fill("#user_email", EMAIL)
        page.fill("#user_pass", PASSWORD)
        page.click('button[data-test="login-btn-submit"]')
        page.wait_for_load_state("networkidle")

    def capture_api_response(self, page):
        def handle_response(response):
            if response.request.resource_type in ["xhr", "fetch"]:
                url = response.url
                if self.proposal_id in url:
                    try:
                        data = response.json()
                        if isinstance(data, dict) and len(data) > 0:
                            self.proposal_data = self._structure_data(data)
                    except Exception:
                        pass
        page.on("response", handle_response)

    def open_proposal(self, page):
        # Updated URL format for Offorte viewer
        viewer_url = f"{BASE_URL}/viewer/{self.proposal_id}"
        page.goto(viewer_url, wait_until="networkidle", timeout=60000)

    def _structure_data(self, data):
        return {
            "metadata": {
                "proposal_id": self.proposal_id,
                "name": data.get("details", {}).get("name"),
                "proposal_number": data.get("details", {}).get("proposal_nr"),
                "company": data.get("details", {}).get("account_company_name"),
                "status": data.get("details", {}).get("status"),
                "last_modified": data.get("details", {}).get("date_modified"),
            },
            "receivers": data.get("details", {}).get("receivers", []),
            "form_fields": data.get("formfields", []),
            "pages": data.get("document", {}).get("pages", [])
        }

    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            self.login(page)
            self.capture_api_response(page)
            try:
                self.open_proposal(page)
            except Exception as e:
                page.screenshot(path=f"error_{self.page_id}.png")
                raise e
            browser.close()
        if not self.proposal_data:
            raise Exception(f"Proposal data not captured for page {self.page_id}")
        return self.proposal_data