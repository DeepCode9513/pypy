import json
from urllib import response
import requests
import pprint
import time
import pandas as pd


client_id = "40fe18c9-2344-4a43-a76b-bceae2856fd8"
client_secret = "4t632z6vh6vytgrb55ym3wffjmatuktki7fzknob5qib2z2ldxem"
datacenter_url = "https://eu-cloud.acronis.com"
base_url = f"{datacenter_url}/api/2"

from base64 import b64decode, b64encode

encoded_client_creds = b64encode(f"{client_id}:{client_secret}".encode("ascii"))
basic_auth = {"Authorization": "Basic " + encoded_client_creds.decode("ascii")}

response = requests.post(
    f"{base_url}/idp/token",
    headers={"Content-Type": "application/x-www-form-urlencoded", **basic_auth},
    data={"grant_type": "client_credentials"},
)

token_info = response.json()
auth = {"Authorization": "Bearer " + token_info["access_token"]}

response = requests.get(f"{base_url}/clients/{client_id}", headers=auth)
tenant_id = response.json()["tenant_id"]


report_data = {
    "parameters": {
        "kind": "usage_summary",
        "tenant_id": tenant_id,
        "level": "accounts",
        "period": {"start": "2022-09-01", "end": "2022-09-30"},
        "formats": ["json_v2_0"],
    },
    "schedule": {"type": "once"},
    "generation_date": "2022-10-01",
    "result_action": "save",
}


response = requests.post(
    f"{base_url}/reports",
    headers={"Content-type": "application/json", **auth},
    data=json.dumps(report_data),
)

if response.ok:
    report_status = "non saved"
    report_id = response.json()["id"]
    stored_report_id = None

    while report_status != "saved":
        response = requests.get(f"{base_url}/reports/{report_id}/stored", headers=auth)

        if response.ok:
            report_status = response.json()["items"][0]["status"]
        else:
            pprint.pprint(response.json())

        time.sleep(2)

    stored_report_id = response.json()["items"][0]["id"]

    response = requests.get(
        f"{base_url}/reports/{report_id}/stored/{stored_report_id}", headers=auth
    )

    if response.ok:
        # pprint.pprint(response.json())
        js = response.json()
        df = pd.json_normalize(js, record_path=["tenants"])
        for col in df.columns:
            print(col)

