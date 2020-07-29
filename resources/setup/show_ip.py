#!/usr/bin/python3

import time
import datetime
from PIL import Image, ImageFont, ImageDraw
from inky import InkyPHAT

import socket
import subprocess

# Get FreeMono Font
font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 15)

WHITE = 0
BLACK = 1
RED = 2
YELLOW = 2
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)

def init_screen(color):
    """Prepare the screen for drawing and return the draw variables
    """
    image = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT), color)
    # Set width and height of screen
    width, height = image.size
    # prepare for drawing
    draw = ImageDraw.Draw(image)
    return image, width, height, draw


# Print current date and time
print("Current date and time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Wait 20 seconds for the RPi Zero to connect to WiFi
time.sleep(20)

# Get SSID of connected network
ssidoutput = subprocess.check_output(["sudo", "iwgetid"], shell=False)

# Get local IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

image, width, height, draw = init_screen(color=WHITE)
draw.text(
    (10, 10), "Connected Wifi SSID: ", fill=BLACK, font=font,
)
draw.text(
    (35, 30), '• "' + ssidoutput.decode().split('"')[1] + '"', fill=RED, font=font,
)
draw.text(
    (10, 50), "Local IP of RPi Zero: ", fill=BLACK, font=font,
)
draw.text(
    (35, 70), "• " + s.getsockname()[0], fill=RED, font=font,
)

print("Connected Wifi SSID: " + ssidoutput.decode().split('"')[1])
print("Local IP of RPi Zero: " + s.getsockname()[0])

inky_display.set_image(image)
inky_display.show()

s.close()

