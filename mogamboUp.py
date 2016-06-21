 #!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot # Librería de la API del bot.
from telebot import types # Tipos para la API del bot.
import time # Librería para hacer que el programa que controla el bot no se acabe.
import sys
import random
import json
import urllib
import urllib2
from gtts import gTTS
from KickassAPI import Search, Latest, User, CATEGORY, ORDER
import kat
import re
import datetime
import pytz
import psycopg2
import commands
import unicodedata,re
#from datetime import datetime, date, time, timedelta
import hashlib
import shutil
from pymongo import MongoClient
import subprocess
import glob
import os
import shutil
import sys, time, threading, random, datetime, timeout, os.path
from random import randint



reload(sys) 
sys.setdefaultencoding("utf-8")

TOKEN = '180897565:AAHVHWZMvyL__y1Yb3TkXQzhsSwQHc7za88' # Nuestro tokken del bot (el que @BotFather nos dió).
global usuarios
usuarios = [line.rstrip('\n') for line in open('usuarios.txt')] # Cargamos la lista de usuarios.


# Antes de que sigas por aquí, los identificadores de un usuario son positivos
# Y los ID de los grupos, negativos
admin1 = -125332301
admin2 = 1541810
# He modificado el log y ahora sale primero el ID del usuario y luego el del grupo



bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.
global repeat
repeat = False
global cidPositive
cidPositive = False
global piropeados
piropeados=[]
global informer
informer = False
global flood
global ultimo_dia

global repeatDict
repeatDict = {}
global comandos
comandos = []
global descripciones
descripciones = []

# RHP >>>>
import time

global dedo_veloz_playing
dedo_veloz_playing=False

#############################################
#Listener
def listener(messages):
    for m in messages:
        cid = m.chat.id
        ucid = m.from_user.id
        
comandos.append("pingUp") 
descripciones.append("pongUp")
@bot.message_handler(commands=['pingUp'])
def command_status(m):
    cid=m.chat.id
    bot.send_message(cid,"pong")



@bot.message_handler(commands=['mogamboUp'])
def mogamboUp_command(m):
    cid = m.chat.id
    users = [6761180, 1541810, 3244610,  34390473,  957761, 5178944,  2497606]
    if m.from_user.id not in users:
        bot.send_message(cid,"Intruso")
        return
    proc = subprocess.Popen(['sudo','ps', '-ef'], stdout=subprocess.PIPE)
    subprocess.Popen.wait(proc)
    grep1 = subprocess.Popen(['grep', 'python2 /home/ubuntu/workspace/bot.py'], stdout=subprocess.PIPE, stdin=proc.stdout)
    grep2 = subprocess.Popen(['grep', '-v', '/bin/sh'], stdout=subprocess.PIPE, stdin=grep1.stdout)
    grep3 = subprocess.Popen(['grep', '-v', 'grep'], stdout=subprocess.PIPE, stdin=grep2.stdout)
    isBot=False
    for line in grep3.stdout.readlines():
        if "python2 /home/ubuntu/workspace/bot.py" in line:
            isBot=True
            print "[MU]Bot is running\n[MU]Stopping the bot"
            pid=line.split()[1]
            command="sudo kill -9 " + pid
            proc = subprocess.call(command, shell=True)
            print "[MU]Bot is stopped"
    proc = subprocess.Popen(['sudo','ps', '-ef'], stdout=subprocess.PIPE)
    subprocess.Popen.wait(proc)
    grep1 = subprocess.Popen(['grep', 'python bot.py'], stdout=subprocess.PIPE, stdin=proc.stdout)
    grep2 = subprocess.Popen(['grep', '-v', '/bin/sh'], stdout=subprocess.PIPE, stdin=grep1.stdout)
    grep3 = subprocess.Popen(['grep', '-v', 'grep'], stdout=subprocess.PIPE, stdin=grep2.stdout)
    isBot=False
    for line in grep3.stdout.readlines():
        #print "[MU]"
        #print line
        if "python bot.py" in line:
            isBot=True
            print "[MU]Bot runned by me is running"
            pid=line.split()[1]
            command="sudo kill -9 " + pid
            print "[MU]Stopping myself bot instance"
            proc = subprocess.call(command, shell=True)
            print "[MU]My bot instance is stopped"
            
    proc = subprocess.call("python bot.py", shell=True)
    time.sleep(5)
@bot.message_handler(commands=['mongoUp'])
def mongoUp_command(m):
    cid = m.chat.id
    users = [6761180, 1541810, 3244610,  34390473,  957761, 5178944,  2497606]
    if m.from_user.id not in users:
        bot.send_message(cid,"Intruso")
        return
    proc = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    subprocess.Popen.wait(proc)
    grep = subprocess.Popen(['grep', 'mongod'], stdout=subprocess.PIPE, stdin=proc.stdout)
    isMongo=False
    for line in grep.stdout.readlines():
        if "mongo" in line:
            isMongo=True
            print "Mongo is executed yet\nStopping Mongo"
            proc = subprocess.Popen(['pkill', 'mongod'], stdout=subprocess.PIPE)
            time.sleep(1)
            print "Mongo is stopped"
    print "Executing Mongo"
    mongo=subprocess.Popen(['mongod', '--smallfiles'], stdout=subprocess.PIPE)
    print "Mongo has been executed"



    #self.log(driver.page_source) #make log
    #driver.save_screenshot(self.directory_img + 'final_workspace.png')

#############################################
#Peticiones
bot.polling(none_stop=True) 