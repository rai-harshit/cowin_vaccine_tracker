import requests
import datetime
from fake_useragent import UserAgent
import json
import time
from twilio.rest import Client
import os

interval = 6

url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'
PARAMS = {
        'pincode': '421306', # Enter your pincode here
        'date': (datetime.date.today()+datetime.timedelta(days=1)).strftime('%d-%m-%Y') # Put days=0 if you wanna search for same day.
}

temp_useragent = UserAgent()
browser_header = {'User-Agent': temp_useragent.random}
contacts = ['+918452904404','+918828064902','+918356854510']

account_sid = '' # Paste Twilio Account SID here
auth_token = '' # Paste Twilio Auth Token here
client = Client(account_sid,auth_token)

while True:
    response = requests.get(url,PARAMS,headers=browser_header)
    if response.ok:
        resp_data = json.loads(response.text)['centers']
        if(len(resp_data)) > 0:
            date_available = True
            available_capacities=[]
            availability_details=[]
            for data in resp_data:
                available_capacities.append(data['sessions'][0]['available_capacity'])
                availability_details.append(data['name']+' : '+str(data['sessions'][0]['available_capacity'])+'\n')
            if max(available_capacities) > 0:
                message_body = ''.join(availability_details)
                print(message_body)
                for contact in contacts:
                    client.messages \
                            .create(
                                body=message_body,
                                from_='+14692948170',
                                to=contact
                            )
        else:
            date_available = False
        print('Last contact with COWIN server: '+str(datetime.datetime.now())+' | Server Response: '+str(response.status_code) +' | Date Available : '+str(date_available))
        time.sleep(interval)
    