
import PySimpleGUI as sg
from gui_constants import GuiLabel, GuiKey


sg.theme('DarkBlue')


layout = [
            [sg.Text('setting parametri CRaC', size=(41,1),font=('Arial',20),justification=('center'))],
                [sg.Frame(layout=([
                    [sg.Text('ip', size=(15,1),font=('Arial',9), key ='ip'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('port', size=(15,1),font=('Arial',9), key ='port'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('loopback_ip', size=(15,1),font=('Arial',9), key ='loopback_ip'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))]
                    ]),title='Setting server', font=('Arial',14), pad=(3, 0)),
                ],
                [sg.Frame(layout=([
                    [sg.Text('Longitude', size=(15,1),font=('Arial',9), key ='lon'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('Latitude', size=(15,1),font=('Arial',9), key ='lat'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('Height', size=(15,1),font=('Arial',9), key ='hight'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('Equinox', size=(15,1),font=('Arial',9), key='eqx'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))]
                    ]),title='Geography', font=('Arial',14), pad=(3, 0)),
                sg.Frame(layout=([
                    [sg.Text('loggingLevel', size=(15,1),font=('Arial',9), key ='loglev'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('sleep', size=(15,1),font=('Arial',9), key ='sleep'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('thesky_server', size=(15,1),font=('Arial',9), key ='tsky_server'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))]
                    ]),title='Automazione', font=('Arial',14), pad=(3, 0)),
                sg.Frame(layout=([
                    [sg.Text('Max secure alt', size=(15,1),font=('Arial',9), key ='max_sec_alt'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('Azimuth di park', size=(15,1),font=('Arial',9), key ='park_az'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('Altezza di park', size=(15,1),font=('Arial',9), key ='park_alt'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('Azimuth di flat', size=(15,1),font=('Arial',9), key ='flat_az'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('Altezza di flat', size=(15,1),font=('Arial',9), key ='flat_alt'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))]
                    ]),title='Telescope', font=('Arial',14), pad=(3, 0)),
                ],
                [sg.Frame(layout=([
                    [sg.Text('Azimuth NE', size=(15,1),font=('Arial',9), key ='AzNE'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('Azimuth SE', size=(15,1),font=('Arial',9), key ='AzSE'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('Azimuth SW', size=(15,1),font=('Arial',9), key ='AzSW'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('Azimuth NW', size=(15,1),font=('Arial',9), key ='AzNW'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))]
                    ]),title='Azimuth', font=('Arial',14), pad=(3, 0)),
                sg.Frame(layout=([
                    [sg.Text('Alt max East', size=(15,1),font=('Arial',9), key='max_est'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('Alt max West', size=(15,1),font=('Arial',9), key ='max_west'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('Alt min East', size=(15,1),font=('Arial',9), key ='park_est'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('Alt min West', size=(15,1),font=('Arial',9), key ='park_west'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('Angolo base tende', size=(15,1),font=('Arial',9), key ='alpha_min'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))]
                    ]),title='Tende', font=('Arial',14), pad=(3, 0)),
                sg.Frame(layout=([
                    [sg.Text('step/giro', size=(15,1),font=('Arial',9), key='n_step'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('step totali per corsa', size=(15,1),font=('Arial',9), key ='n_step_corsa'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('step max sicurezza', size=(15,1),font=('Arial',9), key ='n_step_sicurezza'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('delta_step_min_to_move', size=(15,1),font=('Arial',9), key ='diff_step'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('white'))]
                    ]),title='Encoders_step', font=('Arial',14), pad=(3, 0)),
                ],
                [sg.Frame(layout=([
                    [sg.Button("Read"), sg.Button("Write"), sg.Button('Exit')]
                    ]),title=''),
                ],
             ]


window = sg.Window('Setting CRaC -- Control Roof and Curtains by ARA', layout, grab_anywhere=False, finalize=True)

while True:  # Event Loop
    event, values = window.read()
    print (values[1])
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

window.close()
