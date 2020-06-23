import PySimpleGUI as sg # type: ignore
import math, config
from logger import LoggerClient as Logger
from tkinter import PhotoImage, NW, DISABLED
from typing import Tuple
from orientation import Orientation
from typing import Dict
from gui_constants import GuiLabel, GuiKey

class Gui:

    def __init__(self):
        self.n_step_corsa = config.Config.getInt('n_step_corsa', "encoder_step")
        self.alt_max_tend_e = config.Config.getInt("max_est", "tende")
        self.alt_max_tend_w = config.Config.getInt("max_west", "tende")
        self.alt_min_tend_e = config.Config.getInt("park_est", "tende")
        self.alt_min_tend_w = config.Config.getInt("park_west", "tende")
        self.alpha_min_conf = config.Config.getInt("alpha_min", "tende")
        self.increm_e = (self.alt_max_tend_e - self.alt_min_tend_e) / self.n_step_corsa
        self.increm_w = (self.alt_max_tend_w - self.alt_min_tend_w) / self.n_step_corsa
        self.conv = 2 * math.pi / 360 # conversion from degrees to radians for applying math trigonometric algorithms
        self.tenda_e = None
        self.line2_e = None
        self.line3_e = None
        self.line4_e = None
        self.tenda_w = None
        self.line2_w = None
        self.line3_w = None
        self.line4_w = None
        self.image = None

        self.l = 390
        self.t = self.l / 4.25
        self.delta_pt = 1.5 * self.t
        self.h = int(self.l / 1.8)
        sg.theme('DarkBlue')
        layout = [
                    [sg.Menu([], tearoff=True)],
                    [sg.Text('Monitor Tende e Tetto ', size=(55, 1), justification='center', font=("Helvetica", 15))],
                    [
                        sg.Frame(layout=([[
                            sg.Button('Apri', key=GuiKey.OPEN_ROOF, disabled=False, size=(6, 1)),
                            sg.Button('Chiudi', key=GuiKey.CLOSE_ROOF, disabled=True, size=(6, 1), tooltip="non puoi chiudere il tetto perche è gia chiuso")
                        ]]), title="Tetto", pad=(3, 0)),
                        sg.Frame(layout=([[
                            sg.Button('Park', key=GuiKey.PARK_TELE, disabled=True, size=(5, 1)),
                            sg.Button('Flat', key=GuiKey.FLAT_TELE, disabled=True, size=(5, 1))
                        ]]), title="Telescopio", pad=(3, 0)),
                        sg.Frame(layout=([[
                            sg.Button('Attiva', key=GuiKey.START_CURTAINS, disabled=True, size=(6, 1), tooltip='schiacccia per attivare'),
                            sg.Button('Disattiva', key=GuiKey.STOP_CURTAINS,disabled=True,  size=(6, 1)),
                            sg.Button('Calibra', key=GuiKey.CALIBRATE_CURTAINS,disabled=True,  size=(6, 1))
                        ]]), title="Tende", pad=(3, 0))
                    ],
                    [
                        sg.Frame(layout=([[
                            sg.Button('On', key=GuiKey.PANEL_ON, disabled=False, size=(6, 1), tooltip="non puoi accendere il pannnello, il telescopio è in fase imaging"),
                            sg.Button('Off', key=GuiKey.PANEL_OFF, disabled=True, size=(6, 1), tooltip="non puoi spegnere un pannello spento :-)"),
                            sg.Text(GuiLabel.PANEL_OFF, size=(10, 1), justification='center', font=("Helvetica", 11), key='status-panel', background_color="red", text_color="white")
                        ]]), title="Panel Flat", pad=(3,10)),

                    ],
                    [
                        sg.Canvas(size=(self.l, self.h), background_color='grey', key='canvas'),
                        sg.Frame(layout=
                            ([[
                                sg.Column(layout=(
                                    [sg.Text('Est', size=(5, 1), justification='left', font=("Helvetica", 12), pad=((0, 0), (10, 0)))],
                                    [sg.Text('0', size=(5, 1), justification='right', font=("Helvetica", 12), key='apert_e', background_color="white", text_color="#2c2825", pad=(0, 0))],
                                    [sg.Text('Ovest', size=(5, 1), justification='left', font=("Helvetica", 12), pad=((0, 0), (50, 0)))],
                                    [sg.Text('0', size=(5, 1), justification='right', font=("Helvetica", 12), key='apert_w', background_color="white", text_color="#2c2825", pad=((0, 0), (0, 30)))]
                                ))
                            ]]), title='Tende', relief=sg.RELIEF_GROOVE, pad=(2, 0)
                        ),
                        sg.Frame(layout=
                            ([[
                                sg.Column(layout=(
                                    [sg.Text('Alt', size=(5, 1), justification='left', font=("Helvetica", 12), pad=((0, 0), (10, 0)))],
                                    [sg.Text('0', size=(5, 1), justification='right', font=("Helvetica", 12), key='alt', background_color="white", text_color="#2c2825", pad=(0, 0))],
                                    [sg.Text('Az', size=(5, 1), justification='left', font=("Helvetica", 12), pad=((0, 0), (50, 0)))],
                                    [sg.Text('0', size=(5, 1), justification='right', font=("Helvetica", 12), key='az', background_color="white", text_color="#2c2825", pad=((0, 0), (0, 30)))]
                                ))
                            ]]), title='Telescopio', relief=sg.RELIEF_GROOVE, pad=((6, 0), (0, 0))
                        )
                    ],
                    [sg.Frame(layout=
                        ([
                            [
                                sg.Column(layout=(
                                    [sg.Text('Tetto', size=(17, 1), justification='center', font=("Helvetica", 12))],
                                    [sg.Text(GuiLabel.ROOF_CLOSED, size=(17, 1),justification='center', font=("Helvetica", 12), key='status-roof', background_color="red", text_color="white")]
                                )),
                                sg.Column(layout=(
                                    [sg.Text('Telescopio', size=(17, 1), justification='center', font=("Helvetica", 12))],
                                    [sg.Text(GuiLabel.TELESCOPE_PARKED, size=(8, 1), justification='center', font=("Helvetica", 12), key='status-tele', background_color="red", text_color="white"),
                                    sg.Text(GuiLabel.TELESCOPE_TRACKING_OFF, size=(8, 1), justification='center', font=("Helvetica", 12), key='status-tracking', background_color="white", text_color="red")]
                                )),
                                sg.Column(layout=(
                                    [sg.Text('Tende', size=(17, 1), justification='center', font=("Helvetica", 12))],
                                    [sg.Text(GuiLabel.CURTAINS_CLOSED, size=(17, 1), justification='center', font=("Helvetica", 12), key='status-curtains', background_color="red", text_color="white")]
                                ))

                            ],
                            [sg.Text(GuiLabel.NO_ALERT, size=(64, 1), justification='center',background_color="#B0C4DE", font=("Helvetica", 12), text_color="#FF0000", key="alert",relief=sg.RELIEF_RIDGE)]
                        ]), title='Status CRaC', relief=sg.RELIEF_GROOVE
                    )]
                 ]

        self.win = sg.Window('CRaC -- Control Roof and Curtains by ARA', layout, grab_anywhere=False, finalize=True)
        self.base_draw()

    def create_background_image(self) -> None:

        """ Create the background image for the sky when the roof is open and hides immediately it """

        canvas = self.win.FindElement('canvas')
        self.img_fondo = PhotoImage(file="cielo_stellato.gif")
        self.image = canvas.TKCanvas.create_image(0, 0, image=self.img_fondo, anchor=NW)
        self.hide_background_image()

    def hide_background_image(self) -> None:

        """ Hide the sky when the roof is closed """

        canvas = self.win.FindElement('canvas')
        canvas.TKCanvas.itemconfigure(self.image, state='hidden')

    def show_background_image(self) -> None:

        """ Show the sky when the roof is open """

        canvas = self.win.FindElement('canvas')
        canvas.TKCanvas.itemconfigure(self.image, state='normal')

    def base_draw(self) -> None:
        p1 = ((int((self.l / 2) - (self.delta_pt / 2))) - (0.9 * self.t), self.h)
        p2 = ((int((self.l / 2) - (self.delta_pt / 2))) - (0.9 * self.t), ((self.h / 12) * 10))
        p3 = self.l / 2, 1.2 * (self.h / 2)
        p4 = ((int((self.l / 2) + (self.delta_pt / 2))) + (0.9 * self.t), ((self.h / 12) * 10))
        p5 = ((int((self.l / 2) + (self.delta_pt / 2))) + (0.9 * self.t), self.h)
        p6 = 1, self.h
        p7 = self.l - 1, self.h
        p8 = self.l - 1, (self.h / 11) * 8
        p9 = self.l / 2, (self.h / 11) * 4.5
        p10 = 1, (self.h / 11) * 8
        canvas = self.win.FindElement('canvas')
        self.create_background_image()
        canvas.TKCanvas.create_polygon((p6, p7, p8, p9, p10), width=1, outline='grey', fill='#D8D8D8')
        canvas.TKCanvas.create_polygon((p1, p5, p4, p3, p2), width=1, outline='grey', fill='#848484')

    def status_alert(self, mess_alert: str) -> None:

        """ Avvisa che le tende non possono essere aperte """

        self.win.FindElement('alert').Update(mess_alert)

    def update_status_roof(self, status: str, text_color: str = 'white', background_color: str = 'red') -> None:

        """ Update Roof Status """

        Logger.getLogger().info('update_status_roof in gui')
        self.win.FindElement('status-roof').Update(status, text_color=text_color, background_color=background_color)

    def __toggle_button__(self, *args, **kwargs):

        # args: list of elements keys
        # kwargs: dictionary of elements attributes

        # for every key in args:
        for key in args:

            # update the relative element with the kwargs attributes (actually we use only update=False but we can also do something like):
            # update=False, tooltip="whatever"...
            self.win.FindElement(key).Update(**kwargs)

    def update_enable_disable_button(self): #, status: str, text_color: str = 'white', background_color: str = 'red') -> None:

        """ Update enable-disable button """

        Logger.getLogger().info('update_enable_disable_button in gui')
        self.__toggle_button__(GuiKey.OPEN_ROOF, disabled=True)
        self.__toggle_button__(GuiKey.CLOSE_ROOF, GuiKey.PARK_TELE, GuiKey.FLAT_TELE, GuiKey.START_CURTAINS, GuiKey.STOP_CURTAINS, GuiKey.CALIBRATE_CURTAINS, disabled=False)


    def update_disable_button_close_roof(self): #, status: str, disabeld: str =''):

        """ Update disable button close roof"""

        Logger.getLogger().info('update_enable_disable_button_close_roof in gui')
        # self.win.FindElement('close-roof').Update(disabled=True)
        self.__toggle_button__(GuiKey.CLOSE_ROOF, disabled=True)


    def update_enable_button_open_roof(self): #, status: str, disabeld: str =''):

        """ Update enable button open roof"""

        Logger.getLogger().info('update_enable_disable_button_close_roof in gui')
        self.__toggle_button__(GuiKey.OPEN_ROOF, disabled=False)
        self.__toggle_button__(GuiKey.CLOSE_ROOF, GuiKey.PARK_TELE, GuiKey.FLAT_TELE, GuiKey.START_CURTAINS, GuiKey.STOP_CURTAINS, GuiKey.CALIBRATE_CURTAINS, disabled=True)

    def update_status_tele(self, status, text_color: str = 'white', background_color: str = 'red') -> None:

        """ Update Tele Status """

        Logger.getLogger().info('update_status_tele in gui')
        self.win.FindElement('status-tele').Update(status, text_color=text_color, background_color=background_color)

    def update_tele_text(self, coords: Dict[str, str]) -> None:

        """ Update telescope altazimuth coordinates """

        altitude = int(coords["alt"])
        azimuth = int(coords["az"])

        self.win.FindElement('alt').Update(altitude)
        self.win.FindElement('az').Update(azimuth)

    def update_status_curtains(self, status, text_color: str = 'white', background_color: str = 'red') -> None:

        """ Update Curtains Status """

        Logger.getLogger().info('update_status_curtains in gui')
        self.win.FindElement('status-curtains').Update(status, text_color=text_color, background_color=background_color)


    def update_curtains_text(self, e_e: int, e_w: int) -> Tuple[int, int]:

        """ Update curtains angular values """

        alpha_e = int(e_e * float("{0:.3f}".format(self.increm_e))) # from steps to degree for east
        alpha_w = int(e_w * float("{0:.3f}".format(self.increm_w))) # from steps to degree for west

        self.win.FindElement('apert_e').Update(alpha_e)
        self.win.FindElement('apert_w').Update(alpha_w)
        return alpha_e, alpha_w

    #PANEL FLAT
    def update_status_panel(self, status, text_color: str = 'white', background_color: str = 'red') -> None:

        """ Update Panel Status """

        Logger.getLogger().info('update_status_panel in gui')
        self.win.FindElement('status-panel').Update(status, text_color=text_color, background_color=background_color)

    def update_disable_button_panel_on(self): #, status: str, disabeld: str =''):

        """ Update enable button on panel flat"""

        Logger.getLogger().info('update_disable_button_panel_flat_on')
        self.__toggle_button__(GuiKey.PANEL_ON, disabled=True)
        self.__toggle_button__(GuiKey.PANEL_OFF, disabled=False)

    def update_disable_button_panel_off(self): #, status: str, disabeld: str =''):

        """ Update enable button on panel flat"""

        Logger.getLogger().info('update_disable_button_panel_flat_on')
        self.__toggle_button__(GuiKey.PANEL_ON, disabled=False)
        self.__toggle_button__(GuiKey.PANEL_OFF, disabled=True)

    #STATUS TRACKING
    def update_status_tracking(self, status, text_color: str = 'white', background_color: str = 'red') -> None:

        """ Update Tracking Status """

        Logger.getLogger().info('update_status_tracking in gui')
        self.win.FindElement('status-tracking').Update(status, text_color=text_color, background_color=background_color)

    #GRAPHIC
    def update_curtains_graphic(self, alpha_e: int, alpha_w: int) -> None:

        """ Draw curtains position with canvas """

        self.__delete_polygons__(self.tenda_e, self.line2_e, self.line3_e, self.line4_e)
        self.__delete_polygons__(self.tenda_w, self.line2_w, self.line3_w, self.line4_w)

        self.tenda_e, self.line2_e, self.line3_e, self.line4_e = self.__create_curtain_polygon__(alpha_e, Orientation.EAST)
        self.tenda_w, self.line2_w, self.line3_w, self.line4_w = self.__create_curtain_polygon__(alpha_w, Orientation.WEST)

    def __delete_polygons__(self, *polygons_and_lines) -> None:
        canvas = self.win.FindElement('canvas')
        for polygon in polygons_and_lines:
            canvas.TKCanvas.delete(polygon)

    def __create_curtain_polygon__(self, alpha: int, orientation: Orientation) -> tuple:
        pt, pt1, pt2, pt3, pt4, pt5 = self.__create_polygon_coordinates__(alpha, orientation)

        canvas = self.win.FindElement('canvas')

        return (
                canvas.TKCanvas.create_polygon((pt, pt1, pt2, pt3, pt4, pt5), width=1, outline='#E0F8F7', fill='#0B4C5F'),
                canvas.TKCanvas.create_line((pt, pt2), width=1, fill='#E0F8F7'),
                canvas.TKCanvas.create_line((pt, pt3), width=1, fill='#E0F8F7'),
                canvas.TKCanvas.create_line((pt, pt4), width=1, fill='#E0F8F7')
            )

    def __create_polygon_coordinates__(self, alpha: int, orientation: Orientation) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
            angolo_min = self.alpha_min_conf * self.conv # valore dell'inclinazione della base della tenda in radianti
            angolo1 = ((alpha / 4) + self.alpha_min_conf) * self.conv
            angolo2 = ((alpha / 2) + self.alpha_min_conf) * self.conv
            angolo3 = (((alpha / 4) * 3) + self.alpha_min_conf) * self.conv
            angolo = (alpha + self.alpha_min_conf) * self.conv

            i = 1 if orientation == Orientation.EAST else -1

            y = int(self.h / 3) * 2
            x = int((self.l / 2) + (i * self.delta_pt / 2))
            pt1 = (x + (i * (int(math.cos(angolo_min) * self.t))), y - (int(math.sin(angolo_min) * self.t)))
            pt2 = (x + (i * (int(math.cos(angolo1) * self.t))), y - (int(math.sin(angolo1) * self.t)))
            pt3 = (x + (i * (int(math.cos(angolo2) * self.t))), y - (int(math.sin(angolo2) * self.t)))
            pt4 = (x + (i * (int(math.cos(angolo3) * self.t))), y - (int(math.sin(angolo3) * self.t)))
            pt5 = (x + (i * (int(math.cos(angolo) * self.t))), y - (int(math.sin(angolo) * self.t)))

            pt = (x, y)

            return pt, pt1, pt2, pt3, pt4, pt5
