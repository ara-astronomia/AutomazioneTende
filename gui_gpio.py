import PySimpleGUI as sg
from gui_constants import GuiLabel, GuiKey


sg.theme('DarkBlue')


layout = [
            [sg.Text('SETTING GPIO', size=(41,1),font=('Arial',20),justification=('center'))],
                [sg.Frame(layout=([
                    [sg.Text('clk_e', size=(20,1),font=('Arial',9), key ='clk_e'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('dt_e', size=(20,1),font=('Arial',9), key ='dt_e'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('clk_w', size=(20,1),font=('Arial',9), key ='clk_w'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('dt_w', size=(20,1),font=('Arial',9), key ='dt_w'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))]
                    ]),title='Encoder Board', font=('Arial',14), pad=(3, 0)),
                ],
                [sg.Frame(layout=([
                    [sg.Text('motorE_A', size=(20,1),font=('Arial',9), key ='motorE_A'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('motorE_B', size=(20,1),font=('Arial',9), key ='motorE_B'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('motorE_E', size=(20,1),font=('Arial',9), key ='motorE_E'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('motorW_A', size=(20,1),font=('Arial',9), key='motorW_A'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('motorW_B', size=(20,1),font=('Arial',9), key='motorW_B'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('motorW_E', size=(20,1),font=('Arial',9), key='motorW_E'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))]
                    ]),title='Motors Board', font=('Arial',14), pad=(3, 0)),
                sg.Frame(layout=([
                    [sg.Text('switch_panel', size=(20,1),font=('Arial',9), key ='switch_panel'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('switch_power', size=(20,1),font=('Arial',9), key ='switch_power'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('switch_light', size=(20,1),font=('Arial',9), key ='switch_light'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('switch_aux', size=(20,1),font=('Arial',9), key ='switch_aux'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))]
                    ]),title='Panel Board', font=('Arial',14), pad=(3, 0)),
                ],
                [sg.Frame(layout=([
                    [sg.Text('roof_verify_closed', size=(20,1),font=('Arial',9), key ='roof_ver_closed'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('roof_verify_open', size=(20,1),font=('Arial',9), key ='roof_ver_open'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('switch_roof', size=(20,1),font=('Arial',9), key ='switch_roof'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('wait_for_timeout', size=(20,1),font=('Arial',9), key ='wait_timeout'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('event_bouncetime', size=(20,1),font=('Arial',9), key ='bouncetime'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))]
                    ]),title='Roof Board', font=('Arial',14), pad=(3, 0)),
                sg.Frame(layout=([
                    [sg.Text('curtain_W_verify_open', size=(20,1),font=('Arial',9), key ='w_ver_open'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('curtain_W_verify_closed', size=(20,1),font=('Arial',9), key ='w_ver_close'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('curtain_E_verify_open', size=(20,1),font=('Arial',9), key ='e_ver_open'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))],
                    [sg.Text('curtain_E_verify_closed', size=(20,1),font=('Arial',9), key ='e_ver_close'),sg.InputText('', size=(10,1), font=('Arial',9), text_color=('white'))]
                    ]),title='Curtains Limits Switch', font=('Arial',14), pad=(3, 0)),
                ],
                [sg.Frame(layout=([
                    [sg.Button("Read"), sg.Button("Write"), sg.Button('Exit')]
                    ]),title=''),
                ],
            ]

window = sg.Window ('Setting CRaC -- Control Roof and Curtains by ARA', layout, grab_anywhere=False, finalize=True)

while True:  # Event Loop
    event, values = window.read()
    print (values[1])
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

window.close()
