
# coding: utf-8

# # PythonによるSocket通信

# In[3]:

import sys
from bb2d import BinaryBoundary2D
from bb2dScript import GetBoundary

# ## Threadあり

# In[ ]:

import socket
import threading
import socketserver
import time
import logging
import logging.handlers
import time


def myNamer(name):
    return name+".log"

def log_setup():
    formatter = logging.Formatter(
        "%(asctime)s:%(message)s",
        '%y %b %d %H:%M:%S')
    log_handler = logging.handlers.RotatingFileHandler(filename="serverLog",mode='a',maxBytes=10000000,backupCount=10,encoding='utf-8')
    log_handler.setFormatter(formatter)
    log_handler.namer = myNamer
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)

log_setup()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        start = time.time() 

        currentThread = threading.current_thread()
        try:
            currentThread = threading.current_thread()
            print("thread:",currentThread.name)
            self.data = b''        
            for i in range(1000):
                recieved = self.request.recv(256)
                #print("recieved:",recieved)
                if len(recieved)==0:break
                self.data += recieved        
            txt = self.data.decode('utf-8')
            result = GetBoundary(txt,currentThread.name)
            #logging.debug(result)
            self.request.sendall(result.encode())
            logging.debug("data sent.")

            end = time.time()
            logging.debug(currentThread.name+":Calc Time - "+str(end-start)+"[s]")
        except Exception as ex:
            logging.debug(currentThread.name +" Error:")
            logging.exception("")
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":

    HOST, PORT = "localhost", 13000

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    with server:
        ip, port = server.server_address

        server_thread = threading.Thread(target=server.serve_forever)

        server_thread.daemon = False

        try:    
            server_thread.start()

            logging.debug("Server Start")
            logging.debug(ip+":"+str(port))

            input()

        except Exception as e:
            logging.exception("")
        finally:
            server.shutdown()
            logging.debug("Server Shutdown")
            



