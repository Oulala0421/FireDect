from machine import Pin, I2C, PWM
from dotenv import load_dotenv
import time , sta
import dht
import os

load_dotenv()

P4=Pin(4, Pin.IN)
d=dht.DHT11(P4)        #建立 DHT11 物件

W_token = os.getenv('WIFI')
sta.connAP('TT-Maker', 'W_token')

L_token = os.getenv('VARIABLE_L_NAME')
K_token= os.getenv('thingkey')
URL1 = 'https://api.thingspeak.com/update?api_key=K_toke&field1='
URL2 = 'https://api.thingspeak.com/update?api_key=K_toke&field2='
URLdanger='https://maker.ifttt.com/trigger/danger/with/key/'+L_token
URLnormal='https://maker.ifttt.com/trigger/normal/with/key/'+L_token
URLnotice='https://maker.ifttt.com/trigger/notice/with/key/'+L_token
while True:

    d.measure()                  #重新測量溫溼度
    t=d.temperature()          #讀取攝氏溫度
    h=d.humidity()             #讀取相對溼度
    mydata1=str(t)
    mydata2=str(h)
    sta.sendURL(URL1+mydata1+'&field2='+mydata2)
    he=(1-0.5)*(h+0.5*70)   #實效濕度
    print('溫度'+mydata1,'濕度'+mydata2)
    print('實效濕度'+he)
    if t>35 :
      
      if h > 60:
        sta.sendURL(URLnormal+'?value1='+str(t)+'&value2='+str(h) +'&value3='+str(he))
      else :
        if he < 35:
          sta.sendURL(URLdanger+'?value1='+str(t)+'&value2='+str(h) +'&value3='+str(he))
        else :
          sta.sendURL(URLnotice+'?value1='+str(t)+'&value2='+str(h) +'&value3='+str(he))
    elif 25<t<=35 :
      if h >50:
        sta.sendURL(URLnormal+'?value1='+str(t)+'&value2='+str(h) +'&value3='+str(he))
      else :
        sta.sendURL(URLdanger+'?value1='+str(t)+'&value2='+str(h) +'&value3='+str(he))
    else :
      if h >40:
        sta.sendURL(URLnormal+'?value1='+str(t)+'&value2='+str(h) +'&value3='+str(he))
      else :
        sta.sendURL(URLnotice+'?value1='+str(t)+'&value2='+str(h) +'&value3='+str(he))
    time.sleep(30)                  #暫停 30 秒 為方便觀看使用秒為單位

