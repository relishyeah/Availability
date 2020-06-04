import requests,time,tkinter as tk
from tkinter import font as tkFont 
import json
from rgbxy import Converter
from rgbxy import GamutC

#Imports sensitive information from secret.py file
with open('secret.json') as json_file:
    secret = json.load(json_file)
hue_url = secret["hue_url"]
lux_url = 'https://api.luxafor.com/webhook/v1/actions/solid_color'
lux_id = secret["lux_id"]

#Load colors as defined by user
with open('config.json') as json_file:
    config = json.load(json_file)
colors= [[col,config[col]] for col in config]

#Information for Luxafor Webhook requests
header = {'Content-Type': 'application/json'}

converter = Converter(GamutC)

def lux_body(hex):
    #Body for Luxafor Requests
    return '{"userId": "'+lux_id +'",  "actionFields":{    "color": "custom",\
    "custom_color": "' + hex + '"} }'

def rec_to_hue(rec):
    #converts config file to hue  request
    r,g,b = rec
    ret = '{"on":true,'
    ret += '"xy":'+str(list((converter.rgb_to_xy(r,g,b))))+','
    ret +='"bri":127}'
    return ret

#Initialization of actions from config.json

def off():
    #Sets lights to off
    requests.put(hue_url,data = '{"on":false}')
    requests.post(lux_url,data=lux_body('000000'),headers = header)

def rgb_to_hex(rgb):
    #same as above but not for tkinter button,for lux
    #NOTE: No hashmark
    return ("%02x%02x%02x" % (rgb[0],rgb[1],rgb[2]))

def press(num):
    #sends reqyuests when button is pressed
    rgb = colors[num][1]
    hue = rec_to_hue(rgb)
    lux = lux_body(rgb_to_hex(rgb))

    requests.put(hue_url,data = hue)
    requests.post(lux_url,data=lux,headers = header)

#Tkinter information
root = tk.Tk()
root.grid()
root.title("Availability")
helv = tkFont.Font(family='Helvetica', size=14)

root.resizable(False, False )

for i in range(len(colors)):

    invert = [255-j for j in colors[i][1]]

    bg = "#" + str(rgb_to_hex(colors[i][1]))
    fg = "#" + str(rgb_to_hex(invert))
    button = tk.Button(root, text=colors[i][0],bg=bg,fg=fg,width=10,height=4,
        command = lambda j = i: press(j))
    button.pack(side=tk.LEFT,pady=3,padx=3)
    button['font'] = helv

root.mainloop()
off()

