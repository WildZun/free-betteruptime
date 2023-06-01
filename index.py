import requests
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("UPTIME_APIKEY")

#Set your monitor id here
monitor_ids = ['766174', '839378', '766167', '766387', '951783']

previous_statuses = {}

def send_sms(name, status):
    user = os.getenv("FREE_ID")
    passwd = os.getenv("FREE_PASSWD")
    message = f"Name: {name} Status: {status}"
    message = message.replace(" ", "%20")
    urlfree = f"https://smsapi.free-mobile.fr/sendmsg?user={user}&pass={passwd}&msg={message}"
    response = requests.get(urlfree)

while True:
    for monitor_id in monitor_ids:
        url = f'https://uptime.betterstack.com/api/v2/monitors/{monitor_id}'
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            status = data['data']['attributes']['status']
            name = data['data']['attributes']['pronounceable_name']
            if monitor_id in previous_statuses and previous_statuses[monitor_id] != status:
                send_sms(name, status)
            previous_statuses[monitor_id] = status
            print(f"Status: {status}")
            print(f"Name: {name}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    time.sleep(30)