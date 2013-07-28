from flask import Flask
from flask import request
import FP/rpc_client.py
app = Flask(__name__)

@app.route('/hola')
def hello_world():
    return 'Hola a todos desde python!!'

@app.route("/", methods=["POST", "GET"])
def mailin():
    # see if the message is spam:
    # is_spam = request.form['X-Mailgun-SFlag'] == 'Yes'
    
    # # access some of the email parsed values:
    request.form['From']
    request.form['To']
    request.form['subject']
 
    # # stripped text does not include the original (quoted) message, only what
    # # a user has typed:
    request.form['stripped-text']
    request.form['stripped-signature']
 
    # # enumerate through all attachments in the message and save
    # # them to disk with their original filenames:
    for attachment in request.files.values():
        attachment.filename
        data = attachment.stream.read()
        with open(attachment.filename, "w") as f:
        #with open(request.form['subject'], "w") as f:
            f.write(data)
            print str(request.form['subject'])
            print str(request.form['To'])
#            f.write(str(request.form['To']))
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10081)
