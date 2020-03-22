import PySimpleGUI as sg
import math #, config
#from graphics import *
from tkinter import *
#from logger import Logger
#import gpio_pin
#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BOARD)

#class Test:

sg.theme('DarkBlue')
layout = [
                [sg.Menu([], tearoff=True)],
                [sg.Text('Test Hardware Crac', size=(40, 1), justification='center', font=("Helvetica", 15))],
                [
                    sg.Frame(layout=([[
                        sg.Button('Apri', key="GuiKey.OPEN_ROOF", disabled=False, size=(10, 1)),
                        sg.Button('Chiudi', key="GuiKey.CLOSE_ROOF", disabled=False, size=(10, 1))
                    ]]), title="Comando tetto", title_color ="red", border_width=5, pad=(3,0)),
                ],
                [
                    sg.Frame(layout=([[
                            sg.Frame(layout=([[
                                sg.Text('Open', key="Curtain_W_is_open",  size=(7, 1), justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,8),(1,5))),
                                sg.Text('Closed', key="Curtain_W_is_closed",  size=(7, 1), justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,3),(1,5))),
                            ]]), title="Tenda West", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 4)),
                            sg.Frame(layout=([[
                                sg.Text('Open', key="Curtain_E_is_open",  size=(7, 1), justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,8),(1,5))),
                                sg.Text('Closed', key="Curtain_E_is_closed",  size=(7, 1), justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,3),(1,5))),
                            ]]), title="Tenda Est", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 4)),
                            sg.Frame(layout=([[
                                sg.Text('Open', key="Roof_open",  size=(7, 1), justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,8),(1,5))),
                                sg.Text('Closed', key="Roof_closed",  size=(7, 1), justification='center',background_color="white",text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,3),(1,5))),
                            ]]), title="Tetto", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 4)),

                    ]]), title="Switchs", title_color ="red", border_width=5, pad=(2,6)),

                ],

                [
                    sg.Frame( layout=([[
                            sg.Frame(layout=([[
                                sg.Radio('Open',"Curtain_West"),
                                sg.Radio('Closed',"Curtain_West"),
                                sg.Text('9999', key="Count_W",  size=(5, 1), justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,8),(0,0))),
                            ]]), title="Tenda West", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 8)),

                            sg.Frame(layout=([[
                                sg.Radio('Open',"Curtain_Est"),
                                sg.Radio('Closed',"Curtain_Est"),

                                sg.Text('9999', key="Count_E",  size=(5, 1), justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 10), pad=((3,8),(0,0))),
                            ]]), title="TendaEst", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 5)),

                    ]]), title="Controllo Tende", title_color ="red", border_width=5, pad=(2,10) )
                ],
                ]

win=sg.Window('CRaC -- Control Roof and Curtains by ARA',default_element_size=(40, 1)).Layout(layout)
button, values = win.Read()
#sg.Popup(button, values)
