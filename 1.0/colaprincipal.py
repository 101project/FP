# -*- coding: utf-8 -*- 
# AsyncNotifier example from tutorial
#
# See: http://github.com/seb-m/pyinotify/wiki/Tutorial

import asyncore
import pyinotify
import hilosprueba

wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        #print "Creating:", event.pathname
        t = hilosprueba.MiThread(event.pathname)
        t.start()
        if t is not None:
            print t
        #else:
            #print ut, "error", err

    #def process_IN_DELETE(self, event):
        #print "Removing:", event.pathname

notifier = pyinotify.AsyncNotifier(wm, EventHandler())
#wdd = wm.add_watch('/home/user/Documents/code/notifier', mask, rec=True)
wdd = wm.add_watch('/home/alfonso/Documentos/RabbitMQ/Programa', mask, rec=True)

asyncore.loop()
