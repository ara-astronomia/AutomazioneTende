
import PySimpleGUI as sg
from gui_constants import GuiLabel, GuiKey


sg.theme('Dark Brown')


layout = [
            [sg.Text('setting parametri CRaC', size=(41,1),font=('Arial',20),justification=('center'))],
                [sg.Frame(layout=([
                    [sg.Text('server', size=(15,1),font=('Arial',9)),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('port', size=(15,1),font=('Arial',9)),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))]
                    ]),title='Setting server', font=('Arial',14), pad=(3, 0)),
                ],
                [sg.Frame(layout=([
                    [sg.Text('Longitude', size=(15,1),font=('Arial',9), key ='lon'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('Latitude', size=(15,1),font=('Arial',9), key ='lat'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('Height', size=(15,1),font=('Arial',9), key ='hight'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('fuso oraio', size=(15,1),font=('Arial',9), key='ut'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('daylight', size=(15,1),font=('Arial',9), key='dayl'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('equinox', size=(15,1),font=('Arial',9), key='eqx'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))]
                    ]),title='Geographic', font=('Arial',14), pad=(3, 0)),
                sg.Frame(layout=([
                    [sg.Text('Max secure alt', size=(15,1),font=('Arial',9), key ='max_sec_alt'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('Azimuth di park', size=(15,1),font=('Arial',9), key ='park_az'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('Altezza di park', size=(15,1),font=('Arial',9), key ='park_alt'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('Azimuth di flat', size=(15,1),font=('Arial',9), key ='flat_az'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('Altezza di flat', size=(15,1),font=('Arial',9), key ='flat_alt'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))]
                    ]),title='Telescope', font=('Arial',14), pad=(3, 0)),
                ],
                [sg.Frame(layout=([
                    [sg.Text('Azimuth NE', size=(15,1),font=('Arial',9), key ='Az_NE'),sg.InputText('fsaff', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('Azimuth SE', size=(15,1),font=('Arial',9), key ='Az_SE'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('Azimuth SW', size=(15,1),font=('Arial',9), key ='Az_SW'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('Azimuth NW', size=(15,1),font=('Arial',9), key ='Az_NW'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))]
                    ]),title='Curtains', font=('Arial',14), pad=(3, 0)),
                sg.Frame(layout=([
                    [sg.Text('step/giro', size=(15,1),font=('Arial',9)),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('step totali per corsa', size=(15,1),font=('Arial',9), key ='max_step'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('step max sicurezza', size=(15,1),font=('Arial',9), key ='max_secure_step'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('mod count step', size=(15,1),font=('Arial',9), key ='mod_count_step'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('step min  intervento', size=(15,1),font=('Arial',9), key ='min_step'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))]
                    ]),title='Encoders', font=('Arial',14), pad=(3, 0)),
                ],
                [[sg.Button(Ok)],
                [sg.Button('Exit')]],
             ]

        #[sg.Listbox(values=sg.theme_list(), size=(20, 15), key='-LIST-', enable_events=True)],
        #[sg.Button('Ok')]]

window = sg.Window('Setting CRaC', layout, grab_anywhere=False, finalize=True)

while True:  # Event Loop
    event, values = window.read()
    print (values[1])
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

window.close()
