import PySimpleGUI as sg
from logger import Logger
from gui_constants import GuiLabel, GuiKey


def create_win():
    sg.theme('Bluemono')
    layout = [
        [sg.Menu([], tearoff=True)],
        [sg.Text('Test Hardware', size=(54, 1), justification='center', font=("Helvetica", 15))],
        [
            sg.Frame(layout=([[
                sg.Radio('Apri', "Roof", key="RO"),
                sg.Radio('Chiudi', "Roof", key="RC"),
            ]]), title="Comando tetto", title_location=sg.TITLE_LOCATION_TOP, title_color="Black", pad=(3, 0)),
        ],
        [
            sg.Frame(layout=([[
                sg.Radio('Alza', "Curtain_West", default=False, key="WO"),
                sg.Radio('Abbassa', "Curtain_West", default=False, key="WC"),
                sg.Radio('Stop', "Curtain_West", default=True, key="WS"),
                sg.Text(GuiLabel.STAND_BY, key="Count_W",  size=(7, 1), relief=sg.RELIEF_SUNKEN, justification='center', background_color="white", text_color='DarkBlue', font=("Helvetica", 9), pad=((3, 8), (0, 0))),
            ]]), title="Tenda West", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 5)),
            sg.Frame(layout=([[
                sg.Radio('Alza', "Curtain_Est", default=False, key="EO"),
                sg.Radio('Abbassa', "Curtain_Est", default=False, key="EC"),
                sg.Radio('Stop', "Curtain_Est", default=True, key="ES"),
                sg.Text(GuiLabel.STAND_BY, key="Count_E",  size=(7, 1), relief=sg.RELIEF_SUNKEN, justification='center', background_color="white", text_color='DarkBlue', font=("Helvetica", 9), pad=((3, 8), (0, 0))),
            ]]), title="Tenda Est", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 8)),
        ],
        [
            sg.Frame(layout=([[
                    sg.Frame(layout=([[
                        sg.Text(GuiLabel.STAND_BY, key="Curtain_W_is_open", size=(7, 1), relief=sg.RELIEF_SUNKEN,  justification='center', background_color="white", text_color='DarkBlue', font=("Helvetica", 9), pad=((3, 8), (1, 5))),
                        sg.Text(GuiLabel.STAND_BY, key="Curtain_W_is_closed", size=(7, 1), relief=sg.RELIEF_SUNKEN,  justification='center', background_color="white", text_color='DarkBlue', font=("Helvetica", 9), pad=((3, 3), (1, 5))),
                    ]]), title="Tenda West", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 4)),
                    sg.Frame(layout=([[
                        sg.Text(GuiLabel.STAND_BY, key="Curtain_E_is_open", size=(7, 1), relief=sg.RELIEF_SUNKEN, justification='center', background_color="white", text_color='DarkBlue', font=("Helvetica", 9), pad=((3, 8), (1, 5))),
                        sg.Text(GuiLabel.STAND_BY, key="Curtain_E_is_closed", size=(7, 1), relief=sg.RELIEF_SUNKEN, justification='center', background_color="white", text_color'DarkBlue', font=("Helvetica", 9), pad=((3, 3), (1, 5))),
                    ]]), title="Tenda Est", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 4)),
                    sg.Frame(layout=([[
                        sg.Text(GuiLabel.STAND_BY, key="Roof_open", size=(7, 1), relief=sg.RELIEF_SUNKEN, justification='center', background_color="white", text_color='DarkBlue', font=("Helvetica", 9), pad=((3, 8), (1, 5))),
                        sg.Text(GuiLabel.STAND_BY, key="Roof_closed", size=(7, 1), relief=sg.RELIEF_SUNKEN, justification='center', background_color="white", text_color='DarkBlue', font=("Helvetica", 9), pad=((3, 3), (1, 5))),
                    ]]), title="Tetto", title_location=sg.TITLE_LOCATION_TOP, pad=(3, 4)),

            ]]), title="Switches", title_color="Black", title_location=sg.TITLE_LOCATION_TOP, pad=(2, 6))
        ],
        [
            sg.Frame(layout=([[
                sg.Button(GuiLabel.ON, key=GuiKey.PANEL_ON, disabled=True, size=(4, 1), tooltip="accensione pannnello del flat"),
                sg.Button(GuiLabel.OFF, key=GuiKey.PANEL_OFF, disabled=True, size=(4, 1), button_color=["black", "red"], tooltip="spegnimento pannello flat")
            ]]), title="Panel Flat", pad=(3, 10)),
            sg.Frame(layout=([[
                sg.Button(GuiLabel.ON, key=GuiKey.POWER_ON, disabled=False, size=(4, 1), tooltip="accensione alimentarori"),
                sg.Button(GuiLabel.OFF, key=GuiKey.POWER_OFF, disabled=True, size=(4, 1), button_color=["black", "red"], tooltip="spegnimento alimentatori"),
            ]]), title="Power Switch", pad=(3, 10)),
            sg.Frame(layout=([[
                sg.Button(GuiLabel.ON, key=GuiKey.LIGHT_ON, disabled=False, size=(4, 1), tooltip="accensioni luci cupola, controllare se i telescopio è in fase di ripresa"),
                sg.Button(GuiLabel.OFF, key=GuiKey.LIGHT_OFF, disabled=True, size=(4, 1), button_color=["black", "red"], tooltip="spegnimento luci cupola"),
            ]]), title="Light Dome", pad=(3, 10)),
            sg.Frame(layout=([[
                sg.Button(GuiLabel.ON, key=GuiKey.AUX_ON, disabled=False, size=(4, 1), tooltip="nessuna strumentazione ausiliare implementata"),
                sg.Button(GuiLabel.OFF, key=GuiKey.AUX_OFF, disabled=True, size=(4, 1), button_color=["black", "red"], tooltip="nessuna strumentazione ausiliare implementata"),
            ]]), title="Auxiliary", pad=(3, 10)),
        ]
    ]

    win = sg.Window('CRaC -- Control Roof and Curtains by ARA', default_element_size=(40, 1)).Layout(layout)

    return win
