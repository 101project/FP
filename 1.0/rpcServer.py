#!/usr/bin/env python
import sys
import pika
import os
import threading
import subprocess

#Conexion para RABBITMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

#Variables a usar de os (TERMINAL)
estado = subprocess.Popen(["lpstat", "-p"], stdout=subprocess.PIPE)
out, err = estado.communicate()

#funcion para verificar estado de la impresora e imprimir si no hay error

def func_imprimir(archivoAImprimir):
    estado = subprocess.Popen(["lpstat", "-p"], stdout=subprocess.PIPE)
    out, err = estado.communicate()
    if err is None:
        if "Ready to print" or "Lista para imprimir" in out:
            handle = file('duplicatedfile.txt', 'wb')
            handle.write(archivoAImprimir)
            handle.close()
            path = "/home/alfonso/Documentos/RabbitMQ/Programa/duplicatedfile.txt"
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
    archivo = body
    print " [.] TU archivo: (%s)"  % (archivo,)
    response = func_imprimir(archivo)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print " [x] Awaiting RPC requests"
channel.start_consuming()
