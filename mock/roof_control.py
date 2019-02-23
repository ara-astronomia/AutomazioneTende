import config
from time import sleep
import time

timeout = 5

def verify_closed_roof(): #simula la condizione del fine corsa di chiusura
    status_c = 1
    return status_c

def verify_open_roof(): # simula la condizione del fine corsa di apertura
    status_o = 0
    return status_o

def open_roof():
    try:
        timeout_start = time.time()
        while True:
            time.sleep(1)
            if (timeout_start + timeout) > time.time() > timeout_start :
                status_roof = 'Tetto in fase di apertura'
                #status_o = 2
                print (status_roof)
            elif time.time() > (timeout_start + timeout):
                status_o = 0
                return status_o
    except:
        return -1

def closed_roof():
    try:
        timeout_start = time.time()
        while True:
            time.sleep(1)
            if (timeout_start + timeout) > time.time() > timeout_start:
                status_roof = 'Tetto in fase di chiusura'
                #status_o = 2
                print (status_roof)
            elif time.time() > (timeout_start + timeout):
                status_c = 1
                return status_c
    except:
        return -1

#open_roof()
