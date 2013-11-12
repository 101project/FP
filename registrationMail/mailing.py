from flaskext.mail import Message
...

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

def send_awaiting_confirm_mail(user):
    """
    Send the awaiting for confirmation mail to the user.
    """
    subject = "We're waiting for your confirmation!!"
    mail_to_be_sent = Message(subject=subject, recipients=[user['email']])
    confirmation_url = url_for('activate_user', user_id=user['_id'],
_external=True)
    mail_to_be_sent.body = "Dear %s, click here to confirm: %s" %
(user['email'], confirmation_url)
    from *<my_main_package>* import mail
    mail.send(mail_to_be_sent)
