#!/usr/bin/env python
# Archivo para parsear mails recibidos.

def on_incoming_message(request):
    if request.method == 'POST':
        sender    = request.POST.get('sender')
        recipient = request.POST.get('recipient')
        subject   = request.POST.get('subject', '')

        body_plain = request.POST.get('body-plain', '')
        body_without_quotes = request.POST.get('stripped-text', '')
        # note: other MIME headers are also posted here...

         # attachments:
        for key in request.FILES:
            file = request.FILES[key]
            print "SE HA RECIBIDO UN ARCHIVO LLAMADO " + file
             # do something with the file

     # Returned text is ignored but HTTP status code matters:
     # Mailgun wants to see 2xx, otherwise it will make another attempt in 5 minutes
    return HttpResponse('OK')
