# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
import os, subprocess
import re
import requests
from werkzeug.contrib.fixers import ProxyFix
import time

centros_auth ={'elcopion':'10.8.0.102','independencia':'10.8.0.101'}

rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE|re.DOTALL)
UPLOAD_FOLDER = '/home/user/Documents/archivosprueba'
ALLOWED_EXTENSIONS = set(['pdf','docx','doc','xls','xlsx','odt','ppt','pptx'])
allowed_users = {'alfonso.alvz@gmail.com':10, 'poz2k4444@gmail.com':10, 'papnoe_30@hotmail.com':10, 'euni_siete@hotmail.com':10, 'sertiboy18@hotmail.com':10, 'paush238_@hotmail.com':10, 'nnancy_618@hotmail.com':10, 'claudioII@hotmail.es':10, 'mezcaline@terra.com':10, 'vladirock@live.com.mx':10, 'sheyla_kshow@hotmail.com':10, 'kazzi20@hotmail.com':10, 'dir-models@hotmail.com':10,'sandy_gere@hotmail.com':10,'elvis_co22@hotmail.com':10,'Nayeli Torres':'valeriia.moxxa023@gmail.com','marisa':'chuletas_zulema@hotmail.com','violeta':'cuchu_rrumina21@yahoo.com.mx','josé miguel':'josedb@hotmail.es','gesami88@hotmail.com':10,'hadron_n@hotmail.com':10,'videocarr@hotmail.com':10,'pau_w2005@hotmail.com':10,'rojero_ruben@hotmail.com':10,'rosaleesco@hotmail.com':10,'pauline100@live.com.mx':10,'daniels@grupoquark.com':10,'atlcin__3458@hotmail.com':10,'flor_15zurda@hotmail.com':10,'benc2011pasa@hotmail.com':10,'estrellita_15dance@hotmail.com':10,'joce.dm@hotmail.com':10,'eddy_d23@hotmail.es':10,'miguel_0259@hotmail.com':10,'eli_nu@live.com.mx':10, 'lul_aslove@hotmail.com':10,'silvi_100292@hotmail.com':10,'Kikiss_260593@hotmail.com':10,'mye_92_r@hotmail.com':10,'magali_del_rocio@hotmail.com':10,'pepehdz76@gmail.com':10,'jonnyu_@hotmail.com':10}

app = Flask(__name__)

def countPages(filename):
    data = file(filename,"rb").read()
    return len(rxcountpages.findall(data))

def allowed_file(filename):
    if '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
        return True
    else:
        #flash('Not allowed extension')
        return False

def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v2/fastprinter.co/messages",
        auth=("api", "key-33oilme1umvu7on59yr34trmd50tsbg5"),
        data={"from": "Información <no-reply@fastprinter.co>",
              "to": ["alfonso.alvz@gmail.com"],
              "subject": "Hola mundo",
              "text": "This shit's done babe!"})

def EmailFunction(UserEmail, tipo):
    Sender = 'Información <no-reply@fastprinter.co>'
    Subject = 'Información'
    Text = ''
    name = re.sub('@.*','',UserEmail)
    html = open(tipo+'.html')
    send_mail(UserEmail,Sender,Subject,Text,html)
    return html

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

# def impresoras():
#     printers = []
#     pathVPN = "/etc/openvpn/ccd/"
#     clientes = os.listdir(pathVPN)
#     for cliente in clientes:
#         if not "." in cliente:
#             if os.path.isfile(pathVPN + cliente):
#                 f = open(pathVPN + cliente)
#                 line = f.readline()
#                 f.close()
#                 linea = shlex.split(line)
#                 contenido = []
#                 contenido = [linea[1],linea[3][1:],linea[4:]]
#                 #printers.append(linea[3][1:])
#                 printers.append(contenido)
#     return printers



@app.route('/hola')
def hello_world():
    return 'Hola a todos desde python!!'

@app.route("/", methods=["POST", "GET"])
def mailin():
    # see if the message is spam:
    # is_spam = request.form['X-Mailgun-SFlag'] == 'Yes'
    
    #if request.method == 'POST':
    # # access some of the email parsed values:
    #print request.form['To']
    #request.form['subject']
#    print send_simple_message()
    # # stripped text does not include the original (quoted) message, only what
    # # a user has typed:
    #request.form['stripped-text']
    #request.form['stripped-signature']
    # # enumerate through all attachments in the message and save
    # # them to disk with their original filenames:
    # imprimiendo = subprocess.Popen(['python', 'rpc_client.py', 'fastmail', 25, '10.8.0.22'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    #print "communicate"
    #out, err = imprimiendo.communicate()
    #print out, err            
    print request.form['From'].encode('utf-8')
    mailReceived = request.form['From'].encode('utf-8')
    mailStriped=mailReceived[mailReceived.find("<")+1:mailReceived.find(">")]
    #recipient = request.form['content-id-map']
    print "algo"
#    print request.form['Sender']
    donde = request.form['To']
#    before, sep, after = str.rpartition("@")
#    print before
    name = re.sub('@.*','',donde).replace('\"','').strip()
    name = name[name.find("<")+1:].strip()
    print name
    for attachment in request.files.values():
        print mailStriped
        if allowed_file(str(attachment.filename.encode('utf-8'))):
            #filename = secure_filename(attachment.filename)
            #attachment.filename
            data = attachment.stream.read()
            with open(attachment.filename.encode('utf-8'), "w") as f:
                f.write(data)
                f.close()
                ####Convertir a PDF
                try:
                    os.remove("/home/ubuntu/PDF/FastPrinterJob.pdf")
                except:
                    print "No hay archivo FastPrinter"
                attachment.filename = attachment.filename.replace(' ', '\ ')
                convertToPDF = "soffice --invisible -pt PDF %s" % attachment.filename.encode('utf-8')
                estado = subprocess.Popen([convertToPDF], stdout=subprocess.PIPE, shell=True)
                time.sleep(8) #Esperar 8 segundos para que termine de generar el pdf                                                                               
                for filename in os.listdir("/home/ubuntu/PDF/"):
                    os.rename("/home/ubuntu/PDF/%s"%filename, '/home/ubuntu/PDF/FastPrinterJob.pdf') 

                #if countPages(str(attachment.filename.encode('utf-8'))) <= 10:
                if countPages('/home/ubuntu/PDF/FastPrinterJob.pdf') <= 10:
                    print attachment.filename.encode('utf-8')
                    imprimiendo = subprocess.Popen(['python', 'rpc_client.py', str(name), '/home/ubuntu/PDF/FastPrinterJob.pdf',centros_auth[name]], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                    #imprimiendo = subprocess.Popen(['python', 'rpc_client.py', 'fib', '25', '10.8.0.101'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                    #EmailFunction(mailStriped)
                    out, err = imprimiendo.communicate()
                    print out, err            
                    if "Got 0" in str(out):
                        EmailFunction(mailStriped, 'impreso')
                    else:
                        EmailFunction(mailStriped, 'desconocido')
                        EmailFunction("info@fastprinter.co", 'desconocido')
                else:
                    EmailFunction(mailStriped, 'paginas')
                    EmailFunction("info@fastprinter.co", 'paginas')
        else:
            EmailFunction(mailStriped, 'tipo')
            EmailFunction("info@fastprinter.co", 'tipo')
    return "OK"

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10081, debug=True)
