# Read Me


GUI for controlling Philip's Hue lights in conjunction with a Luxafor LED Flag for light notifications to family while working from home.

## Usage

### secret.json

1. Create "secret.json" in same directory
2. Store the endpoint for the Hue API  as "hue_url". Form is http://<Bridge IP>/api/<username>/lights/1/state"
3. Store Luxafor id as "lux_id"

### config.json

An example file is given with three colors and corresponding RGB codes. The names do not need to be the names of the colors, they are just used for button identification.

To add or remove colors, simply add or delete comma separated lines in the format `"<name>":[<r>,<g>,<b>]`

### requirements.txt

1. Run `pip install -r requirements.txt` from Command line on windows, or `pip3 install -r requirements.txt` on Unix

### Controlling lights

1. To turn on lights, run the program, click a button to change the lights to that color
2. To turn off the lights, click the last selected light or close the program
3. Press `F5` to reload from config and get updated colors.