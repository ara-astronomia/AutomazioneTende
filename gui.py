import PySimpleGUI as sg
import math, config
from logger import Logger
from tkinter import PhotoImage, NW, DISABLED

class Gui:

    def __init__(self):
        self.n_step_corsa = config.Config.getInt('n_step_corsa', "encoder_step")
        self.alt_max_tend_e = config.Config.getInt("max_est", "tende")
        self.alt_max_tend_w = config.Config.getInt("max_west", "tende")
        self.alt_min_tend_e = config.Config.getInt("park_est", "tende")
        self.alt_min_tend_w = config.Config.getInt("park_west", "tende")
        self.alpha_min_conf = config.Config.getInt("alpha_min", "tende")
        self.increm_e = (self.alt_max_tend_e-self.alt_min_tend_e)/self.n_step_corsa
        self.increm_w = (self.alt_max_tend_w-self.alt_min_tend_w)/self.n_step_corsa
        self.tenda_e = None
        self.line2_e = None
        self.line3_e = None
        self.line4_e = None
        self.tenda_w = None
        self.line2_w = None
        self.line3_w = None
        self.line4_w = None
        self.img_fondo = None
        self.image = None

        self.l = 390
        self.t = self.l / 4.25
        self.delta_pt = 1.5 * self.t
        self.h = int(self.l / 1.8)
        sg.theme('DarkBlue')
        layout = [
                    [sg.Menu([], tearoff=True)],
                    [sg.Text('Monitor Tende e Tetto ', size=(50, 1), justification='center', font=("Helvetica", 15))],
                    [
                        sg.Frame(layout=([[
                            sg.Button('Apri', key='open-roof', size=(6, 1)),
                            sg.Button('Chiudi', key="close-roof", size=(6, 1))
                        ]]), title="Tetto"),
                        sg.Frame(layout=([[
                            sg.Button('Park', key="park-tele", size=(6, 1))
                        ]]), title="Telescopio"),
                        sg.Frame(layout=([[
                            sg.Button('Attiva', key='start-curtains', size=(9, 1)),
                            sg.Button('Disattiva', key="stop-curtains", size=(9, 1)),
                            sg.Button('Calibra', key="calibrate-curtains", size=(9, 1))
                        ]]), title="Tende")
                    ],
                    [
                        sg.Canvas(size=(self.l,self.h), background_color='grey', key='canvas'),
                        sg.Frame(layout=
                            ([[
                                sg.Column(layout=(
                                    [sg.Text('Est', size=(5, 1), justification='left', font=("Helvetica", 12), pad=((0, 0), (35, 0)))],
                                    [sg.Text('0', size=(5, 1), justification='right', font=("Helvetica", 12), key='apert_e', background_color="white", text_color="#2c2825", pad=(0, 0))],
                                    [sg.Text('Ovest', size=(5, 1), justification='left', font=("Helvetica", 12), pad=((0, 0), (50, 0)))],
                                    [sg.Text('0', size=(5, 1), justification='right', font=("Helvetica", 12), key='apert_w', background_color="white", text_color="#2c2825", pad=((0, 0), (0, 35)))]
                                ))
                            ]]), title='Tende', relief=sg.RELIEF_GROOVE, pad=(0,0)
                        )
                    ],
                    [sg.Frame(layout=
                        ([[
                            sg.Column(layout=(
                                [sg.Text('Tetto', size=(17, 1), justification='center', font=("Helvetica", 12))],
                                [sg.Text('Chiuso', size=(17, 1),justification='center', font=("Helvetica", 12), key='status-roof', background_color="red", text_color="white")]
                            )),
                            sg.Column(layout=(
                                [sg.Text('Telescopio', size=(17, 1), justification='center', font=("Helvetica", 12))],
                                [sg.Text('Parked', size=(17, 1), justification='center', font=("Helvetica", 12), key='status-tele', background_color="red", text_color="white")]
                            )),
                            sg.Column(layout=(
                                [sg.Text('Tende', size=(17, 1), justification='center', font=("Helvetica", 12))],
                                [sg.Text('Chiuse', size=(17, 1), justification='center', font=("Helvetica", 12), key='status-curtains', background_color="red", text_color="white")]
                            ))
                        ]]), title='Status CRaC', relief=sg.RELIEF_GROOVE
                    )]
                 ]

        self.win = sg.Window('CRaC -- Control Roof and Curtains by ARA', layout, grab_anywhere=False, finalize=True)
        self.base_draw()
        self.remove_background_image()

    def create_background_image(self):
        canvas = self.win.FindElement('canvas')
        self.img_fondo = PhotoImage(file = "cielo_stellato.gif")
        self.image = canvas.TKCanvas.create_image(0,0, image=self.img_fondo, anchor=NW)

    def remove_background_image(self):
        canvas = self.win.FindElement('canvas')
        canvas.TKCanvas.itemconfigure(self.image, state='hidden')

    def set_background_image(self):
        if not self.img_fondo:
            self.create_background_image()
        canvas = self.win.FindElement('canvas')
        canvas.TKCanvas.itemconfigure(self.image, state='normal')

    def base_draw(self):
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

    def roof_alert(self, mess_alert):

        """Avvisa che le tende non possono essere aperte"""

        canvas = self.win.FindElement('canvas')
        alert = mess_alert
        self.win.FindElement('status-roof').Update(alert)
        canvas.TKCanvas.create_text(self.l / 2, self.h / 2, font=('Helvetica', 25), fill='#FE2E2E', text=alert)

    def closed_roof(self):

        """ avvisa sullo stato chiuso del tetto """

        self.remove_background_image()

    def open_roof(self):

        """ avvisa sullo stato aperto del tetto """

        self.set_background_image()

    def update_status_roof(self, status, text_color='white', background_color='red'):

        """ Update Roof Status """

        Logger.getLogger().info('update_status_roof in gui')
        self.win.FindElement('status-roof').Update(status, text_color=text_color, background_color=background_color)

    def update_status_tele(self, status, text_color='white', background_color='red'):

        """ Update Tele Status """

        Logger.getLogger().info('update_status_tele in gui')
        self.win.FindElement('status-tele').Update(status, text_color=text_color, background_color=background_color)

    def update_status_curtains(self, status, text_color='white', background_color='red'):

        """ Update Curtains Status """

        Logger.getLogger().info('update_status_curtains in gui')
        self.win.FindElement('status-curtains').Update(status, text_color=text_color, background_color=background_color)

    def update_curtains_text(self, e_e, e_w):

        """ Update curtains angular values """

        alpha_e = int(e_e*float("{0:.3f}".format(self.increm_e))) # trasformazione posizione step in gradi
        alpha_w = int(e_w*float("{0:.3f}".format(self.increm_w))) # COME SOPRA

        self.win.FindElement('apert_e').Update(alpha_e)
        self.win.FindElement('apert_w').Update(alpha_w)
        return alpha_e, alpha_w

    def update_curtains_graphic(self, alpha_e, alpha_w):

        """ Draw curtains position with canvas """

        self.__delete_polygons__(self.tenda_e, self.line2_e, self.line3_e, self.line4_e)
        self.__delete_polygons__(self.tenda_w, self.line2_w, self.line3_w, self.line4_w)

        self.tenda_e, self.line2_e, self.line3_e, self.line4_e = self.__create_curtain_polygon__(alpha_e, "E")
        self.tenda_w, self.line2_w, self.line3_w, self.line4_w = self.__create_curtain_polygon__(alpha_w, "W")

    def __delete_polygons__(self, *polygons_and_lines):
        canvas = self.win.FindElement('canvas')
        for polygon in polygons_and_lines:
            canvas.TKCanvas.delete(polygon)

    def __create_curtain_polygon__(self, alpha, orientation):
        conv=2*math.pi/360.0 # converisone gradi in radianti per potere applicare gli algoritimi trigonometrici in math
        alpha_min = self.alpha_min_conf
        angolo_min=alpha_min*conv # valore dell'inclinazione della base della tenda est in radianti
        angolo1 = ((alpha / 4) + alpha_min) * conv
        angolo2 = ((alpha / 2) + alpha_min) * conv
        angolo3 = (((alpha / 4) * 3) + alpha_min) * conv
        angolo = (alpha + alpha_min) * conv


        i = 1 if orientation == "E" else -1

        y = int(self.h/3)*2
        x = int((self.l/2)+(i*self.delta_pt / 2)) # int(l/5)*3
        pt1 = (x + (i * (int(math.cos(angolo_min) * self.t))), y - (int(math.sin(angolo_min) * self.t)))
        pt2 = (x + (i * (int(math.cos(angolo1) * self.t))), y - (int(math.sin(angolo1) * self.t)))
        pt3 = (x + (i * (int(math.cos(angolo2) * self.t))), y - (int(math.sin(angolo2) * self.t)))
        pt4 = (x + (i * (int(math.cos(angolo3) * self.t))), y - (int(math.sin(angolo3) * self.t)))
        pt5 = (x + (i * (int(math.cos(angolo) * self.t))), y - (int(math.sin(angolo) * self.t)))

        pt = (x, y)

        canvas = self.win.FindElement('canvas')

        return (
                canvas.TKCanvas.create_polygon((pt, pt1, pt2, pt3, pt4, pt5), width=1, outline='#E0F8F7', fill='#0B4C5F'),
                canvas.TKCanvas.create_line((pt, pt2), width=1, fill='#E0F8F7'),
                canvas.TKCanvas.create_line((pt, pt3), width=1, fill='#E0F8F7'),
                canvas.TKCanvas.create_line((pt, pt4), width=1, fill='#E0F8F7')
            )
