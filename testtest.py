import PySimpleGUI as sg
import math, config
from graphics import *
from tkinter import *
from logger import Logger
#import gpio_pin
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

class Test:
    def __init__(self):
        self.pins = []
        self.pins.append({"pin": config.Config.getInt('curtain_W_verify_open', 'curtains_limit_switch'), "element": "Curtain_West_Open", "button": "open-curtain-W"})
        self.pins.append({"pin": config.Config.getInt('curtain_W_verify_closed','curtains_limit_switch'), "element": "Curtain_West_Closed", "button": "close-curtain-W"})
        self.pins.append({"pin": config.Config.getInt('curtain_E_verify_open', 'curtains_limit_switch'), "element": "Curtain_East_Open", "button": "open-curtain-E"})
        self.pins.append({"pin": config.Config.getInt('curtain_E_verify_closed', 'curtains_limit_switch'), "element": "Curtain_East_Closed", "button": "close-curtain-E"})
        self.pins.append({"pin": config.Config.getInt('roof_verify_open', 'roof_board'), "element": "Roof_Open", "button": "open-roof"})
        self.pins.append({"pin": config.Config.getInt('roof_verify_closed', 'roof_board'), "element": "Roof_Closed", "button": "close-roof"})

        for pin in self.pins:
            GPIO.setup(pin["pin"], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        sg.ChangeLookAndFeel('Dark Blue')
        n=(20,1)
        b=(20,1)

        layout = [
            [sg.Text('Test hardware', size=(20, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
            [sg.Text("guida breve", justification = 'center', font=("Helvetica", 14), size =(38,1), relief=sg.RELIEF_RIDGE)],
            [sg.Text("cliccare nella finestra control l'hardware che si vuole testare.                                                                 Nella finestra di ceck saranno visualizzati i risultati", font=("Helvetica", 12),size=(40,3))],

            [sg.Frame(layout=[
            [sg.Button('Open Roof', key = 'open-roof',size=b),sg.Button('Close Roof', key = 'close-roof',size=b)],
            [sg.Button('Open Curtain West', key= 'open-curtain-W',size=n),sg.Button('Close Curtain West', key='close-curtain-W',size=n)],
            [sg.Button('Open Curtain East', key='open-curtain-E',size=n),sg.Button('Close Curtain East', key='close-curtain-E', size=n)]],
            title='Test Roof',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='clicca per attivare')],


            [sg.Frame(layout=[
            [sg.Checkbox('Roof_Open', default = False, key ='Roof_open', size=n),  sg.Checkbox('Roof_Closed', default=False, key ='Roof_closed', size=n)],
            [sg.Checkbox('Curtain West Open', default = False, key = 'Curtain_West_Open', size=n),  sg.Checkbox('Curtain West Closed', default=False, key = 'Curtain_West_Closed',size=n)],
            [sg.Checkbox('Curtain East_Open', default = False, key = 'Curtain_East_Open', size=n),  sg.Checkbox('Curtain East Closed', default=False, key = 'Curtain_East_Closed', size=n)]],
            title='Switch Status',title_color='red', element_justification = 'left', relief=sg.RELIEF_SUNKEN, tooltip='leggi lo status dell switch')],

            [sg.Text('tenda E posizione raggiunta per apertura 70°' , size=(38,1), justification='center', font=("Arial", 8), relief=sg.RELIEF_RIDGE, tooltip=('il valore corretto max apertura è 70°')),
            sg.InputText('  ' , size=(3, 1), justification='left', font=("Arial", 8),  key ='apert_e')],
            [sg.Text('tenda W posizione raggiunta per apertura 70°', size=(38, 1), justification='center', font=("Arial", 8), relief=sg.RELIEF_RIDGE, tooltip=('il valore corretto max apertura è 70°')),
            sg.InputText('  ' , size=(3, 1), justification='left', font=("Arial", 8),  key ='apert_w')],

            [sg.Frame(layout=[
            [sg.Button('exit', key ='Quit')]],
            title='Control',title_color='red', relief=sg.RELIEF_FLAT, tooltip='clicca per attivare')]]


        self.window = sg.Window('CRaC -- Control Roof and Curtains by ARA', layout, default_element_size=(40, 1), grab_anywhere=False)
        while True:
            event, values = self.window.read()
            # INSERIRE I COLLEGAMENTI AGLI ALTRI METODI, PER COMANDI E RETURN
            # VEDERE FILE gui.py . config, client.py, server.py
            for pin in self.pins:
                if event == pin["button"]:
                    self.test_pin(pin)
                    break

    def test_pin(self, pin):
        GPIO.output(pin["pin"], not GPIO.input(pin["pin"]))
        status = True if GPIO.input(pin["pin"]) == GPIO.LOW else False
        self.window.FindElement(pin["element"]).Update(status)

'''
            if event == 'open-roof':
                # attiva pin open roof
                window.FindElement('Roof_open').Update(True)

            if event == 'close-roof':
                window.FindElement('Roof_closed').Update(True)
                # disattiva pin open roof

            if event == 'open-curtain-W':

                #attiva mnotore tenda w in open, leggere status pin necessario
                window.FindElement('Curtain _West_Open').Update(True)

                #resta in ascolto fintanto che il pin dell
                update_curtains_w_text()
                window.FindElement('Curtain _West_Open').Update(True)

            if event == 'close-curtain-W':
                window.FindElement('Curtain _West_Closed').Update(True)
                window.FindElement('Curtain _West_Open').Update(True)
            if event == 'open-curtain-E':
                window.FindElement('Curtain _East_Open').Update(True)
            if event == 'close-curtain-E':
                window.FindElement('Curtain _East_Closed').Update(True)
            if event == 'Quit':
                window.close()
            #break

        def update_curtains_w_text(self, e_w):

            """Update valori angolari tende"""
            print(e_w)
            alpha_w = int(e_w*float("{0:.3f}".format(self.increm_w))) # trasformazione posizione step in gradi
            self.win.FindElement('apert_w').Update(alpha_w)
            return alpha_w

        def update_curtains_e_text(self, e_e):

            """Update valori angolari tende"""
            print(e_e)
            alpha_e = int(e_e*float("{0:.3f}".format(self.increm_e))) # trasformazione posizione step in gradi
            self.win.FindElement('apert_e').Update(alpha_e)
            return alpha_w
'''
#event, values = window.Read()
#print(event)
#window.close()
#[sg.Radio('Open Roof', "Roof", default= False, key = 'open_roof',size=n),sg.Radio('Close Roof', "Roof", key = "close_roof",default = False, size =n)],



    #return alpha_e, alpha_w
