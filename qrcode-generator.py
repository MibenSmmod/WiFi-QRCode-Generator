#!/usr/bin/env python3
import getpass  ## import getpass is required if prompting for password
import qrcode
import os
from colored import fg
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

########################################################################################################################
## written by:       Mike Rieben
## e-mail:           mrieben@extremenetworks.com
## date:             May, 2025
## version:          1.0
## tested versions:  Python 3.13.2
########################################################################################################################
## This script ...  See README.md file for full description 
########################################################################################################################
## ACTION ITEMS / PREREQUISITES
## Please read the README.md file in the package to ensure you've completed the required and optional settings below
## Also as a reminder, do not forget to install required modules:  pip install -r requirements.txt
########################################################################################################################
## - ## two pound chars represents a note about that code block or a title
## - # one pound char represents a note regarding the line and may provide info about what it is or used for
########################################################################################################################

## ***** USER EDITS BELOW THIS LINE **********************************************************************

output_ssid_png = True # change to False if you want the SSID name to be included in the QR code
output_datetime_png = True # change to False if you want the date/time to be included in the QR code
encryption = "WPA" # "WPA" (for WPA, WPA2, or WPA3 Personal), "WEP" (for WEP), or "nopass" (for open networks)
hidden = "false" # must be "true" or "false" (case sensitive) within ""
output_file = "wifi_qr.png"
ssid = "" # if you wish to hard code the SSID name, enter it here otherwise leave as blank "" and you'll be prompted
# ssid = "MySSID"
wifi_psk = "" # if you wish to hard code the password, enter it here otherwise leave as blank "" and you'll be prompted
# wifi_psk = "QRCodeUserPass"


## ***** NO USER EDITS BELOW THIS LINE **********************************************************************

colorWhite = fg(255) ##DEFAULT Color: color pallete here: https://dslackw.gitlab.io/colored/tables/colors/
colorRed = fg(1) ##RED
colorGreen = fg(2) ##GREEN
colorPurple = fg(54) ##PURPLE
colorCyan = fg(6) ##CYAN
colorOrange = fg(94) ##ORANGE
colorGrey = fg(8)  ##GREY

while not ssid: # loop until ssid is provided
    ssid = input(f"\n{colorWhite}SSID Name (case sensitive): ")
    if not ssid:
        print(f"\n{colorOrange}SSID Name must not be blank.")

while len(wifi_psk) < 8: # loop until a password of at least 8 characters is provided
    wifi_psk = getpass.getpass(f"\n{colorWhite}Password (min 8 characters): ")
    if len(wifi_psk) < 8:
        print(f"\n{colorOrange}Password must be at least 8 characters long.")

def is_valid_ssid(ssid):
    return bool(ssid and ssid.strip())

def is_valid_password(password):
    return bool(password and len(password) >= 8)

ssid = ssid.strip()
while not is_valid_ssid(ssid):
    ssid = input(f"\n{colorWhite}SSID Name (case sensitive): ").strip()
    if not is_valid_ssid(ssid):
        print(f"\n{colorOrange}SSID Name must not be blank or spaces only.")

wifi_psk = wifi_psk.strip()
while not is_valid_password(wifi_psk):
    wifi_psk = getpass.getpass(f"\n{colorWhite}Password (min 8 characters): ").strip()
    if not is_valid_password(wifi_psk):
        print(f"\n{colorOrange}Password must be at least 8 characters long and not blank.")

print(f"\n{colorPurple}SSID: {ssid}, Password: \033[3mencrypted\033[0m")

wifi_string = f"WIFI:T:{encryption};S:{ssid};P:{wifi_psk};H:{hidden};;"

def save_qr(qr, filename):
    try:
        # Convert QR to PIL Image if not already
        if not isinstance(qr, Image.Image):
            qr = qr.get_image()
        # Calculate how much extra space is needed
        extra_height = 0
        if output_ssid_png:
            extra_height += 30
        if output_datetime_png:
            extra_height += 30
        if extra_height == 0:
            extra_height = 10  # minimal padding if no text
        width, height = qr.size
        new_height = height + extra_height
        new_img = Image.new("RGB", (width, new_height), "white")
        new_img.paste(qr, (0, 0))
        # Draw text
        draw = ImageDraw.Draw(new_img)
        font = ImageFont.load_default()
        y_offset = height + 10
        # SSID text
        if output_ssid_png:
            ssid_text = f"SSID: {ssid}"
            bbox_ssid = draw.textbbox((0, 0), ssid_text, font=font)
            ssid_width = bbox_ssid[2] - bbox_ssid[0]
            ssid_x = (width - ssid_width) // 2
            draw.text((ssid_x, y_offset), ssid_text, fill="black", font=font)
            y_offset += 20
        # Timestamp text
        if output_datetime_png:
            timestamp = datetime.now().strftime("Generated: %Y-%m-%d %H:%M:%S")
            bbox_time = draw.textbbox((0, 0), timestamp, font=font)
            time_width = bbox_time[2] - bbox_time[0]
            time_x = (width - time_width) // 2
            draw.text((time_x, y_offset), timestamp, fill="black", font=font)
            y_offset += 20
        # Save image
        new_img.save(filename)
        print(f"\n{colorGreen}{output_file} -> File Created Successfully. Check current directory.\n")
    except Exception as e:
        print(f"{colorRed}**** Something went wrong, no QR Code generated****")
        print(f"{colorRed}Error: {e}")

if os.path.exists(output_file):
    overwrite = ""
    while overwrite not in ("yes", "no", "y", "n"):
        overwrite = input(f"\n{colorWhite}{output_file} already exists. Overwrite? (Yes/No): ").strip().lower()
        if overwrite in ("y", "yes"):
            overwrite = "yes"
        elif overwrite in ("n", "no"):
            overwrite = "no"
        else:
            print(f"\n{colorOrange}Please enter 'Yes' or 'No'.")
    if overwrite == "yes":
        qr = qrcode.make(wifi_string)
        save_qr(qr, output_file)
    else:
        print(f"\n{colorRed}***QR Code creation was skipped, file was not overwritten****\n")
else:
    qr = qrcode.make(wifi_string)
    save_qr(qr, output_file)

### End of script