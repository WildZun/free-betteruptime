import requests
import time
from urllib.parse import quote
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("UPTIME_APIKEY")
user = os.getenv("FREE_ID")
passwd = os.getenv("FREE_PASSWD")

# Monitor IDs
monitor_ids = ['766174', '839378', '766167', '766387', '951783']

# Initialize previous statuses
previous_statuses = {}

def send_sms(name, status):
    message = quote(f"Name: {name} Status: {status}")
    url = f"https://smsapi.free-mobile.fr/sendmsg?user={user}&pass={passwd}&msg={message}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to send SMS: {e}")

def check_and_notify():
    for monitor_id in monitor_ids:
        url = f'https://uptime.betterstack.com/api/v2/monitors/{monitor_id}'
        headers = {'Authorization': f'Bearer {api_key}'}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            status = data['data']['attributes']['status']
            name = data['data']['attributes']['pronounceable_name']

            if monitor_id in previous_statuses and previous_statuses[monitor_id] != status:
                send_sms(name, status)

            previous_statuses[monitor_id] = status
            print(f"Status: {status} - Name: {name}")

        except requests.RequestException as e:
            print(f"Failed to retrieve status: {e}")

if __name__ == "__main__":
    while True:
        check_and_notify()
        time.sleep(30)
