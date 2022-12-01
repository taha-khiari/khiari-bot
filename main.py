import urllib.parse

import requests
from deep_translator import GoogleTranslator
from flask import Flask, request, render_template
import pyttsx3
engine= pyttsx3.init('sapi5')
voices= engine.getProperty('voices')
engine.setProperty("rate", 170)
engine.setProperty('voice',voices[1].id)
def speak(audio):
        engine.say(audio)
        engine.runAndWait()

app= Flask(__name__,template_folder="templates")
id_app="A8RHYW-A435JQA5L8"
host ="api.wolframalpha.com"
con_id=""
s=""
qr=[]

@app.route("/")
def home():
    return render_template("home.html",data=qr)
@app.route("/",methods=["POST"])
def activerkhiari():
    global con_id,host,s


    question= request.form["question"]
    qrtemp=[]
    qrtemp.append(question)
    question=GoogleTranslator(source="fr",target="en").translate(question)
    if con_id:
        query = f"http://{host}/v1/conversation.jsp?appid={id_app}&conversationid={con_id}&i={urllib.parse.quote_plus(question)}"
    else:
        query = f"http://{host}/v1/conversation.jsp?appid={id_app}&i={urllib.parse.quote_plus(question)}"
    if s:
        query+= f'&s={s}'
        s=""
    reponse=requests.get(query).json()
    if reponse.get('error',0):
        qrtemp.append("j pas comprie poser une autre question!")
        qr.append(qrtemp)
        return home()
    con_id = reponse["conversationID"]
    host = reponse["host"] + "/api"
    s = reponse.get("s", "")
    reponse= GoogleTranslator(source="en",target="fr").translate(reponse["result"])
    qrtemp.append(reponse)
    #speak(qrtemp)
    qr.append(qrtemp)

    return home()

if __name__=="__main__":
    app.run()
