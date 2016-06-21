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
from threading import Timer
import Image
import ImageDraw
from PIL import Image as ImagePIL
import numpy as np
from images2gif import writeGif





reload(sys) 
sys.setdefaultencoding("utf-8")

TOKEN = '190597061:AAGVYMme_ok6By3jZkEaFzj6_8ypc2zn4-8' # Nuestro tokken del bot (el que @BotFather nos dió).
global usuarios
#usuarios = [line.rstrip('\n') for line in open('usuarios.txt')] # Cargamos la lista de usuarios.
usuarios=[]
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
global fin
fin=0

global dedo_veloz_playing
dedo_veloz_playing=False

global dedo_veloz_ended
dedo_veloz_ended=True

global dedovelozmundia_playing
dedovelozmundial_playing=False

global ganador
ganador="None"
global ganadorTime
ganadorTime=datetime.datetime.now()

global segundo
segundo="None"
global segundoTime
segundoTime=datetime.datetime.now()

global mensaje_id
mensaje_id=""

global jugadores
jugadores={}

global fichas4
fichas4 = 4
global tamanyo4
tamanyo4 = 25
global margen4
margen4 = 5
# Filas y columnas
global filas4
filas4 = 6
global columnas4
columnas4 = 7
# Tablero
global tablero4
tablero4 = [[None]*columnas4 for _ in range(filas4)]
# Control de Juego
global jugando4
jugando4 = False
# Turno
turno4 = "Rojo"
# Equipos
global equipo_rojo4
equipo_rojo4 = []

global equipo_amarillo4
equipo_amarillo4 = []

global mensaje_id_conectame4
mensaje_id_conectame4=""

global giffing
giffing=False

global imagesToGIF
imageToGIF=[]

def check_self_runnings():
    print "Checking current running"
    proc = subprocess.Popen(['ps', '-efo', 'etime,pid,args'], stdout=subprocess.PIPE)
    #subprocess.Popen.wait(proc)
    grep1 = subprocess.Popen(['grep', 'python bot.py'], stdout=subprocess.PIPE, stdin=proc.stdout)
    grep2 = subprocess.Popen(['grep', '-v', '/bin/sh'], stdout=subprocess.PIPE, stdin=grep1.stdout)
    grep3 = subprocess.Popen(['grep', '-v', 'grep'], stdout=subprocess.PIPE, stdin=grep2.stdout)
    isBot=False
    for line in grep3.stdout.readlines():
        #print line
        if "python bot.py" in line:
            isBot=True
            print "Bot is running"
            pid=line.split()[1]
            #proc2 = subprocess.Popen(['sudo','ps', '-efo', 'pid,etime'], stdout=subprocess.PIPE)
            #print proc2.stdout.readlines()[1]
            #print pid
            #pidaux="'" + pid + "'"
            #print pidaux
            command = "grep "+ str(pid)
            #grep4 = subprocess.Popen(['grep', str(pidaux)], stdout=subprocess.PIPE, stdin=proc2.stdout)
            command="sudo kill -9 " + pid
            time = line.split()[0]
            if str(time)=="00:00" or str(time)=="00:01" or str(time)=="00:02" or str(time)=="00:03":
                print "The other bot its me!"
            else:
                print "Stopping the bot"
                proc = subprocess.call(command, shell=True)
                print "Bot is stopped"




def execute_mongo():
    proc = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    subprocess.Popen.wait(proc)
    grep = subprocess.Popen(['grep', 'mongod'], stdout=subprocess.PIPE, stdin=proc.stdout)
    isMongo=False
    for line in grep.stdout.readlines():
        if "mongo" in line:
            isMongo=True    
    if isMongo==False:
        print "Executing Mongo"
        mongo=subprocess.Popen(['sudo','mongod', '--smallfiles'], stdout=subprocess.PIPE)
        print "Mongo has been executed"
    else:
        print "Mongo is executed yet"

def load_users():
    client = MongoClient()
    db = client.bot
    print "Loading users"
    user=""
    for user in db.users.find({}):
        global usuarios
        usuarios.append(user.get("_id"))
    print "Users loaded"
        

def check_date():
    client = MongoClient()
    db = client.bot
    print "Loading date"
    if db.dia.count()==0:
        dia = datetime.datetime.now(pytz.timezone('Europe/Madrid')).day
        lastDay={"lastDay" : dia}
        db.dia.insert(lastDay)
    print "Date loaded"
    
    poleObjetivo=db.dia.find({})
    document=""
    for document in poleObjetivo:
        i=0
    ultimo_dia= document.get("lastDay")
        
def clean_tmp():
    proc = subprocess.Popen(['ls', '-lah', '/tmp'], stdout=subprocess.PIPE)
    subprocess.Popen.wait(proc)
    grep = subprocess.Popen(['grep', 'tmp'], stdout=subprocess.PIPE, stdin=proc.stdout)
    tmp=False
    for line in grep.stdout.readlines():
        if "tmp" in line:
            tmp=True    
    if tmp==True:
        path=glob.glob("/tmp/tmp"+"*")
        for fl in path:
            shutil.rmtree(fl, ignore_errors=True)
        print "/tmp has been cleaned"
        
def someone_pole():
    ahora=datetime.datetime.now(pytz.timezone('Europe/Madrid'))
    fecha=datetime.date(ahora.year,ahora.month, ahora.day)
    client = MongoClient()
    db = client.bot
    last={"lastPole": str(fecha)}
    if db.poles.count(last) == 0:
        return False
    else:
        return True

def dedo_veloz_mundial(cid):
    global dedo_veloz_playing
    if dedo_veloz_playing==True:
        bot.send_message(cid,"Ya hay una partida en marcha")
        return
    else:
        dedo_veloz_playing=True
    global dedo_veloz_ended
    dedo_veloz_ended=False
    global jugadores
    jugadores.clear()
    global ganador
    global segundo
    ganador="None"
    segundo="None"
    mensaje = bot.send_message(cid, "El primero que pulse 'Go', gana :)")
    time.sleep(2)
    
    bot.edit_message_text("Preparados...", cid, mensaje.message_id)
    numero = random.randrange(1,4)
    time.sleep(numero)
    
    #bot.send_message(cid, "Listos......")
    bot.edit_message_text("Listos.....", cid, mensaje.message_id)
    numero = random.randrange(1,4)
    time.sleep(numero)

    
    markup = types.ReplyKeyboardMarkup()
    palabras = ["Na","No","Ga","Ge","So","Puta"]
    numero = random.randrange(1,6)
    itembtn1 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn2 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn3 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn4 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn5 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn6 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn7 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn8 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn9 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    
    numero = random.randrange(1,9)
    if numero == 1:
        itembtn1 = types.KeyboardButton('Go')
    elif numero == 2:
        itembtn2 = types.KeyboardButton('Go')
    elif numero == 3:
        itembtn3 = types.KeyboardButton('Go')
    elif numero == 4:
        itembtn4 = types.KeyboardButton('Go')
    elif numero == 5:
        itembtn5 = types.KeyboardButton('Go')
    elif numero == 6:
        itembtn6 = types.KeyboardButton('Go')
    elif numero == 7:
        itembtn7 = types.KeyboardButton('Go')
    elif numero == 8:
        itembtn8 = types.KeyboardButton('Go')
    elif numero == 9:
        itembtn9 = types.KeyboardButton('Go')
                            
    markup.row(itembtn1,itembtn2,itembtn3)
    markup.row(itembtn4,itembtn5,itembtn6)
    markup.row(itembtn7,itembtn8,itembtn9)
    global mensaje_id
    #bot.edit_message_text("YA!", cid, mensaje.message_id)
    mensaje=bot.send_message(cid, 'YA!', reply_markup=markup)
    mensaje_id=mensaje.message_id
    
    # Juego

    while(dedo_veloz_playing==True):
        i=1
    #print "a"
    markup = types.ReplyKeyboardHide()
    #print "b"
    dedo_veloz_ended=True
    #print "c"
    global ganador
    bot.send_message(cid, "Y el ganador es: " + ganador, reply_markup=markup)
    mensaje_id=0
    if jugadores[ganador]==1:
        puntos = 3
        print "3"
    else:
        puntos = 1
        print "1"
    client = MongoClient()
    db = client.bot
    dedo_ganador = {"username" :ganador}
    if db.dedovelozmundial.count(dedo_ganador)==0:
        dedo_ganador["totalVictorias"]=puntos
    else:
        dedoObjetivo=db.dedovelozmundial.find({"username":ganador})
        document=""
        for document in dedoObjetivo:
            i=0
                #print(document)
        totalVictorias= document.get("totalVictorias")
        dedo_ganador["totalVictorias"]=totalVictorias+puntos
        db.dedovelozmundial.remove(document)
        
    dedoAdmin=db.dedovelozmundial.find_one({"username": "dedoAdmin"})
    totalPartidas=dedoAdmin.get("totalPartidas")
    totalPartidas=totalPartidas+1
    dedoAdminAux={"username":"dedoAdmin", "totalPartidas":totalPartidas}
    db.dedovelozmundial.remove(dedoAdmin)
    db.dedovelozmundial.insert(dedoAdminAux)
    db.dedovelozmundial.insert(dedo_ganador)

#Función hecha por lmontesn
def download_file(cid, url, destination):
  response = urllib.urlopen(url)
  data = response.read()
  file=open(destination,'w')
  file.write(data)
  file.close()
  digest = hashlib.sha256(data).hexdigest()  
  if(digest == "4cf454486035ac3786caac3a3d23fff9c5dfa8563299d9a7e73ae474e76810d2"):
    #bot.send_message(cid, "Tio eres el amo")
    bot.send_sticker(cid, open('donotwant2.webp', 'rb'))


def mostrar_teclado4(cid):
    
    global turno4, mensaje_id_conectame4
    
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton("1")
    itembtn2 = types.KeyboardButton("2")
    itembtn3 = types.KeyboardButton("3")
    itembtn4 = types.KeyboardButton("4")
    itembtn5 = types.KeyboardButton("5")
    itembtn6 = types.KeyboardButton("6")
    itembtn7 = types.KeyboardButton("7")
    markup.row(itembtn1,itembtn2,itembtn3,itembtn4,itembtn5,itembtn6,itembtn7)
    mensaje=bot.send_message(cid, "Te toca: " + turno4, reply_markup=markup)
    mensaje_id_conectame4=mensaje.message_id

# CONECTAME 4
def comprobar_tablero4():
    
    global fichas4, tablero4, filas4, columnas4
    
    ### Revisamos
    for i in range(filas4):
        for j in range(columnas4):
            if tablero4[i][j] != None:
                # Tipo de ficha
                ficha = tablero4[i][j]
                ## Horizontales
                # Izquierda
                if j - (fichas4 - 1) >= 0:
                    contador = 0
                    for k in range(fichas4):
                        if tablero4[i][j - k] == ficha:
                            contador+=1
                    if contador == fichas4:
                        return ficha
                # Derecha
                if j + (fichas4 - 1) < columnas4:
                    contador = 0
                    for k in range(fichas4):
                        if tablero4[i][j + k] == ficha:
                            contador+=1
                    if contador == fichas4:
                        return ficha
                ## Verticales
                # Arriba
                if i - (fichas4 - 1) >= 0:
                    contador = 0
                    for k in range(fichas4):
                        if tablero4[i - k][j] == ficha:
                            contador+=1
                    if contador == fichas4:
                        return ficha
                # Abajo
                if i + (fichas4 - 1) < filas4:
                    contador = 0
                    for k in range(fichas4):
                        if tablero4[i + k][j] == ficha:
                            contador+=1
                    if contador == fichas4:
                        return ficha
                ## Diagonales
                # Arriba-Izquierda
                if  i - (fichas4 - 1) >= 0 and j - (fichas4 - 1) >= 0:
                    contador = 0
                    for k in range(fichas4):
                        if tablero4[i - k][j - k] == ficha:
                            contador+=1
                    if contador == fichas4:
                        return ficha
                # Arriba-Derecha
                if  i - (fichas4 - 1) >= 0 and j + (fichas4 - 1) < columnas4:
                    contador = 0
                    for k in range(fichas4):
                        if tablero4[i - k][j + k] == ficha:
                            contador+=1
                    if contador == fichas4:
                        return ficha
                # Abajo-Izquierda
                if i + (fichas4 - 1) < filas4 and j - (fichas4 - 1) >= 0:
                    contador = 0
                    for k in range(fichas4):
                        if tablero4[i + k][j - k] == ficha:
                            contador+=1
                    if contador == fichas4:
                        return ficha
                # Abajo-Derecha
                if i + (fichas4 - 1) < filas4 and j + (fichas4 - 1) < columnas4:
                    contador = 0
                    for k in range(fichas4):
                        if tablero4[i + k][j + k] == ficha:
                            contador+=1
                    if contador == fichas4:
                        return ficha
                
    ### No hemos encontrado ganador
    return None
    
def actualizar_tablero4(pos):
    
    global tablero4, turno4
    
    # Buscamos la posición donde añadir la ficha
    for i in range(filas4):
        if tablero4[i][pos - 1] == None:
            tablero4[i][pos - 1] = turno4
            return True
    
    # Si no hay hueco, avisamos para repetir
    return False

def pinta_tablero4(cid):
    
    global tablero4, filas4, columnas4, tamanyo4, margen4
    
    # Rotamos el tablero
    tablero_rotate = tablero4[::-1]

    # Imagen azul de fondo
    width = ( tamanyo4 + margen4 ) * columnas4 + margen4 
    height = ( tamanyo4 + margen4 ) * filas4 + margen4
    img = Image.new('RGB',(width, height),"blue") 

    # Pintamos las fichas
    for i in range(filas4):
        for j in range(columnas4):
            draw = ImageDraw.Draw(img)
            position = (margen4 + margen4 * j + tamanyo4 * j,            # x0
                        margen4 + margen4 * i + tamanyo4 * i,            # y0
                        margen4 + margen4 * j + tamanyo4 * j + tamanyo4, # x1
                        margen4 + margen4 * i + tamanyo4 * i + tamanyo4) # y1
                        
            if tablero_rotate[i][j] == 'Rojo':
                draw.ellipse(position, fill="red")
            elif tablero_rotate[i][j] == 'Amarillo':
                draw.ellipse(position, fill="yellow")
            else:
                draw.ellipse(position, fill="white")
            del draw

    # Guardamos la imagen
    img.save('img/conectame4.jpg')
    bot.send_photo( cid, open( 'img/conectame4.jpg', 'rb'))
    

def listener4(m):
    cid = m.chat.id
    global mensaje_id_conectame4, turno4, equipo_rojo4, equipo_amarillo4, jugando4
    if m.reply_to_message==None:
        return
    if m.reply_to_message.message_id!=mensaje_id_conectame4:
        return
    
    # Comprobamos que sea una posición
    if m.text!="1" and m.text!="2"  and m.text!="3" and m.text!="4" and m.text!="5" and m.text!="6":
        return
    
    # Comprobamos equipo
    if turno4 == "Rojo":
        if m.from_user.username not in equipo_rojo4:
            bot.send_message( cid, "No es turno, capullo.")
            return
    elif turno4 == "Amarillo":
        if m.from_user.username not in equipo_amarillo4:
            bot.send_message( cid, "No es turno, capullo.")
            return
        
    if not actualizar_tablero4(int(m.text)):
        bot.send_message( cid, "No puedes ponerla ahí, capullo.")
        return
    
    pinta_tablero4(cid)
    
    ganador = comprobar_tablero4()
    if ganador == None:
        # Cambiamos turno
        if turno4 == "Rojo":
            turno4 = "Amarillo"
        elif turno4 == "Amarillo":
            turno4 = "Rojo"
    else:
        markup = types.ReplyKeyboardHide()
        bot.send_message( cid, "El ganador es el equipo: " + ganador, reply_markup=markup)
        jugando4 = False
    
#############################################
#Listener
def listener(messages):
    for m in messages:
        cid = m.chat.id
        ucid = m.from_user.id
        global usuarios
        global giffing
        if (m.from_user.id not in usuarios):
            usuarios.append(m.from_user.id)
            client = MongoClient()
            db = client.bot
            user = {"_id" : m.from_user.id}
            user["username"] = m.from_user.username
            db.users.insert(user)
            print db.users.count(user)
        if m.content_type == 'text': # Sólo saldrá en el log los mensajes tipo texto
            global dedo_veloz_playing
            global dedo_veloz_ended
            global jugando4
            if jugando4==True:
                listener4(m)
            #print str(dedo_veloz_playing)
            if dedo_veloz_ended==False:
            #print "Playing"
                if m.reply_to_message!=None:
                    global mensaje_id
                    if m.reply_to_message.message_id==mensaje_id:
                        global jugadores
                        if jugadores.has_key(m.from_user.username)==True:
                            jugadores[m.from_user.username]=jugadores[m.from_user.username]+1
                        else:
                            jugadores[m.from_user.username]=1
                        if m.text=="Go":
                            global ganador
                            global ganadorTime
                            global segundo
                            global segundoTime
                            if ganador=="None":
                                ganador=m.from_user.username
                                ganadorTime=datetime.datetime.now(pytz.timezone('Europe/Madrid'))
                                dedo_veloz_playing=False
                            elif segundo=="None":
                                segundo=m.from_user.username
                                segundoTime=datetime.datetime.now(pytz.timezone('Europe/Madrid'))
            else:
                dia = datetime.datetime.now(pytz.timezone('Europe/Madrid'))
                if cid > 0:
                    cidPositive = True
                    mensaje = str(m.chat.first_name) + " [" + str(ucid) + "] " + "(" + dia.strftime('%Y/%m/%d %H:%M:%S') + "): "+ m.text
                else:
                    cidPositive = False
                    mensaje = str(m.from_user.first_name) + " [" + str(ucid) + "] " + str(m.chat.title) + " [" + str(cid) + "] " + "(" + dia.strftime('%Y/%m/%d %H:%M:%S') + "): " + m.text 
                if m.text[0]=="/":
                    f = open('log.txt', 'a')
                    f.write(mensaje + "\n")
                    f.close()
            #in_usuarios(m)

                print mensaje

        elif m.content_type == 'sticker':
            file_info = bot.get_file(m.sticker.file_id)
            download_file(cid, 'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path), "sticker.webp")
            #print(file_info)
        elif( m.content_type=='photo' and giffing==True):
            global imagesToGIF
            file_info = bot.get_file(m.photo[0].file_id)

            download_file(cid,'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path),"image1.jpg")
            imagesToGIF.append(ImagePIL.open("image1.jpg"))
            print "Image added"


bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.


def in_usuarios(m):
    cid = m.chat.id
    if cid>0:
        if not str(cid) in usuarios and not (str(m.chat.first_name) + " - " + str(m.chat.username) + " - " + str(cid)) in usuarios:
            aux=open('usuarios.txt', 'a')
            usuarios.append(cid)
            userName=str(m.chat.first_name)
            userQuote=str(m.chat.username)
            aux.write(userName + " - " + userQuote + " - " + str(cid) + "\n")
            aux.close()
            return True
    else:
        if not str(cid) in usuarios and not (str(m.chat.title) + " - " + "None" + " - " + str(cid)) in usuarios:
            aux=open('usuarios.txt', 'a')
            usuarios.append(cid)
            userName=str(m.chat.title)
            userQuote="None"
            aux.write(userName + " - " + userQuote + " - " + str(cid) + "\n")
            aux.close()
        if not str(cid) in usuarios and not (str(m.from_user.first_name) + " - " + str(m.from_user.username) + " - " + str(m.from_user.id)) in usuarios:
            aux=open('usuarios.txt', 'a')
            usuarios.append(cid)            
            userName=str(m.from_user.first_name)
            userQuote=str(m.from_user.username)
            aux.write(userName + " - " + userQuote + " - " + str(m.from_user.id) + "\n")
            aux.close()
        return False
            
    return False
#############################################
#Funciones
#@bot.message_handler(commands=['roto2']) # Indicamos que lo siguiente va a controlar el comando '/roto2'.
#def command_roto2(m): # Definimos una función que resuelva lo que necesitemos.
#    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
#    bot.send_photo( cid, open( 'roto2.png', 'rb')) # Con la función 'send_photo()' del bot, enviamos al ID de la conversación que hemos almacenado previamente la foto de nuestro querido :roto2:
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if not str(cid) in usuarios: # Con esta sentencia, hacemos que solo se ejecute lo de abajo cuando un usuario hace uso del bot por primera vez.
        usuarios.append(str(cid)) # En caso de no estar en la lista de usuarios, lo añadimos.
        aux = open( 'usuarios.txt', 'a') # Y lo insertamos en el fichero 'usuarios.txt'
        if cid > 0:
            userName=str(m.chat.first_name)
        else:
            userName=str(m.chat.title)
        aux.write(userName + " - " + str(cid) + "\n")
        aux.close()
        bot.send_message( cid, "Encantado, compañeros")
    client = MongoClient()
    db = client.bot
    db.ban.remove({})

comandos.append("ping") 
descripciones.append("pong")
@bot.message_handler(commands=['ping'])
def command_status(m):
    cid=m.chat.id
    bot.send_message(cid,"pong")

comandos.append("pong")
descripciones.append("ping")
@bot.message_handler(commands=['pong'])
def cpong(m):
    cid=m.chat.id
    bot.send_message(cid,"ping")
    
#comandos.append("enviar")    
@bot.message_handler(commands=['enviar'])
def command_enviar(m):
    if " " in m.text:
            token = m.text.split(" ", 1)[1]
            bot.send_message(-1159490, token)

comandos.append("cuallado")
descripciones.append("Devuelve una famosa coletilla")
@bot.message_handler(commands=['cuallado']) # Indicamos que lo siguiente va a controlar el comando '/miramacho'
def command_miramacho(m): # Definimos una función que resuleva lo que necesitemos.
    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
    numero = random.randrange(1,4) 
    frases ={1:"sa rallao", 
    2:"cabrón",
    3:"Fucking master of universe"
    }
    mensaje = frases[numero]
    bot.send_message( cid, mensaje, reply_to_message_id=m.message_id) # Con la función 'send_message()' del bot, enviamos al ID almacenado el texto que queremos.

comandos.append("voice")
descripciones.append("Manda en nota de audio el texto")
@bot.message_handler(commands=['voice'])#voice
def command_voice(m):
    cid = m.chat.id 
    #if m.from_user.id == 1541810:
    #    token = " Cuallado, te estas rayando"
    #elif m.from_user.id == 5178944:
    #    token = "Jaime, me estas rayando la cabeza"
    if len(m.text)>6:
        if " " in m.text:
            token = m.text.split(" ", 1)[1]
        else:
            token = "No mandes audios vacíos"
    else:
        token = " No mandes audios vacíos"
    #if m.from_user.id == 5178944:
    #    token = " Jaime, me estas rayando la cabeza"
    
    #tts = gTTS(text=token, lang='es')
    #tts.save("tts.mp3")
    #audio = open('tts.mp3', 'rb')
    #bot.send_voice(cid, audio)

#comandos.append("voiceto")    
@bot.message_handler(commands=['voiceto'])
def command_voiceto(m):
    cid = m.chat.id 
    if len(m.text.split(" "))<3:
        token = "No mandes audios vacíos, o sin destino"
        to = cid
    else:
        token = m.text.split(" ",1)[1]
        to = m.text.split(" ")[-1]
        token = token.replace(to,"")
    tts = gTTS(text=token, lang='es')
    tts.save("tts.mp3")
    audio = open('tts.mp3', 'rb')
    bot.send_voice(to, audio)    
    
comandos.append("torrent")    
descripciones.append("Realiza una búsqueda en KickAss.to")
@bot.message_handler(commands=['torrent'])
def command_torrent(m):
    cid = m.chat.id
    token = m.text[9:]
    #token = re.escape(token)
    if "/" in token:
        results = "Error en la búsqueda"
    elif len(token)<3:
        results = "Haz una búsqueda más larga"
    else:
    #token = "the room"
        url = "http://kat.cr/json.php?q=" + token + "category:movies" + "/?field=seeders&sorder=desc"
        link = urllib.urlopen(url)
        data = json.loads(link.read())
        results= ""
    #print data
    # [0]['title'] ['torrentLink'] ['seeds']
        if int(float(data['total_results']))==0:
            results = "No se ha encontrado nada"
        else:
            for item in range(min(int(float(data['total_results'])),3)):
                results = results + data['list'][item]['title'] + "\n" + 'Seeds:' + str(data['list'][item]['seeds']) + "\n" + data['list'][item]['torrentLink'] + "\n"
    #    results = data['list'][0]['title'] + "\n" + 'Seeds:' + str(data['list'][0]['seeds']) + "\n" + data['list'][0]['torrentLink'] + "\n" + data['list'][1]['title'] + "\n" + 'Seeds:' + str(data['list'][1]['seeds']) + "\n" + data['list'][1]['torrentLink'] + "\n" + data['list'][2]['title'] + "\n" + 'Seeds:' + str(data['list'][2]['seeds']) + "\n" + data['list'][2]['torrentLink']
    
    bot.send_message(cid, results)
    

#comandos.append("KAtorrent")
@bot.message_handler(commands=['KAtorrent'])
def command_KAtorrent(m):
    cid = m.chat.id
    token = m.text[11:]
    home=kat.popular()
    #url = "http://kat.cr/json.php?q=" + token
    #link = urllib.urlopen(url)
    #data = json.loads(link.read())
    #print data
    bot.send_message(cid,home)

    for torrent in home:
        torrent.print_details()
        bot.send_message(cid,torrent)
    #for t in Search(token, category=CATEGORY.MOVIES, order= ORDER.SEED):
    #    t.lookup()
    # [0]['title'] ['torrentLink'] ['seeds']
    #results = data['list'][0]['title'] + "\n" + 'Seeds:' + str(data['list'][0]['seeds']) + "\n" + data['list'][0]['torrentLink'] + "\n" + data['list'][1]['title'] + "\n" + 'Seeds:' + str(data['list'][1]['seeds']) + "\n" + data['list'][1]['torrentLink'] + "\n" + data['list'][2]['title'] + "\n" + 'Seeds:' + str(data['list'][2]['seeds']) + "\n" + data['list'][2]['torrentLink']
    #bot.send_message(cid, str(results))
#@bot.message_handler(commands=['what']) # Indicamos que lo siguiente va a controlar el comando '/roto2'.
#def command_what(m): # Definimos una función que resuelva lo que necesitemos.
#    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
#    bot.send_photo( cid, open( 'donotwant.png', 'rb'))
    
#@bot.message_handler(commands=['repetir'])
#def command_repetir(m):
#    cid = m.chat.id
#    for i in range(10): # 10 se puede cambiar por el numero de mensajes
#        bot.send_photo( cid, open( 'donotwant.png', 'rb'))
#        time.sleep(10)
        
comandos.append("repetirwhat")   
descripciones.append("Contesta con la imagen DoNotWantGuy")
@bot.message_handler(commands=['repetirwhat'])
def repetir(m):
    cid = m.chat.id
    global repeatDict
    repeatDict[cid]=True
    #global repeat
    #repeat = True
    
comandos.append("detenerwhat")
descripciones.append("Deja de contestar con la imagen DoNotWantGuy")
@bot.message_handler(commands=['detenerwhat'])
def detener(m):
    cid = m.chat.id
    global repeatDict
    if cid in repeatDict:
        del repeatDict[cid]

comandos.append("piropeame")
descripciones.append("Te cita y te lanza piropos")    
@bot.message_handler(commands=['piropeame'])
def piropeame_command(m):
    global piropeados
    if (not(m.from_user.first_name in piropeados)):
        piropeados.append(m.from_user.first_name)
        
comandos.append("nopiropeame")
descripciones.append("Deja de citarte y lanzarte piropos")    
@bot.message_handler(commands=['nopiropeame'])
def nopiropeame_command(m):
    global piropeados
    if (m.from_user.first_name in piropeados):
        piropeados.pop(piropeados.index(m.from_user.first_name))

# > RHP
#@bot.message_handler(commands=['flood'])
#def flood_command(m):
#    global flood
#    if (not(m.from_user.first_name in flood)):
#        flood.append
# < RHP

  # < JC
comandos.append("gol")
descripciones.append("de señor")
@bot.message_handler(commands=['gol'])
def goldesenyor(m):
    cid = m.chat.id
    audio = open('gol.mp3','rb')
    bot.send_voice(cid, audio)   
    #dejo aqui el resto de la idea por si alguien se anima a hacerlo, que no tengo tiempo
    #falta ampliar con un random entre 
        #el gif de socrates
        #un mensaje que ponga "menudo golazo de señor, lo he visto hace por lo menos 20 minutos
        #la transcripcion del video en mensajes
comandos.append("jesuisjudas")
descripciones.append("A este comando no le veo la gracia")
@bot.message_handler(commands=['JeSuisJudas', 'jesuisjudas'])
def jeSuisJudas(m):
    cid = m.chat.id
    bot.send_message(cid,"Veneciano Cabron")
    
comandos.append("forthewatch")
descripciones.append("¿Cuanto queda hasta el estreno de la siguiente temporada de GoT?")
@bot.message_handler(commands=['forthewatch', 'ForTheWatch'])
def GOT(m):
    cid = m.chat.id
    hoy=datetime.datetime.now()
    estreno = datetime.datetime(2016, 04, 25, 4, 0, 0, 0)
    diferencia=estreno-hoy
    if(estreno < hoy):
        token = "Game of thrones season 6 episode 1"
        url = "http://kat.cr/json.php?q=" + token + "category:series" + "/?field=seeders&sorder=desc"
        link = urllib.urlopen(url)
        data = json.loads(link.read())
        mensaje= ""
        if int(float(data['total_results']))==0:
            mensaje = "No se ha encontrado nada"
        else:
            for item in range(min(int(float(data['total_results'])),3)):
                mensaje = mensaje + data['list'][item]['title'] + "\n" + 'Seeds:' + str(data['list'][item]['seeds']) + "\n" + data['list'][item]['torrentLink'] + "\n"
    else:
        mensaje="Tranquila nenaza, aun quedan " + str(diferencia.days) + " dias, " + str(diferencia.seconds/3600) + " horas, " +str((diferencia.seconds%3600)/60) + " minutos y " + str((diferencia.seconds%3600)%60) + " segundos"
   # mensaje="Hasta los cojones de la puta serie."
    bot.send_message(cid,mensaje)
    

#una funcion de ayuda para el usuario. Creo que seria mejor hacer un script que monitorizara este documento en busca de commands
comandos.append("comandos")
descripciones.append("Lista los comandos disponibles")
@bot.message_handler(commands=['comandos'])
def help(m):
    cid = m.chat.id
    #bot.send_message(cid, "## Comandos actuales ##")
    message= "## Comandos actuales ##\n"
    for com in comandos:
        message= message + "/"+ str(com) + " - " + str(descripciones[comandos.index(com)]) +  "\n"
    bot.send_message(cid, message)
    
@bot.message_handler(commands=['comandosbotfather'])
def comandosbotfather_command(m):
    cid = m.chat.id
    #bot.send_message(cid, "## Comandos actuales ##")
    message= ""
    for com in comandos:
        message= message + str(com) + " - " + str(descripciones[comandos.index(com)]) +  "\n"
    bot.send_message(cid, message)

    
    
    
#comandos.append("informer")    
@bot.message_handler(commands=['informer'])
def hola(m):
    cid = m.chat.id
    #if(m.cid == admin2):
    #bot.send_message(5178944, m.text[11:])
    bot.send_message(-1159490, m.text[10:])
    #bot.send_message(-1159490, )
    #else:
    #  bot.send_message(cid, "adios mundo", reply_to_message_id=m.message_id)
    
comandos.append("spoiler")    
descripciones.append("Limpia la pantalla para que otros no lean el Spoiler que acaba de soltar Joan, o en su defecto el Ruso")
@bot.message_handler(commands=['spoiler'])
def spoiler_command(m):
    cid = m.chat.id
    for i in range(2): # 10 se puede cambiar por el numero de mensajes
        bot.send_sticker(cid, open('donotwant.webp','rb'))
        bot.send_sticker(cid, open('donotwantright.webp','rb'))
        
comandos.append("trololo")
descripciones.append("Usar con responsabilidad")
@bot.message_handler(commands=['trololo'])
def troll(m):
    cid = m.from_user.id
    for i in range(50): # 10 se puede cambiar por el numero de mensajes
        bot.send_sticker(cid, open('donotwant.webp','rb'))
        bot.send_sticker(cid, open('donotwantright.webp','rb'))
    #bot.send_message(cid, "comando deshabilitado.. hay mucho flander en el grupo")




# > JC
comandos.append("insulta_a")
descripciones.append("Devuelve un SUPERINGENIOSO insulto")
@bot.message_handler(commands=[''])#insulta_a
def command_insultar(m):
    cid = m.chat.id 
    if m.from_user.id == 1541810:
        token = " Cuallado, te estas rayando"
    elif len(m.text)>10:
        if " " in m.text:
            token = m.text.split(" ", 1)[1]
            numero = random.randrange(1,4) 
            frases ={1:" Tienes menos gracia que una paella con pelotas.",
            2: "Te estas poniedo fuerte cabrón, fuerte como una ballena.",
            3: "Ojalá que Idir apueste a que mañana sigues vivo."
            }
            mensaje = frases[numero]
            token = token + ", " + mensaje
        else:
            token = "Es bromuro no te ralles"
    else:
        token ="¿Pero a quien quieres que insulte?"
    #if m.from_user.id == 5178944:
    #    token = " Jaime, me estas rayando la cabeza"
    tts = gTTS(text=token, lang='es')
    tts.save("tts.mp3")
    audio = open('tts.mp3', 'rb')
    bot.send_voice(cid, audio)
    
comandos.append("buenosdias")
descripciones.append("Para que sigas sintiendote la princesa de la casa")
@bot.message_handler(commands=['buenosdias'])
def command_buenos(m):
    cid = m.chat.id
    bot.send_message(cid, "Buenos días, Princesa")
    
comandos.append("pedirtaxi")
descripciones.append("Está de camino")
@bot.message_handler(commands=['pedirtaxi'])
def command_pedirTaxi(m):
    cid = m.chat.id
    bot.send_message(cid, "Taxi en camino")
    time.sleep(1)
    bot.send_message(cid, ".............🚕")
    time.sleep(1)
    bot.send_message(cid, ".........🚕....")
    time.sleep(1)
    bot.send_message(cid, ".....🚕........")
    time.sleep(1)
    bot.send_message(cid, "..🚕...........")
    time.sleep(1)
    bot.send_message(cid, "🚕.............")
    
comandos.append("pedirgafas")
descripciones.append("También están de camino")
@bot.message_handler(commands=['pedirgafas'])
def command_pedir(m):
    cid = m.chat.id
    numero = random.randrange(1,4) 
    frases ={1:"Vuelve a intentarlo",
    2: "Si ya tienes veinte, revienta chollos!!",
    3: "Hawkers para todos!!"
    }
    mensaje = frases[numero]
    bot.send_message(cid, mensaje)

def slugify(str): # funcion para sacar el slug de una palabra ,es decir para normalizarla
    slug = unicodedata.normalize("NFKD",unicode(str)).encode("ascii", "ignore")
    slug = re.sub(r"[^\w]+", " ", slug)
    slug = "-".join(slug.lower().strip().split())
    return slug

#comandos.append("palabra_magica")
@bot.message_handler(commands=['palabra_magica']) #Para palabra de inicio
def command_palabra(m):
    cid = m.chat.id
    aid = m.from_user.id
    con = None
    if cid != aid: #comprobamos que el admin no escribe en otro sitio que no sea su chat
        bot.send_message(cid,'Todos sabemos que eres un poco retrasado, pero esto lo deberías de hacer por privado. \n P.D: Al menos cambia la palabra')
    else:
        try:
            con = psycopg2.connect(database='camino', user='mogambo') 
            cur = con.cursor()
            
            cur.execute('SELECT admin from juegos') # comprobamos que es admin en algún juego
            if not cur.fetchone():
                bot.send_message(cid, 'No eres admin en ningún juego, cuando lo crees hablamos')
            else:
                cur.execute('SELECT estado from juegos where admin = %d'%aid) # obtenemos el estado del juego en el cual es moderador
                estado = cur.fetchone()[0]
                if estado == 0:
                    if " " in m.text:
                        token = m.text.split(" ")
                        token = slugify(token[1])
                        cur.execute("UPDATE juegos SET palabra='%s', estado=1 WHERE admin = %d" % (token,aid))
                        con.commit()
                        bot.send_message(cid, 'El juego acaba de comenzar, la palabra magica es: '+token)
                        cur.execute('SELECT chat FROM juegos WHERE admin = %d' % aid)
                        bot.send_message(cur.fetchone()[0], 'El juego ha comenzado, ya estamos de camino')
                    else:
                        bot.send_message(cid, 'Pero pedazo de retrasado escribe la palabra')
                    #bot.send_message(cid, 'Insertar palabra') # comprobar si hay palabra o no en el comando y cuando se inserte mandar mensaje al grupo
                else:
                    bot.send_message(cid, 'No puedes modificar la palabra mágica durante el desarrollo de un juego')
            
        except psycopg2.DatabaseError, e:
            if con:
                con.rollback()
            
            print 'Error %s' % e    
            sys.exit(1)

        finally:
            if con:
                con.close()
                
#comandos.append("comenzar_camino")    
@bot.message_handler(commands=['comenzar_camino']) #Para comenzar juego, crear tabla jugadores
def command_comenzar(m):
    cid = m.chat.id
    aid = m.from_user.id
    con = None

    try:
     
        con = psycopg2.connect(database='camino', user='mogambo') 
        cur = con.cursor()
        
        cur.execute('SELECT chat from juegos where chat = %d' % cid)  
        if cid > 0:
           bot.send_message(cid, '¿Para que cojones quieres jugar solo?')
        elif not cur.fetchone(): # comprobamos si el chat esta en la bd, por si es la primera vez que se juega en ese chat
            cur.execute('SELECT admin from juegos where admin = %d' % aid) 
            if not cur.fetchone(): # comprobamos si el administrador no esta moderando otro juego
                cur.execute('INSERT INTO juegos (chat, admin, estado) VALUES (%d, %d, 0)' % (cid,aid))
                con.commit()
                bot.send_message(cid, m.from_user.first_name + " ahora debes de escribirme por privado la palabra mágica") # añadir bd chat admin y estado 0 sin comenzar
            else:
                bot.send_message(cid, 'no puedes ser el moderador en varios juegos')
        else: # el chat esta en la bd por lo que comprobamos el usuario y el estado del juego
            cur.execute('SELECT admin FROM juegos where admin = %d'%aid)
            if not cur.fetchone(): # comprobamos si el jugador ya es moderador
                cur.execute('SELECT estado FROM juegos WHERE chat =%d'%cid) # si no esta jugando comprobamos el estado del juego
                estado = cur.fetchone()[0]
                if estado == 0:
                    bot.send_message(cid, 'El juego está apunto de comenzar, el moderador debe de suministrar la palabra mágica')
                elif estado == 1:
                    bot.send_message(cid, 'No puedes empezar un juego nuevo sin terminar el actual')
                elif estado == 2: # El juego estaba terminado por lo que preparamos el nuevo juego
                    cur.execute('UPDATE juegos SET admin=%d, estado=0 where chat=%d ' % (aid,cid))
                    con.commit()
                    bot.send_message(cid, m.from_user.first_name + " ahora debes de escribirme por privado la palabra mágica")
            else: # Si el admin ya esta en un juego comprobamos si esta en este, si lo esta comprobamos el estado sin comenzar o en juego. Si no esta es que esta moderando otro juego
                cur.execute('SELECT admin FROM juegos WHERE chat =%d and admin=%d'%(cid,aid))  
                if not cur.fetchone(): # el admin esta moderando otro juego
                    bot.send_message(cid, m.from_user.first_name + " no puedes ser moderador de más de un juego")
                else:
                    cur.execute('SELECT estado FROM juegos WHERE chat =%d'%cid) # si no esta jugando comprobamos el estado del juego
                    estado = cur.fetchone()[0]
                    if estado == 0:
                        bot.send_message(cid, 'El juego está apunto de comenzar, debes suministrar la palabra mágica')
                    elif estado == 1:
                        bot.send_message(cid, 'No puedes empezar un juego nuevo sin terminar el actual')
                
    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()
        commands.getoutput("sudo /etc/init.d/postgresql start")
        bot.send_message(cid, 'El chino del servidor estaba durmiendo, pero ya se ha despertado. Intentalo de nuevo')
        commands.getoutput("python bot.py")
        print 'Error %s' % e    
        sys.exit(1)

    finally:
        if con:
            con.close()

#comandos.append("terminar_camino")
@bot.message_handler(commands=['terminar_camino']) #Para terminar el juego en cualquier momento
def command_terminar(m):
    cid = m.chat.id
    aid = m.from_user.id
    con = None

    try:
        con = psycopg2.connect(database='camino', user='mogambo') 
        cur = con.cursor()
        cur.execute('SELECT estado from juegos where admin = %d' % aid)
        estado = cur.fetchone()
        if not estado: #comprobamos que el admin esta en la bd
            bot.send_message(cid, "Para terminar un juego primero debes moderarlo")
        elif estado == 0:
            cur.execute('SELECT chat from juegos where admin = %d' % aid)
            chat = cur.fetchone
            cur.execute('UPDATE juegos SET estado = 2, admin = null, palabra = null where admin = %d' % aid)
            con.commit()
            bot.send_message(chat, "Juego terminado sin comenzarlo")
        elif estado != 2: #Si es igual a dos no decimos nada puesto que el admin sera igual a null
            # Terminar el juego poniendo el admin a null y la palabra a null y cambiando el estado de los jugadores
            cur.execute('SELECT chat, palabra from juegos where admin = %d' % aid)
            atributos = cur.fetchone()
            cur.execute('UPDATE juegos SET estado = 2, admin = null, palabra = null where admin = %d' % aid)
            cur.execute('UPDATE jugadores SET palabra = null where chat = %d' % atributos[0])
            con.commit()
            bot.send_message(atributos[0], "La palabra mágica era: "+ atributos[1] +" losers, que sois unos losers.")
            
    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()
        commands.getoutput("sudo /etc/init.d/postgresql start")
        bot.send_message(cid, 'El chino del servidor estaba durmiendo, pero ya se ha despertado. Intentalo de nuevo')
        commands.getoutput("python bot.py")
        print 'Error %s' % e    
        sys.exit(1)

    finally:
        if con:
            con.close()

#comandos.append("camino_a")            
@bot.message_handler(commands=['camino_a']) #Para el juego en si
def command_camino(m):
    cid = m.chat.id
    aid = m.from_user.id
    con = None

    try:
        con = psycopg2.connect(database='camino', user='mogambo') 
        cur = con.cursor()
        cur.execute('SELECT estado, admin, palabra from juegos where chat = %d' % cid)
        datos = cur.fetchone()
        if datos[0] == 2 or not datos[0]:
            bot.send_message(cid, 'Para poder jugar primero debe de crearse el juego')
        elif datos[0] == 0:
            bot.send_message(cid, 'El moderador debe de suministrar la palabra mágica')
        else:
            if " " in m.text:
                token = m.text.split(" ")
                token = slugify(token[1])
                if datos[1] == aid: # El moderador reconduce el juego y se cambia el estado de los jugadores
                    if datos[2]==token:
                        bot.send_message(cid, 'Enhorabuena el moderador es retrasado y os acaba de decir la palabra mágica')
                    else:
                        cur.execute('UPDATE jugadores SET palabra = null where chat = %d' % cid)
                        con.commit()
                        bot.send_message(cid, 'Camino reconducido')
                
                else: # Es un jugador el que utiliza su turno de juego, comprobamos que lo no lo haya utilizado
                    cur.execute('SELECT jugador,palabra from jugadores where jugador = %d and chat =%d' % (aid,cid))
                    atributos = cur.fetchone()
                    
                    if not atributos: # El jugador no ha jugado nunca en ese chat por lo que lo agregamos junto con su palabra
                        cur.execute("INSERT INTO jugadores (chat, jugador, palabra) VALUES (%d, %d, '%s')" % (cid,aid,token))
                        if datos[2] == token: # El jugador a acertado la palablra magica, por lo que gana el juego y el estado de este pasa a terminado
                            cur.execute('UPDATE jugadores SET palabra = null where chat = %d' % cid)
                            cur.execute('UPDATE juegos SET estado = 2, admin = null, palabra = null where chat = %d' % cid)
                            bot.send_message(cid, 'Enhorabuena, pedazo de hdp has ganado. Mis dies')
                            bot.send_sticker( cid, open( 'misdies.jpg', 'rb'))
                        else:
                            bot.send_message(cid, 'Ese no es el camino, sigue intentandolo')
                        con.commit()
                    elif not atributos[1]: # El jugador estaba jugando pero no habia completado su turno
                        cur.execute("UPDATE jugadores SET palabra ='%s' where chat = %d and jugador = %d" % (token,cid,aid))
                        if datos[2] == token: # El jugador a acertado la palablra magica, por lo que gana el juego y el estado de este pasa a terminado
                            cur.execute('UPDATE jugadores SET palabra = null where chat = %d' % cid)
                            cur.execute('UPDATE juegos SET estado = 2, admin = null, palabra = null where chat = %d' % cid)
                            bot.send_message(cid, 'Enhorabuena, pedazo de hdp has ganado. Mis dies')
                            bot.send_sticker( cid, open( 'misdies.jpg', 'rb'))
                        else:
                            bot.send_message(cid, 'Ese no es el camino, sigue intentandolo')
                        con.commit()
                    else: # Ya habia enviado su palabra, por lo que tiene que esperar 
                        bot.send_message(cid,'Una palabra permitida por turno, impaciente.')
                    
            else:
                bot.send_message(cid, 'Pero pedazo de retrasado escribe la palabra')    
                
    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()
        commands.getoutput("sudo /etc/init.d/postgresql start")
        bot.send_message(cid, 'El chino del servidor estaba durmiendo, pero ya se ha despertado. Intentalo de nuevo')
        commands.getoutput("python bot.py")
        print 'Error %s' % e    
        sys.exit(1)

    finally:
        if con:
            con.close()
#comandos.append("instrucciones")
@bot.message_handler(commands=['instrucciones'])
def command_instrucciones(m):
    cid = m.chat.id
    bot.send_message(cid, "Instrucciones de Camino a Venezuela: \n/comenzar_camino Inicializa el juego  \n/palabra_magica + palabra Comando utilizado por el moderador del juego, el cual, le tendra que pasar la palabra por privado para que nadie sepa cual es \n/camino_a + palabra Por parte de los jugadores se le pasa la palabra que creén que es. Por parte del moderador la palabra para reconducir el juego. \n/terminar_camino Comando utilizado por el moderador para finalizar el juego antes de lo esperado")

comandos.append("reservapadel")
descripciones.append("En construcción")
@bot.message_handler(commands=['ReservaPadel','reservapadel'])
def reserva_padel_command(m):
    cid = m.chat.id
  #  if(m.cid == admin2):
    bot.send_message(cid, "En construcción")
    bot.send_photo( cid, open( 'padel.jpg', 'rb')) # Con la función 'send_photo()' del bot, enviamos al ID de la conversación que hemos almacenado previamente la foto de nuestro querido :roto2:

     # bot.send_message(-1159490, 'huele como a playa, no?')
     # bot.send_message(-1159490, )
 #   else:
  #    bot.send_message(cid, "adios mundo", reply_to_message_id=m.message_id)

#comandos.append("jabu")    #estoy en la hora del café ya iré probando tontadas.
#@bot.message_handler(commands=['jabu'])
#def command_jabu(m):
#    cid = m.chat.id
#    url = "http://ip.jsontest.com/"
#    link = urllib.urlopen(url)
#    data = json.loads(link.read())
#    results= ""
#    if len(data['ip']) < 0:
#        results = "NOPE"
#    else:
#        results = results + data['ip']
#        
#    bot.send_message(cid, results)
    
comandos.append("letocadespertara")
descripciones.append("No dejéis que el bot muera, él no lo haría")
@bot.message_handler(commands=['letocadespertara'])
def command_letocadespertara(m):
    cid = m.chat.id
    message = ''
    usersDesp = []
    try:
        f = open('usuarios.txt', 'r')
        for line in f:
            line = line.split(' - ')
            if int(line[1]) > 0:
                userD = line[0]
                usersDesp.append(userD)
        f.close()
        pringado = random.randrange(0, len(usersDesp)+1)
        message = usersDesp[pringado]
        
        bot.send_message(cid, message)
    except:
        bot.send_message(cid, "Dejame dormir tranquilo. Día libre")
    


comandos.append("ban")
descripciones.append("Reporta a un usuario objetivo")
@bot.message_handler(commands=['ban'])
def ban_command(m):
    cid = m.chat.id
    if cid>0:
        return
    if " " in m.text:
        #usuarioObjetivo = m.text.split(" ", 1)[1]
        if "@" in m.text:
            usuarioObjetivo = m.text.split("@", 1)[1]
        else:
            bot.send_message(cid,"Tienes que citar al usuario objetivo")
            return
        if " " in usuarioObjetivo:
            usuarioObjetivo = usuarioObjetivo.split(" ", 1)[0]
        if usuarioObjetivo == "None":
            return
        client = MongoClient()
        db = client.bot
        user = {"username" : usuarioObjetivo}
        #print user
        if db.users.count(user) != 0:
            idObjetivo=db.users.find({"username":usuarioObjetivo})
            document=""
            for document in idObjetivo:
                i=0
                #print(document)
            idObjetivo= document.get("_id")
            report= {"idObjetivo":idObjetivo}
            report["reportedAt"]=datetime.datetime.utcnow()
            report["reportedBy"]=m.from_user.id
            if (db.ban.find({"reportedBy":m.from_user.id,"idObjetivo":idObjetivo}).count()>0) and (m.from_user.id!="6761180"):
                bot.send_message(cid,"Deja descansar a la reportadora")
                return
            db.ban.insert(report)
            if db.ban.find({"idObjetivo":idObjetivo}).count()>3:
                bot.send_message(cid,"Nos vemos en el infierno")
                bot.kick_chat_member(cid, idObjetivo)
            else: 
                mensaje=usuarioObjetivo+", estás jugando con fuego\nLlevas " + str(db.ban.find({"idObjetivo":idObjetivo}).count()) + " reporte(s)"
                bot.send_message(cid,mensaje)
            #print db.ban.find({"idObjetivo":idObjetivo}).count()
                
        else:
            bot.send_message(cid,"No tengo datos de ese usuario")
    else:
        bot.send_message(cid,"Si no me dices a quien...")

comandos.append("visto")
descripciones.append("Indica que has visto el último capítulo de GoT (VIP)")
@bot.message_handler(commands=['visto'])
def visto_command(m):
    cid = m.chat.id
    if cid>0:
        username=m.chat.username
    else:
        username = m.from_user.username
    users=["lmontesn","DameYoPido","Telefonillo","barbarity", "ThomasTens","Jaimeorro","Apodaco","cloco46"]
    if username not in users:
        bot.send_message(cid,"¿Te conozco?")
        return
    client = MongoClient()
    db = client.bot
    visto={"username":username}
    if (db.vistos.count(visto)==0):
        visto["vistoAt"]=datetime.datetime.utcnow()
        db.vistos.insert(visto)
        bot.send_message(cid,"Your watch is ended ")
        if (db.vistos.count()==len(users)):
            bot.send_message(cid,"Ya estamos todos, que comiencen los spoilers")
    else:
        bot.send_message(cid,"Que si, pesado")

comandos.append("faltaporver")
descripciones.append("Indica que usuarios no han visto todavía el último capítulo de GoT (VIP)")
@bot.message_handler(commands=['faltaporver'])
def faltaporver_command(m):
    cid = m.chat.id
    users=["lmontesn","DameYoPido","Telefonillo","barbarity", "ThomasTens","Jaimeorro","Apodaco","cloco46"]
    client = MongoClient()
    db=client.bot
    if (db.vistos.count()==len(users)):
        bot.send_message(cid,"No falta nadie por ver el capítulo")
    else:
        message="Los siguientes usuarios aún no han visto el capítulo:"
        for user in users:
            userdb={"username":user}
            if(db.vistos.count(userdb)==0):
                message=message+"\n" + "@" + str(user)
        bot.send_message(cid,message)
        
comandos.append("reiniciarcapitulo")
descripciones.append("Reinicia la lista de vistos del último capítulo de GoT (VIP)")
@bot.message_handler(commands=['reiniciarcapitulo'])
def reiniciarcapitulo_command(m):
    cid=m.chat.id
    client=MongoClient()
    db=client.bot
    db.vistos.remove({})
    bot.send_message(cid,"A esperar hasta el domingo.")

comandos.append("hodor")
descripciones.append("Hodor")
@bot.message_handler(commands=['hodor'])
def hodor_command(m):
    cid=m.chat.id
    bot.send_message(cid,"Obstruye el corredor")
    
comandos.append("hodor2")
descripciones.append("NO LO ACTIVES NUNCA")
@bot.message_handler(commands=['hodor2'])
def hodor2_command(m):
    cid=m.chat.id
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Si')
    itembtn2 = types.KeyboardButton('No')
    markup.add(itembtn1, itembtn2)
    bot.send_message(cid, '¿Necesita Ruben un cursillo de programación?', reply_markup=markup)
    
comandos.append("hodor2sostiene")
descripciones.append("NO LO ACTIVES NUNCA")
@bot.message_handler(commands=['hodor2sostiene'])
def hodor2_command(m):
    cid=m.chat.id
    markup = types.ReplyKeyboardHide()
    bot.send_message(cid, text="HIJO DE PUTA", reply_markup=markup)



comandos.append("cuervo") 
descripciones.append("Cuallado es retrasado")
@bot.message_handler(commands=['cuervo'])
def cuervo(m):
    if " " in m.text:
            token = m.text.split(" ", 1)[1]
            bot.send_message(-26557866,"Un cuervo ha llegado. Parece que lleva un mensaje de " +m.chat.first_name+ " en el cuello: \n\n" + token)
            
        
comandos.append("avisarcuervos")
descripciones.append("Avisa mediante cuervos de posibles spoilers a los usuarios que no hayan visto el último capítulo de GoT (VIP)")
@bot.message_handler(commands=['avisarcuervos'])
def avisarcuervos_command(m):
    cid = m.chat.id
    users=["lmontesn","DameYoPido","Telefonillo","barbarity", "ThomasTens","Jaimeorro","Apodaco","cloco46"]
    client = MongoClient()
    db=client.bot
    if (db.vistos.count()==len(users)):
        bot.send_message(cid,"No falta nadie por ver el capítulo")
    else:
        message="Los cuervos han sido mandados."
        cuervos="Los caminantes blancos impacientes están soltando spoilers en el grupo.\nSerá mejor que uses /cuervo para comunicarte con ellos."
        for user in users:
            userdb={"username":user}
            if(db.vistos.count(userdb)==0):
                idObjetivo=db.users.find({"username":user})
                document=""
                for document in idObjetivo:
                    i=0
                #print(document)
                idObjetivo= document.get("_id")
                print user
                bot.send_message(idObjetivo, cuervos)
        bot.send_message(cid,message)

#comandos.append("unban")
#descripciones.append("reporta a un usuario objetivo")
@bot.message_handler(commands=['unban'])
def unban_command(m):
    cid = m.chat.id
    if cid>0:
        return
    if " " in m.text:
        #usuarioObjetivo = m.text.split(" ", 1)[1]
        if "@" in m.text:
            usuarioObjetivo = m.text.split("@", 1)[1]
        else:
            bot.send_message(cid,"Tienes que citar al usuario objetivo")
            return
        if " " in usuarioObjetivo:
            usuarioObjetivo = usuarioObjetivo.split(" ", 1)[0]
        if usuarioObjetivo == "None":
            return
        client = MongoClient()
        db = client.bot
        user = {"username" : usuarioObjetivo}
        #print user
        idObjetivo=db.users.find({"username":usuarioObjetivo})
        document=""
        for document in idObjetivo:
            i=0
            #print(document)
        idObjetivo= document.get("_id")
        bot.send_message(cid,"Nos vemos en el infierno")
        bot.unban_chat_member(cid, idObjetivo)
        #print db.ban.find({"idObjetivo":idObjetivo}).count()
    else:
        bot.send_message(cid,"Si no me dices a quien...")


comandos.append("polestats")
descripciones.append("¿Quien es el más poleman?")
@bot.message_handler(commands=['polestats'])
def polestats_command(m):
    cid = m.chat.id
    client = MongoClient()
    db = client.bot
    polemans=db.poles.find().sort("totalPoles",-1)
    if db.poles.count()==0:
        bot.send_message(cid,"No hay datos de poles ahora mismo")
        return
    document=""
    message = "Este es el ranking de polemans:\n"
    for document in polemans:
        message=message + str(document.get("userPoleman")) + " -> " + str(document.get("totalPoles")) + "\n"
            #print(document)
    bot.send_message(cid, message)        
    
comandos.append("dejalocerrado")
descripciones.append("Dejalo cerrado, calorrado, hodor")
@bot.message_handler(commands=['dejalocerrado'])
def dejalo_cerrado_command(m):
    cid = m.chat.id
    audio = open('hodor.mp3','rb')
    bot.send_voice(cid, audio)

def timeout():
    global dedo_veloz_playing
    dedo_veloz_playing=False

comandos.append("dedo_veloz")
descripciones.append("Juega al Dedo Veloz.")
@bot.message_handler(commands=['dedo_veloz'])
def dedo_veloz_command(m):
    cid = m.chat.id
    if cid > 0:
        bot.send_message(cid, "Este juego solo está disponible para grupos, tramposo.")
        return
    if cid == -1159490:
        bot.send_message(cid, "Grupo censurado, que se nos enfada Joan")
        return
    global dedo_veloz_playing
    if dedo_veloz_playing==True:
        bot.send_message(cid,"Ya hay una partida en marcha")
        return
    else:
        dedo_veloz_playing=True
    global dedo_veloz_ended
    dedo_veloz_ended=False
    global jugadores
    t = Timer(60, timeout)
    t.start()
    global ganador
    ganador="None"
    global segundo
    segundo="None"
    jugadores.clear()
    mensaje = bot.send_message(cid, "El primero que pulse 'Go', gana :)")
    time.sleep(2)
    
    bot.edit_message_text("Preparados...", cid, mensaje.message_id)
    numero = random.randrange(3,7)
    time.sleep(numero)
    
    #bot.send_message(cid, "Listos......")
    bot.edit_message_text("Listos.....", cid, mensaje.message_id)
    numero = random.randrange(4,10)
    time.sleep(numero)

    numero = random.randrange(1,3)
    if numero == 1:
        bot.edit_message_text("Un poquito más.........", cid, mensaje.message_id)
        numero = random.randrange(2,7)
        time.sleep(numero)
    numero = random.randrange(1,10)
    if numero == 1:
        bot.edit_message_text("YA!", cid, mensaje.message_id)
        time.sleep(2)
        bot.edit_message_text("Que era broma! Va, ahora si...", cid, mensaje.message_id)
        numero = random.randrange(3,7)
        time.sleep(numero)
    
    markup = types.ReplyKeyboardMarkup()
    palabras = ["Na","No","Ga","Ge","So","Puta"]
    numero = random.randrange(1,6)
    itembtn1 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn2 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn3 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn4 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn5 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn6 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn7 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn8 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    itembtn9 = types.KeyboardButton(palabras[numero])
    numero = random.randrange(1,6)
    
    numero = random.randrange(1,9)
    if numero == 1:
        itembtn1 = types.KeyboardButton('Go')
    elif numero == 2:
        itembtn2 = types.KeyboardButton('Go')
    elif numero == 3:
        itembtn3 = types.KeyboardButton('Go')
    elif numero == 4:
        itembtn4 = types.KeyboardButton('Go')
    elif numero == 5:
        itembtn5 = types.KeyboardButton('Go')
    elif numero == 6:
        itembtn6 = types.KeyboardButton('Go')
    elif numero == 7:
        itembtn7 = types.KeyboardButton('Go')
    elif numero == 8:
        itembtn8 = types.KeyboardButton('Go')
    elif numero == 9:
        itembtn9 = types.KeyboardButton('Go')
                            
    markup.row(itembtn1,itembtn2,itembtn3)
    markup.row(itembtn4,itembtn5,itembtn6)
    markup.row(itembtn7,itembtn8,itembtn9)
    global mensaje_id
    #bot.edit_message_text("YA!", cid, mensaje.message_id)
    mensaje=bot.send_message(cid, 'YA!', reply_markup=markup)
    partidaTime=datetime.datetime.now(pytz.timezone('Europe/Madrid'))
    mensaje_id=mensaje.message_id
    
    # Juego

    while(dedo_veloz_playing==True):
        dedo_veloz_playing==True
    markup = types.ReplyKeyboardHide()
    time.sleep(1)
    dedo_veloz_ended=True
    if ganador=="None":
        print "timeout"
        bot.send_message(cid, "Timeout", reply_markup=markup)
        return
    else:
        t.cancel()
    global ganadorTime
    global segundoTime
    if jugadores[ganador]>1:
        message="Y el ganador es: " + str(ganador) + " con un total de " + str(jugadores[ganador]) + " intentos"
    else:
        message="Y el ganador es: " + str(ganador) + " con un total de " + str(jugadores[ganador]) + " intento"
    
    ganadorSec=(float(ganadorTime.second)+(float(ganadorTime.microsecond)/(10**len(str(ganadorTime.microsecond)))))
    if ganador!="None" and segundo!="None":
        segundoSec=(float(segundoTime.second)+(float(segundoTime.microsecond)/(10**len(str(segundoTime.microsecond)))))
        difPrimero=segundoSec - ganadorSec
        message=message+"\n\nHa acertado " + str(difPrimero) + " segundos antes que " + str(segundo)
        
    partidaSec=(float(partidaTime.second)+(float(partidaTime.microsecond)/(10**len(str(partidaTime.microsecond)))))
    difPartida=ganadorSec-partidaSec
    message=message+"\n\nHa tardado " + str(difPartida) + " segundos en acertar."
    bot.send_message(cid, message, reply_markup=markup)
    #bot.edit_message_text("YA!", cid, mensaje_id,reply_markup=markup)
    mensaje_id=0
    client = MongoClient()
    db = client.bot
    dedo_ganador = {"username" :ganador}
    if db.dedoveloz.count(dedo_ganador)==0:
        dedo_ganador["totalVictorias"]=1
    else:
        dedoObjetivo=db.dedoveloz.find({"username":ganador})
        document=""
        for document in dedoObjetivo:
            i=0
                #print(document)
        totalVictorias= document.get("totalVictorias")
        dedo_ganador["totalVictorias"]=totalVictorias+1
        db.dedoveloz.remove(document)
        
    dedoAdmin=db.dedoveloz.find_one({"username": "dedoAdmin"})
    totalPartidas=dedoAdmin.get("totalPartidas")
    totalPartidas=totalPartidas+1
    dedoAdminAux={"username":"dedoAdmin", "totalPartidas":totalPartidas}
    db.dedoveloz.remove(dedoAdmin)
    db.dedoveloz.insert(dedoAdminAux)
    db.dedoveloz.insert(dedo_ganador)
    
comandos.append("photofinish")
descripciones.append("Photo finish de la última partida de Dedo Veloz")
@bot.message_handler(commands=['photofinish'])
def photofinish_command(m):
    cid = m.chat.id
    global ganador
    global segundo
    global ganadorTime
    global segundoTime
    if dedo_veloz_playing==True:
        bot.send_message(cid,"Hay una partida en marcha")
        return
    if ganador!="None" and segundo!="None":
        message=str(ganadorTime) + " " + str(ganador)+": Go\n" + str(segundoTime) + " " + str(segundo)+": Go\n"
        ganadorSec=(float(ganadorTime.second)+(float(ganadorTime.microsecond)/(10**len(str(ganadorTime.microsecond)))))
        segundoSec=(float(segundoTime.second)+(float(segundoTime.microsecond)/(10**len(str(segundoTime.microsecond)))))
        dif=segundoSec - ganadorSec
        message=message+"\n"+str(ganador) + " ha ganado la partida por " + str(dif) + " segundos."
        bot.send_message(cid,message)
    else:
        bot.send_message(cid,"No hay datos")
    
    
comandos.append("dedovelozstats")
descripciones.append("¿Quien tiene el dedo más veloz?")
@bot.message_handler(commands=['dedovelozstats'])
def dedovelozstats_command(m):
    cid = m.chat.id
    client = MongoClient()
    db = client.bot
    dedoAdmin=db.dedoveloz.find_one({"username": "dedoAdmin"})
    totalPartidas=dedoAdmin.get("totalPartidas")
    veloces=db.dedoveloz.find().sort("totalVictorias",-1)
    if db.dedoveloz.count()==0:
        bot.send_message(cid,"No hay datos de dedos veloces ahora mismo")
        return
    document=""
    message= "Se han jugado " + str(totalPartidas) + " partidas\n"
    message = message + "Este es el ranking de dedos más veloces:\n"
    for document in veloces:
        if str(document.get("username"))!="dedoAdmin":
            message=message + str(document.get("username")) + " -> " + str(document.get("totalVictorias")) + "\n"
            #print(document)
    bot.send_message(cid, message)


comandos.append("iniciomundial")
descripciones.append("Reglas e iniciación del mundial de Dedo Veloz")
@bot.message_handler(commands=['iniciomundial'])
def iniciomundial_command(m):
    cid = m.chat.id
    if cid > 0:
        bot.send_message(cid, "Este juego solo está disponible para grupos, tramposo.")
        return
    if cid == -1159490:
        bot.send_message(cid,"Grupo prohibido, que Joan se enfada y saca la reportadora")
        return
    global dedovelozmundial_playing
    if dedovelozmundial_playing==True:
        bot.send_message(cid,"Ya hay un mundial en juego")
        return
    bot.send_message(cid, "En 2 minutos dará comienzo el mundial de Dedo Veloz. Por favor, que todos los participantes empiecen sus preparativos. Estas son las normas:\n\n1. El mundial tiene una duración de 10 minutos.\n2. Durante el transcurso del mundial, no se detendrá la partida en ningún caso.\n3. Si alguien accede o modifica el bot durante la duración del mundial, la furia de Mogambo caerá sobre él.\n4. El juego debe ser jugado en móvil, nada de tablets.\n5. No valen mordiscos ni empujones.")
    time.sleep(120)
    bot.send_message(cid, "Vamos a ir empezando. Mucha suerte a todos")


comandos.append("dedovelozmundial")
descripciones.append("Que comience el mundial de Dedo Veloz")
@bot.message_handler(commands=['dedovelozmundial'])
def dedovelozmundial_command(m):
    cid = m.chat.id
    if cid > 0:
        bot.send_message(cid, "Este juego solo está disponible para grupos, tramposo.")
        return
    if cid == -1159490:
        bot.send_message(cid,"Grupo prohibido, que Joan se enfada y saca la reportadora")
        return
    global dedovelozmundial_playing
    if dedovelozmundial_playing==True:
        bot.send_message(cid,"Ya hay un mundial en juego")
        return
    else:
        dedovelozmundial_playing=True
    client = MongoClient()
    db = client.bot
    db.dedovelozmundial.remove({})
    db.dedovelozmundial.insert({"username":"dedoAdmin","totalPartidas":0})
    mensaje=bot.send_message(cid, "5")
    time.sleep(1)
    bot.edit_message_text("4", cid, mensaje.message_id)
    time.sleep(1)
    bot.edit_message_text("3", cid, mensaje.message_id)
    time.sleep(1)
    bot.edit_message_text("2", cid, mensaje.message_id)
    time.sleep(1)
    bot.edit_message_text("1", cid, mensaje.message_id)
    time.sleep(1)
    bot.edit_message_text("¡Que comience el mundial!", cid, mensaje.message_id)
    t0 = time.time()
    while ((time.time() - t0)<600) and dedovelozmundial_playing==True:
        dedo_veloz_mundial(cid)
        time.sleep(5)
    dedovelomundial_playing=False
    bot.send_message(cid, "El mundial ha llegado a su fin. A continuación se os muestra la clasificación:\n\n")
    dedoAdmin=db.dedovelozmundial.find_one({"username": "dedoAdmin"})
    totalPartidas=dedoAdmin.get("totalPartidas")
    veloces=db.dedovelozmundial.find().sort("totalVictorias",-1)
    if db.dedovelozmundial.count()==0:
        bot.send_message(cid,"No hay datos de dedos veloces ahora mismo")
        return
    document=""
    message= "Se han jugado " + str(totalPartidas) + " partidas en esta edición del mundial\n"
    message = message + "Este es el ranking de dedos más veloces:\n"
    for document in veloces:
        if str(document.get("username"))!="dedoAdmin":
            message=message + str(document.get("username")) + " -> " + str(document.get("totalVictorias")) + "\n"
            #print(document)
    bot.send_message(cid, message)
    
comandos.append("detenermundial")
descripciones.append("Que se detenga el mundial de Dedo Veloz")
@bot.message_handler(commands=['detenermundial'])
def detenermundial_command(m):
    global dedovelozmundial_playing
    dedovelozmundial_playing=False
    global dedo_veloz_playing
    dedo_veloz_playing=False

# CONECTAME 4
comandos.append("info4")
descripciones.append("Muestra la info de conectame4")
@bot.message_handler(commands=['info4']) 
def info4(m):
    cid=m.chat.id
    global jugando4, equipo_rojo4, equipo_amarillo4, turno4, fichas4, tamanyo4, margen4
    global filas4, columnas4, tablero4, turno4, equipo_rojo4, equipo_amarillo4, mensaje_id_conectame4
    
    if jugando4 == False:
        bot.send_message(cid, "No hay partida en marcha, capullo.")
        return
    
    text = 'Equipo Rojo: '
    for jugador in equipo_rojo4:
        text = text + jugador + ' '
    bot.send_message(cid, text)
    
    text = 'Equipo Amarillo: '
    for jugador in equipo_amarillo4:
        text = text + jugador + ' '
    bot.send_message(cid, text)
    
    bot.send_message(cid, "Empieza el equipo: " + turno4)
    pinta_tablero4(cid)
    
comandos.append("conectame4")
descripciones.append("Juega a Conectame4")
@bot.message_handler(commands=['conectame4']) 
def conectame4(m):
    cid=m.chat.id
    global jugando4, equipo_rojo4, equipo_amarillo4, turno4, fichas4, tamanyo4, margen4
    global filas4, columnas4, tablero4, turno4, equipo_rojo4, equipo_amarillo4, mensaje_id_conectame4
    
    # Comprobamos que no hay partida en marcha
    if jugando4 == True:
        bot.send_message(cid, "Ya hay partida en marcha, capullo.")
        return
    
    fichas4 = 4
    tamanyo4 = 25
    margen4 = 5
    filas4 = 6
    columnas4 = 7
    tablero4 = [[None]*columnas4 for _ in range(filas4)]
    turno4 = "Rojo"
    equipo_rojo4 = []
    equipo_amarillo4 = []
    mensaje_id_conectame4=""
    jugando4 = True
    
    
    # Generamos los equipos
    jugadores4 = ["lmontesn","DameYoPido", "Telefonillo","Gazpacho","ThomasTens","Jaimeorro","Apodaco","cloco46", "jabujavi"]
    aux = True
    while len(jugadores4) != 0:
        num = random.randrange(0, len(jugadores4))
        if aux:
            equipo_rojo4.append(jugadores4[num])
        else:
            equipo_amarillo4.append(jugadores4[num])
        aux = not aux
        del jugadores4[num]
    
    info4(m)
    mostrar_teclado4(cid)
    
# FIN CONECTAME4



@bot.message_handler(commands=['startgif']) 
def startgif_command(m):
    cid=m.chat.id
    global giffing
    giffing=True
    global imagesToGIF
    imagesToGIF=[]
    
    
    
@bot.message_handler(commands=['stopgif'])
def stopgif_command(m):
    cid=m.chat.id
    global giffing
    giffing=False
    global imagesToGIF
    npimages=np.asarray(imagesToGIF, dtype=object)
    print "numpyed"
    writeGif("gif1.gif",npimages,duration=1,loops=10)
    bot.send_document(cid,open('gif1.gif', 'rb'))
    
    

@bot.message_handler(func=lambda m: True)
def patata(m):
    cid = m.chat.id
    global cidPositive
    global piropeados
    global repeatDict
    global ultimo_dia
    #dia = datetime.datetime.now(pytz.timezone('Europe/Madrid')).day

    if not(someone_pole()) and str(cid) == "-1159490":
        bot.send_message(cid, m.from_user.username + " ha hecho la pole!")
        client = MongoClient()
        db = client.bot
        user = {"username" : m.from_user.username}
        #lastDay={"lastDay" : dia}
        #db.dia.remove({})
        #db.dia.insert(lastDay)
        if db.users.count(user) == 0:
            bot.send_message(cid,"¿Te conozco?")
            return
        #print str(datetime.datetime.now(pytz.timezone('Europe/Madrid')).date)
        pole= {"idPoleman":m.from_user.id}
        ahora = datetime.datetime.now(pytz.timezone('Europe/Madrid'))
        fecha = datetime.date(ahora.year,ahora.month,ahora.day)
        if db.poles.count(pole)==0:
            pole["lastPole"]=str(fecha)
            pole["totalPoles"]=1
            pole["userPoleman"]=m.from_user.username

        else:
            poleObjetivo=db.poles.find({"userPoleman":m.from_user.username})
            document=""
            for document in poleObjetivo:
                i=0
                #print(document)
            totalPoles= document.get("totalPoles")
            pole["lastPole"]=str(fecha)
            pole["totalPoles"]=totalPoles+1
            pole["userPoleman"]=m.from_user.username
            db.poles.remove(document)
        db.poles.insert(pole)
    if(m.text[0] == "/"):
        bot.send_message(cid, "Comando desconocido, pero todo se andará...")
    if cid<0:
        if (str(m.from_user.id) == "0"):
            bot.send_sticker(cid, open('paquitov1.webp', 'rb'), reply_to_message_id=m.message_id)
    if ("compañero" in m.text):
        bot.send_photo(cid,open('celma.jpg', 'rb'),reply_to_message_id=m.message_id)
    if ("Rafa" in m.text):
        bot.send_message(cid,"Huele como a playa")
    if(cid in repeatDict):
        if(repeatDict[cid]):
            bot.send_sticker( cid, open( 'donotwant.webp', 'rb'))
    if (m.from_user.first_name in piropeados):
        numero = random.randrange(1,14) 
        frases ={1:"¡¡Que el mundo pare de girar, que yo me bajo para conocerte!!",
        2:"Ojalá fueras el mar y yo la roca, para que estuvieras continuamente tocando mi boca.",
        3:"¡Quien fuera sol para rozarte todo el día con sus rayos!",
        4:"Tu nombre debe ser Bill Gates, se te ve muy rico.",
        5:"¡Ponte en mis rodillas precioso, sabrás lo que es estar en un trono!",
        6:"¡Si ese cuerpo fuera montaña, yo me convierto en alpinista!",
        7:"Qué bonita es la lluvia cuando se contempla bajo el paraguas de tus abrazos.",
        8:"¡Eso si que son buenas curvas y no las de la carretera de mi pueblo, acho!",
        9:"Mi camión se acelera cuando te veo pasar por la acera.",
        10:"No existe cosa más bonita que mi hermosa princesita.",
        11:"¡Un gran corazón como el tuyo necesita un cuerpo tan grande!",
        12:"Tienes cuerpo para todo el barrio, precioso!",
        13: "Entre esa boquita de nata y esos ojos de gata, te metería dos pollazos que te dejaría cegata!"
        }
        mensaje = frases[numero]
        bot.send_message(cid,mensaje,reply_to_message_id=m.message_id)

from keepUp import KeepUp
test=False
check_self_runnings()
if test==False:
    k= KeepUp()
    user="thorapio"
    password="mogambo"
    workspace="https://ide.c9.io/thorapio/mogambo-bot"
    k.loadTask(user,password,workspace)
    clean_tmp()

execute_mongo()
load_users()
check_date()

#############################################
#Peticiones
bot.polling(none_stop=True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algún fallo.