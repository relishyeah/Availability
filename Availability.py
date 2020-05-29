import requests,time,tkinter as tk
from tkinter import font as tkFont 
import json

#Imports sensitive information from secret.py file
with open('secret.json') as json_file:
    data = json.load(json_file)
hue_url = data["hue_url"]
lux_url = 'https://api.luxafor.com/webhook/v1/actions/solid_color'
lux_id = data["lux_id"]

#Information for Luxafor Webhook requests
header = {'Content-Type': 'application/json'}
body ='{"userId": "'+lux_id +'" , "actionFields":{ "color": "'
off_body = '{"userId": "'+lux_id +'",  "actionFields":{    "color": "custom",\
    "custom_color": "000000"} }'

def off():
    #Sets lights to off
    requests.put(hue_url,data = '{"on":false}')
    requests.post(lux_url,data=off_body,headers = header)
    
def red():
    #Sets lights to red
    com = '{"on":true, "sat":254, "bri":50,"hue":0}'
    color = "red"
    requests.put(hue_url,data = com)
    requests.post(lux_url,data=body+color+'" } }',headers = header)

def green():
    #Sets lights to green
    com = '{"on":true, "sat":254, "bri":50,"hue":20000}'
    color = "green"
    requests.put(hue_url,data = com)
    requests.post(lux_url,data=body+color+'" } }',headers = header)

def yellow():
    #Sets lights to yellow
    com = '{"on":true, "sat":254, "bri":75,"hue":9999}'
    color = "yellow`"
    requests.put(hue_url,data = com)
    requests.post(lux_url,data=body+color+'" } }',headers = header)

def loop(i,s):
    #takes number of iterations, seconds between change
    #loops through colors
    for i in range(i):
        red()
        time.sleep(s)
        green()
        time.sleep(s)
        yellow()
        time.sleep(s)

#Tkinter information
root = tk.Tk()
root.geometry("540x200")
root.title("Availability")

helv22 = tkFont.Font(family='Helvetica', size=14)

root.resizable(False, False )

G = tk.Button(root, bg='green', width=15, command=green)
G.pack( padx=10,pady=37, side=tk.LEFT,fill=tk.Y)

Y = tk.Button(root, bg = 'yellow', width=15, command=yellow)
Y.pack(padx=10,pady=37, side=tk.LEFT,fill=tk.Y)

R = tk.Button(root, bg='red', width=15, command=red)
R.pack( padx=10,pady=37, side=tk.LEFT,fill=tk.BOTH)

o = tk.Button(root, bg = 'royalblue1',fg = 'black',text='Off', width=9, command=off)
o.pack(padx=10,pady=37, side=tk.LEFT,fill=tk.BOTH)

o['font'] = helv22

root.mainloop()
off()
