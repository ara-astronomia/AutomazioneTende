import config
from time import sleep
import time

timeout = 5

def verify_closed_roof(): #simula la condizione del fine corsa di chiusura
    status_c = 1
    status_roof = 'Tetto chiuso'
    return status_c, status_roof
    sleep(config.Config.getFloat("sleep"))

def verify_open_roof(): # simula la condizione del fine corsa di apertura
    status_o = 0
    status_roof = 'Tetto Aperto'
    return status_o, status_roof
    
    sleep(config.Config.getFloat("sleep"))

def open_roof():
    timeout_start = time.time()
    while True: 
        time.sleep(1)
        if (timeout_start + timeout) > time.time() > timeout_start :
            status_roof = 'Tetto in fase di apertura'
            #status_o = 2
            print (status_roof)
            continue
            
        if time.time() > (timeout_start + timeout):
            status_o = 0
            status_roof = 'Tetto Aperto'
            return status_o, status_roof
            sleep(config.Config.getFloat("sleep"))
            
def closed_roof():
  timeout_start = time.time()
  while True: 
        time.sleep(1)
        if (timeout_start + timeout) > time.time() > timeout_start:
            status_roof = 'Tetto in fase di chiusura'
            #status_o = 2
            print (status_roof)
            continue
            
            
        if time.time() > (timeout_start + timeout):
            status_c = 1
            status_roof = 'Tetto chiuso'
            return status_c, status_roof
            sleep(config.Config.getFloat("sleep"))        

#open_roof()