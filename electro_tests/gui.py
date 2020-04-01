import PySimpleGUI as sg

def create_win():
    sg.theme('Bluemono')
    layout = [
        [sg.Menu([], tearoff=True)],
        [sg.Text('Test Hardware', size=(54, 1), justification='center', font=("Helvetica", 15))],
        [
            sg.Frame(layout=([[
                sg.Radio('Apri', "Roof", key="RO"),
                sg.Radio('Chiudi', "Roof", key="RC"),
            ]]), title="Comando tetto", title_location=sg.TITLE_LOCATION_TOP, title_color ="Black", pad=(3,0)),
        ],
        [
            sg.Frame(layout=([[
                sg.Radio('Alza', "Curtain_West", default=False, key="WO"),
                sg.Radio('Abbassa', "Curtain_West", default=False, key="WC"),
                sg.Radio('Stop', "Curtain_West", default=True, key="WS"),
                sg.Text('stand-by', key="Count_W",  size=(7, 1), relief=sg.RELIEF_SUNKEN, justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 9), pad=((3,8),(0,0))),
            ]]), title="Tenda West", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 5)),
            sg.Frame(layout=([[
                sg.Radio('Alza', "Curtain_Est", default=False, key="EO"),
                sg.Radio('Abbassa', "Curtain_Est", default=False, key="EC"),
                sg.Radio('Stop', "Curtain_Est", default=True, key="ES"),
                sg.Text('stand-by', key="Count_E",  size=(7, 1), relief=sg.RELIEF_SUNKEN, justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 9), pad=((3,8),(0,0))),
            ]]), title="Tenda Est", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 8)),
        ],
        [
            sg.Frame(layout=([[
                    sg.Frame(layout=([[
                        sg.Text('stand-by', key="Curtain_W_is_open",  size=(7, 1),relief=sg.RELIEF_SUNKEN,  justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 9), pad=((3,8),(1,5))),
                        sg.Text('stand-by', key="Curtain_W_is_closed",  size=(7, 1),relief=sg.RELIEF_SUNKEN,  justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 9), pad=((3,3),(1,5))),
                    ]]), title="Tenda West", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 4)),
                    sg.Frame(layout=([[
                        sg.Text('stand-by', key="Curtain_E_is_open",  size=(7, 1), relief=sg.RELIEF_SUNKEN, justification='center', background_color="white", text_color = 'DarkBlue', font=("Helvetica", 9), pad=((3,8),(1,5))),
                        sg.Text('stand-by', key="Curtain_E_is_closed",  size=(7, 1), relief=sg.RELIEF_SUNKEN, justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 9), pad=((3,3),(1,5))),
                    ]]), title="Tenda Est", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 4)),
                    sg.Frame(layout=([[
                        sg.Text('stand-by', key="Roof_open",  size=(7, 1), relief=sg.RELIEF_SUNKEN, justification='center',background_color="white", text_color = 'DarkBlue', font=("Helvetica", 9), pad=((3,8),(1,5))),
                        sg.Text('stand-by', key="Roof_closed",  size=(7, 1), relief=sg.RELIEF_SUNKEN, justification='center',background_color="white",text_color = 'DarkBlue', font=("Helvetica", 9), pad=((3,3),(1,5))),
                    ]]), title="Tetto", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 4)),

            ]]), title="Switches", title_color ="Black", title_location=sg.TITLE_LOCATION_TOP, pad=(2,6)),
        ],
    ]


    win=sg.Window('CRaC -- Control Roof and Curtains by ARA',default_element_size=(40, 1)).Layout(layout)
    return win
