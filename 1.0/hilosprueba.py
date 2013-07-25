#!/usr/bin/env python                                                   
# -*- coding: utf-8 -*- 

import threading
import time
import random
import subprocess

class MiThread(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print "Mando imprimir", self.name
        imprimir = subprocess.Popen(["python", "rpcCliente.py",
        self.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = imprimir.communicate()
        if err is None:
            return out
        else:
            return err
        #time.sleep(1)
        #for i in range (0,5):
            #time.sleep(random.randint(0,10))
            #print "numero", i,  "en el thread de ", self.name

#print "soy el hilo principal"

#for i in range (0,4):
 #   t = MiThread(i)
  #  t.start()
    #t.join()


