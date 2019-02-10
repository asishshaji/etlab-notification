import requests
from bs4 import BeautifulSoup
from fractions import Fraction
import os
import datetime
from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()

TWILIO_SID = "ACe76ab1a13cf70c1e9f24ba17908d14f2"
TWILIO_AUTHTOKEN = "c8906d09e1c0baab59a6c5dfc184e95a"

def main():
    url = 'https://nssce.etlab.in/user/login'
    payload = {'LoginForm[username]': 'CE160170', 'LoginForm[password]': '86b20a'}
    client = Client(TWILIO_SID, TWILIO_AUTHTOKEN)
    while True:
        sess = requests.session()
     
        post = sess.post(url=url, data=payload)

        attendance_url = 'https://nssce.etlab.in/ktuacademics/student/results?sem_id=239'

        _data = BeautifulSoup(sess.get(attendance_url).content, 'html.parser')
        _user_name = (_data.find('span',{'class':'text'}).getText().strip())
        
        atten_table = _data.find_all('table', {'class': 'items table table-striped table-bordered table-condensed'})
        message = []
        for tag in atten_table:
            tdTags = tag.find_all('tr')
            for tag in tdTags[1:-1]:
                try:
                    _sub = tag.find('td', {'nowrap': 'nowrap'}).getText().strip()
                    _perc = float(Fraction(tag.find('td', {'class': 'span1'}).getText().strip())) * 100

                
                    if _perc < float(80):
                        _message = '{}, your attedance for {} is {}'.format(_user_name,_sub, _perc)
                        message.append("\n"+_message)
                       
                    
                except Exception as e:
                    pass
   
        print(message)

        # 918129494749
   
        client_message =  client.messages.create(to="+918129494749",from_="+14844644015",body='\n'.join(message)+str(datetime.datetime.now()))
    
        if client_message.sid != None:
            print(client_message.sid)
            
            exit()


  
@sched.scheduled_job('interval', seconds=10)
def timed_job():
    main()

sched.start()

