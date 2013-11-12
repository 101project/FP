# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
import os, subprocess
import re
import requests
from flaskext.mail import Mail

app = Flask(__name__)

def send_mail(to_address, from_address, subject, plaintext, html):
    r = requests.\
        post("https://api.mailgun.net/v2/fastprinter.co/messages",
            auth=("api", "key-33oilme1umvu7on59yr34trmd50tsbg5"),
             data={
                 "from": from_address,
                 "to": to_address,
                 "subject": subject,
                 "text": plaintext,
                 "html": html,
             }
         )
    return r

@app.route('/hola')
def hello_world():
    return 'Hola a todos desde python!!'

@app.route("/", methods=["POST", "GET"])
def mailin():
    print request.form['From'].encode('utf-8')
    mailReceived = request.form['From'].encode('utf-8')
    mailStriped=mailReceived[mailReceived.find("<")+1:mailReceived.find(">")]
    print "algo"
    donde = request.form['To']
    name = re.sub('@.*','',donde).replace('\"','').strip()
    name = name[name.find("<")+1:].strip()
    print name
    for attachment in request.files.values():
        print mailStriped
        if mailStriped in allowed_users:
            if allowed_file(str(attachment.filename.encode('utf-8'))):
                data = attachment.stream.read()
                with open(attachment.filename.encode('utf-8'), "w") as f:
                    f.write(data)
                    f.close()
                    if countPages(str(attachment.filename.encode('utf-8'))) <= allowed_users[mailStriped]:
                        print attachment.filename.encode('utf-8')
                        imprimiendo = subprocess.Popen(['python', 'rpc_client.py', str(name), str(attachment.filename.encode('utf-8')),centros_auth[name]], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                        #EmailFunction(mailStriped)
                        out, err = imprimiendo.communicate()
                        print out, err            
                        if "Got 0" in str(out):
                            EmailFunction(mailStriped, 'impreso')
                        else:
                            EmailFunction(mailStriped, 'desconocido')
                    else:
                        EmailFunction(mailStriped, 'paginas')
            else:
                EmailFunction(mailStriped, 'tipo')
        else:
            EmailFunction(mailStriped, 'usuario')
    return "OK"

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10081, debug=True)
