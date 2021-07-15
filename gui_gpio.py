
import PySimpleGUI as sg
from gui_constants import GuiLabel, GuiKey


sg.theme('Dark Brown')


layout = [
            [sg.Text('setting parametri CRaC', size=(41,1),font=('Arial',20),justification=('center'))],
                [sg.Frame(layout=([
                    [sg.Text('clk_e', size=(15,1),font=('Arial',9)),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('dt_e', size=(15,1),font=('Arial',9)),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('clk_w', size=(15,1),font=('Arial',9)),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('dt_w', size=(15,1),font=('Arial',9)),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))]
                    ]),title='Encoder Board', font=('Arial',14), pad=(3, 0)),
                [sg.Frame(layout=([
                    [sg.Text('motorE_A', size=(15,1),font=('Arial',9), key ='lon'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('motorE_B', size=(15,1),font=('Arial',9), key ='lat'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('motorE_E', size=(15,1),font=('Arial',9), key ='hight'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('motorW_A', size=(15,1),font=('Arial',9), key='ut'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('motorW_B', size=(15,1),font=('Arial',9), key='dayl'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('motorW_E', size=(15,1),font=('Arial',9), key='eqx'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))]
                    ]),title='Motors Board', font=('Arial',14), pad=(3, 0)),
                sg.Frame(layout=([
                    [sg.Text('switch_panel', size=(15,1),font=('Arial',9), key ='max_sec_alt'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('switch_power', size=(15,1),font=('Arial',9), key ='park_az'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('switch_light', size=(15,1),font=('Arial',9), key ='park_alt'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('switch_aux', size=(15,1),font=('Arial',9), key ='flat_az'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))]
                    ]),title='Panel Board', font=('Arial',14), pad=(3, 0)),
                ],
                [sg.Frame(layout=([
                    [sg.Text('roof_verify_closed', size=(15,1),font=('Arial',9), key ='Az_NE'),sg.InputText('fsaff', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('roof_verify_open', size=(15,1),font=('Arial',9), key ='Az_SE'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('switch_roof', size=(15,1),font=('Arial',9), key ='Az_SW'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('wait_for_timeout', size=(15,1),font=('Arial',9), key ='Az_NW'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))]
                    ]),title='event_bouncetime', font=('Arial',14), pad=(3, 0)),
                sg.Frame(layout=([
                    [sg.Text('curtain_W_verify_open', size=(15,1),font=('Arial',9)),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('curtain_W_verify_closed', size=(15,1),font=('Arial',9), key ='max_step'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('curtain_E_verify_open', size=(15,1),font=('Arial',9), key ='max_secure_step'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))],
                    [sg.Text('curtain_E_verify_closed', size=(15,1),font=('Arial',9), key ='min_step'),sg.InputText('', size=(25,1), font=('Arial',9), text_color=('black'))]
                    ]),title=' Curtains Limits Switch', font=('Arial',14), pad=(3, 0)),
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
