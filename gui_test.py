import PySimpleGUI as sg
import math #, config
from tkinter import *
#from logger import Logger
#import gpio_pin
#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BOARD)
from gui_constants import GuiLabel, GuiKey
#class Test:

sg.theme('Bluemono')
layout = [
                [sg.Menu([], tearoff=True)],
                [sg.Text('Test Hardware', size=(40, 1), justification='center', font=("Helvetica", 15))],
                [
                    sg.Frame(layout=([[
                        sg.Radio('Apri', "Roof"),
                        sg.Radio('Chiudi', "Roof"),
                    ]]), title="Comando tetto", title_color ="Black", border_width=5, pad=(3,0)),
                ],
                [
                    sg.Frame( layout=([[
                            sg.Frame(layout=([[
                                sg.Radio('Alza',"Curtain_West"),
                                sg.Radio('Abbassa',"Curtain_West"),
                                sg.Text('9999', key="Count_W",  size=(5, 1), justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,8),(0,0))),
                            ]]), title="Tenda West", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 8)),

                            sg.Frame(layout=([[
                                sg.Radio('Alza',"Curtain_Est"),
                                sg.Radio('Abbassa',"Curtain_Est"),

                                sg.Text('9999', key="Count_E",  size=(5, 1), justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,8),(0,0))),
                            ]]), title="TendaEst", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 5)),

                    ]]), title="Controllo Tende", title_color ="Black", border_width=5, pad=(2,10) )
                ],
                [
                    sg.Frame(layout=([[
                            sg.Frame(layout=([[
                                sg.Text('Aperta', key="Curtain_W_is_open",  size=(7, 1), justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,8),(1,5))),
                                sg.Text('Chiusa', key="Curtain_W_is_closed",  size=(7, 1), justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,3),(1,5))),
                            ]]), title="Tenda West", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 4)),
                            sg.Frame(layout=([[
                                sg.Text('Aperta', key="Curtain_E_is_open",  size=(7, 1), justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,8),(1,5))),
                                sg.Text('Chiusa', key="Curtain_E_is_closed",  size=(7, 1), justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,3),(1,5))),
                            ]]), title="Tenda Est", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 4)),
                            sg.Frame(layout=([[
                                sg.Text('Aperto', key="Roof_open",  size=(7, 1), justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,8),(1,5))),
                                sg.Text('Chiuso', key="Roof_closed",  size=(7, 1), justification='center',background_color="white",text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,3),(1,5))),
                            ]]), title="Tetto", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 4)),

                    ]]), title="Switchs", title_color ="Black", border_width=5, pad=(2,6)),
                ],
                ]

win=sg.Window('CRaC -- Control Roof and Curtains by ARA',default_element_size=(40, 1)).Layout(layout)
button, values = win.Read()
#sg.Popup(button, values)
