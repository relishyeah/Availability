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

#Information for Luxafor Webhook requests
header = {'Content-Type': 'application/json'}

# Color Format converter engine
converter = Converter(GamutC)

def load_colors():
    #Load colors as defined by user
    with open('config.json') as json_file:
        config = json.load(json_file)
    colors= [[col,config[col]] for col in config]
    return colors

def lux_body(hex):
    #Body for Luxafor Requests
    return '{"userId": "'+lux_id +'",  "actionFields":{    "color": "custom",\
    "custom_color": "' + hex + '"} }'

def con_to_hue(config):
    #converts config file to hue request format
    r,g,b = config
    hue = '{"on":true,'
    hue += '"xy":'+str(list((converter.rgb_to_xy(r,g,b))))+','
    hue +='"bri":127}'
    return hue

def rgb_to_hex(rgb):
    #Converts RGB to hex  format, not in rgb_xy
    return ("%02x%02x%02x" % (rgb[0],rgb[1],rgb[2]))

#Initialization of actions from config.json

def off():
    #Sets lights to off
    requests.put(hue_url,data = '{"on":false}')
    requests.post(lux_url,data=lux_body('000000'),headers = header)

def press(num):
    #sends requests when button is pressed, based off config
    buttons = all_children(root)

    rgb = colors[num][1]
    hue = con_to_hue(rgb)
    lux = lux_body(rgb_to_hex(rgb))

    requests.put(hue_url,data = hue)
    requests.post(lux_url,data=lux,headers = header)
    
    #Button Press behavior
    for i in range(len(buttons)):
        if i != num:
            buttons[i].config(relief=tk.RAISED)
        else:
            if buttons[i]["relief"] == "sunken":
                buttons[i].config(relief=tk.RAISED)
                off()
            else:   
                buttons[i].config(relief=tk.SUNKEN)


def all_children (window) :
    #Helper Function, shows all active buttons
    _list = window.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list

#Tkinter information
root = tk.Tk()
root.title("Availability")
helv = tkFont.Font(family='Helvetica', size=14)
root.resizable(False, False )

#Dynamic Button Creation
def init():
    global colors
    colors = load_colors()
    for i in range(len(colors)):

        invert = [255-j for j in colors[i][1]]

        bg = "#" + str(rgb_to_hex(colors[i][1]))
        fg = "#" + str(rgb_to_hex(invert))
        button = tk.Button(root, text=colors[i][0],bd=3,bg=bg,fg=fg,width=10,height=4,
            command = lambda j = i: press(j))
        button.pack(side=tk.LEFT,pady=3,padx=3)
        button['font'] = helv

def refresh(x):
    #Reload colors from config.json by pressing f5
    off()
    colors = []
    widget_list = all_children(root)
    for item in widget_list:
        item.destroy()
    init()

root.bind("<F5>", refresh)

init()
root.mainloop()
off()