#!/usr/bin/env python
#$ python rpc_server.py tipoDeMensajeAEscuchar
#$ python rpc_server.py fibonacci   #Para que escuche puro "Fibonacci"
import pika
import sys
import subprocess
import os
import threading

#Conexion de Rabbit
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

#Diferenciador de tipo directo
channel.exchange_declare(exchange="diferenciador", type='direct')

#Declaramos la cola
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

#Lee los tipos de mensaje que recibira (Severities)
severities = sys.argv[1:]
if not severities:
    print >> sys.stderr, "Usa: %s [fibonacci] [impresoraCasa] [impresoraEscuela]" % (sys.argv[0],)
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange='diferenciador', queue=queue_name, routing_key=severity)

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def func_imprimir(archivoAImprimir):
    estado = subprocess.Popen(["lpstat", "-p"], stdout=subprocess.PIPE)
    out, err = estado.communicate()
    if err is None:
        if "Ready to print" or "Lista para imprimir" in out:
            handle = file('duplicatedfile.pdf', 'wb')
            handle.write(archivoAImprimir)
            handle.close()
            #Path donde se va a duplicar el archivo (Donde se corre el programa)
            path = "/home/alfonso/Documentos/RabbitMQ/Programa/duplicatedfile.pdf"
            estado = subprocess.Popen(["lp", path], stdout=subprocess.PIPE)
            out, err = estado.communicate() #Verifico errores al mandar imprimir (otra vez)
            #t = threading.Timer(2.0, func_verificaEstado())
            imprimiendo = func_verificaEstado()
            while imprimiendo != 0:
                t = threading.Timer(2,0, func_verificaEstado())
                imprimiendo = func_verificaEstado()
                print "Estoy imprimiendo . . . " + str(imprimiendo)
            print "YA ESTA LISTA. MANDA OTRO"
            return(0)
        elif "inactiva" in out:
            print "ESPERA.. AUN NO.. VUELVE EN 2 SEGUNDOS.... "
            t=threading.Timer(2.0, func_imprimir).start()
        else:
            print "Sucede otra cosa pero no es error, espero que este imprimiendo"
    else:
        print err
        print "Ha ocurrido un error"
        print err

def func_verificaEstado():
    estado = subprocess.Popen(["lpstat", "-p"], stdout=subprocess.PIPE)
    out, err = estado.communicate()
    if "Lista" in out:
        return 0 #Ya esta lista para imprimir
    else:
        return 1 #Aun no esta lista



def on_request(ch, method, props, body):
    ################# PARA FIBONACCI ##############3
    #n = int(body) #Numero
    #print " [.] fib(%s)"  % (n,)
    #response = fib(n)

    ################ PARA IMPRESORA ##############
    archivo = body
    print " [.] TU archivo: (%s)"  % (archivo,)
    response = func_imprimir(archivo)

    #print "Metodo:%s, Channel:%s, props:%s" % (method, ch, props,)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue=queue_name)#, no_ack=True)

print " [x] Awaiting RPC requests"
channel.start_consuming()
