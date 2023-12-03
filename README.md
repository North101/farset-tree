# Farset Tree

### Hardware
Microcontroller: [Plasma Stick 2040 W](https://shop.pimoroni.com/products/plasma-stick-2040-w?variant=40359072301139)

Lights: [5m Flexible Addressable RGB LED Wire](https://shop.pimoroni.com/products/5m-flexible-rgb-led-wire-50-rgb-leds-aka-neopixel-ws2812-sk6812?variant=40384556171347)

### About

This project is designed to allow FarsetLabs members to upload their own Christmas tree lights code to the FarsetLabs Christmas tree.

This repo contains the bootstrap code to get things up and running. If it fails to connect to wifi, it will open an access point to configure wifi details. After it successfully connects, it will attempt to sync the latest code for the configured github account, run `/lights.py` and then open a webserver to allow changing which github repo to sync to.

### Uploading Code

You'll need to navigate to the Plasma Stick 2040 W's ip address. Here you can enter your github details. When you click save, it will automatically reboot and attempt to sync the repo. Any other files that were on the device (except for those listed below) will be removed.

Your main file should be named `lights.py` in the root of the project. Bellow you can find some examples of code to control the LEDs.

Files or directories with the following names will be ignored:
- Any file or directory beginning with `.`
- `/lib/phew/`
- `/farset_tree/`
- `/main.py`

Try not to include unnecessary files as they will be synced and theres only so much space.

### Examples

https://github.com/North101/farset-tree-lights/blob/main/lights.py

https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/examples/plasma_stick
