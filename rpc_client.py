#!/usr/bin/env python
#$ python rpc_client.py tipoDeMensajeAEnviar(TEMA) Mensaje ip
#$ python rpc_client.py fibonacci 30 192.168.1.106

import pika
import uuid
import sys
import os

class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(sys.argv[3])))

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='diferenciador', type='direct')
        self.severity = sys.argv[1] if len(sys.argv) > 1 else 'default'
        self.message = ' '.join(sys.argv[2:]) or "Este es un mje default"
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)
#respuesta que se manda al server
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, cuerpo, severity):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='diferenciador',
                                   routing_key=severity,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(cuerpo))
                                   #body=cuerpo.read()) #para archivo
        print "El tema es:%s" % (str(self.severity))
        print "El numero es:%d" % (int(cuerpo))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

tema = sys.argv[1]
cuerpo = sys.argv[2]

if len(sys.argv) > 1:
    #mando llamar el call enviando el body y el severity
    ####PARA FIBONACCI####
    print " [x] Requesting Severity:%s Body:fib(%d)" % (str(tema), int(cuerpo))
    response = fibonacci_rpc.call(int(cuerpo), str(tema)) #Para fib

    ####PARA ARCHIVOS####
    #archivoAImprimir = open(cuerpo, 'rb')
    #response = fibonacci_rpc.call(archivoAImprimir, str(tema))
    #archivoAImprimir.close()

else: #En caso de que no se haya mandado severity ni archivo
    print " [x] Requesting Sev... No has enviado nada... utiliza: \n $ python rpc_client [Cuerpo] [Tema]"
    sys.exit(1)
    #response = fibonacci_rpc.call(1, "default")
#mando llamar fubonacci, primer parametro es el body. seg severity
print " [.] Got %r" % (response,)
