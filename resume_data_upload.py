import os
import requests
import json
from config import AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME

url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"

headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

def write_to_airtable(resume_info):
    """Uploads structured resume data to Airtable."""
    data = {
        "fields": {
            "email": resume_info.get("Email Address"),
            "state": resume_info.get("User's State"),
            "country": resume_info.get("User's Country"),
            "linkedin": resume_info.get("LinkedIn Link"),
            "education": resume_info.get("Education"),
            "experience": resume_info.get("Experience"),
            "skills": resume_info.get("Skills"),
            "certifications": resume_info.get("Certifications")
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Record successfully added to Airtable!")
    else:
        print(f"Failed to add record. Status Code: {response.status_code}")
        print(response.json())
