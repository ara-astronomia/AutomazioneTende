import PySimpleGUI as sg
import math, config

class Gui:

    def __init__(self):
        self.l=400
        self.t=self.l/4.25
        self.delta_pt= 1.5*self.t
        self.h=int(self.l/1.8) # int((l/3)*2)
        sg.ChangeLookAndFeel('GreenTan')
        # Design pattern 1 - First window does not remain active

        menu_def = [['File', ['Exit']],
                    ['Help', 'About...']]
        layout = [[sg.Menu(menu_def, tearoff=True)],

                 [sg.Text('Controllo movimento tende ', size=(37, 1), justification='center', font=("Helvetica", 15), relief=sg.RELIEF_RIDGE)],
                 [sg.Button('Apri tetto'),sg.Button('Start Tende')],
                 [sg.ProgressBar((100), orientation='h', size=(37,25), key='progbar_tetto')],
                 [sg.InputText('Tetto chiuso',size=(57, 1),justification='center', font=("Arial", 10), key='aperturatetto')],
                 [sg.Canvas(size=(self.l,self.h), background_color= '#045FB4', key= 'canvas')],


                 [sg.Text('posizione tenda est -- apertura  °' , size=(28,1), justification='right', font=("Arial", 8), relief=sg.RELIEF_RIDGE),
                 sg.InputText('  ' , size=(3, 1), justification='left', font=("Arial", 8),  key ='apert_e')],
                 [sg.Text('posizione tenda west -- apertura  °', size=(28, 1), justification='right', font=("Arial", 8), relief=sg.RELIEF_RIDGE),
                 sg.InputText('  ' , size=(3, 1), justification='left', font=("Arial", 8),  key ='apert_w')],
                 [sg.Button('Chiudi tende'), sg.Button('Chiudi tetto'),sg.Button('Exit')]]
        if config.Config.getValue("test") is "1":
            layout.append([sg.Button('Shutdown')])


        self.win = sg.Window('Controllo tende Osservatorio', grab_anywhere=False).Layout(layout)

    def base_draw(self):
        p1 = ( (int((self.l/2)-(self.delta_pt/2)))-(0.9*self.t),self.h)
        p2 = ( (int((self.l/2)-(self.delta_pt/2)))-(0.9*self.t),((self.h/12)*10) )
        p3 = self.l/2, 1.2*(self.h/2)
        p4 = ( (int((self.l/2)+(self.delta_pt/2)))+(0.9*self.t),((self.h/12)*10) )
        p5 = ( (int((self.l/2)+(self.delta_pt/2)))+(0.9*self.t),self.h)
        p6 = 1,self.h
        p7 = self.l-1,self.h
        p8 = self.l-1,(self.h/11)*8
        p9 = self.l/2, (self.h/11)*4.5
        p10 = 1, (self.h/11)*8
        canvas = self.win.FindElement('canvas')
        canvas.TKCanvas.create_polygon((p6,p7,p8,p9,p10), width=1, outline='grey',fill='#D8D8D8')
        canvas.TKCanvas.create_polygon((p1,p5,p4,p3,p2), width=1, outline='grey',fill='#848484')

    def closed_roof_alert(self):

        """Avvisa che il tetto non può essere aperto"""

        canvas = self.win.FindElement('canvas')
        canvas.TKCanvas.create_text(self.l/2, self.h/2, font=('Arial', 25), fill='#FE2E2E', text= "Attenzione aprire il tetto")

    def open_roof(self):

        """Disegna l'apertura del tetto"""

        canvas = self.win.FindElement('canvas')
        self.win.FindElement('aperturatetto').Update('Tetto aperto')
        canvas.TKCanvas.create_rectangle(0,0,self.l,self.h, fill='#045FB4')

    def update_curtains_text(self, e_e, e_w, increm_e, increm_w):

        """Update valori angolari tende"""

        alpha_e = int(e_e*float("{0:.3f}".format(increm_e))) # trasformazione posizione step in gradi
        alpha_w = int(e_w*float("{0:.3f}".format(increm_w))) # COME SOPRA

        self.win.FindElement('apert_e').Update(alpha_e)
        self.win.FindElement('apert_w').Update(alpha_w)
        return alpha_e, alpha_w

    def update_curtains_graphic(self, alpha_e, alpha_w):

        """Disegna le tende con canvas"""

        #-------definizione settori angolari tende -----------#

        conv=2*math.pi/360.0 # converisone gradi in radianti per potere applicare gli algoritimi trigonometrici in math
        alpha_e_min = -12
        alpha_w_min = -12
        angolo_e_min=alpha_e_min*conv # valore dell'inclinazione della base della tenda est in radianti
        angolo_w_min=alpha_w_min*conv # valore dell'inclinazione della base della tenda west in radianti
        angolo1_e = ((alpha_e/4)+alpha_e_min) * conv
        angolo2_e = ((alpha_e/2)+alpha_e_min) * conv
        angolo3_e = (((alpha_e/4)*3)+alpha_e_min) * conv
        angolo_e = (alpha_e + alpha_e_min) * conv

        angolo1_w = ((alpha_w/4)+alpha_w_min) * conv
        angolo2_w = ((alpha_w/2)+alpha_w_min) * conv
        angolo3_w = (((alpha_w/4)*3)+alpha_w_min) * conv
        angolo_w = (alpha_w + alpha_w_min)* conv

      #-------------parametri grafici tende--------#

        #---origine tende----#
        x_e = int((self.l/2)+(self.delta_pt/2)) # int(l/5)*3
        y_e = int(self.h/3)*2

        x_w = int((self.l/2)-(self.delta_pt/2)) # int(l/5)*2
        y_w = int(self.h/3)*2

        #-------vertici poligoni tende----------#
        #delete = canvas.TKCanvas.delete(canvas)

        canvas = self.win.FindElement('canvas')

        pt_e = (x_e, y_e)
        pt_w = (x_w, y_w)

        pt_e0 = (x_e-self.t, y_e)
        pt_w0 = (x_w+self.t, y_w)

        x_e1 = (math.cos(angolo_e_min)*self.t)+x_e
        x_w1 = (math.cos(angolo_e_min)*self.t)+x_w

        pt_e1= (x_e+(int(math.cos(angolo_e_min)*self.t)),y_e-(int(math.sin(angolo_e_min)*self.t)))
        pt_e2= (x_e+(int(math.cos(angolo1_e)*self.t)),y_e-(int(math.sin(angolo1_e)*self.t)))
        pt_e3= (x_e+(int(math.cos(angolo2_e)*self.t)),y_e-(int(math.sin(angolo2_e)*self.t)))
        pt_e4= (x_e+(int(math.cos(angolo3_e)*self.t)),y_e-(int(math.sin(angolo3_e)*self.t)))
        pt_e5= (x_e+(int(math.cos(angolo_e)*self.t)),y_e-(int(math.sin(angolo_e)*self.t)))

        canvas.TKCanvas.create_polygon((pt_e,pt_e1,pt_e2,pt_e3,pt_e4,pt_e5), width=1,outline='#E0F8F7',fill='#0B4C5F') # tenda_e

        canvas.TKCanvas.create_line((pt_e,pt_e2), width=1,fill='#E0F8F7') #line2_e
        canvas.TKCanvas.create_line((pt_e,pt_e3), width=1,fill='#E0F8F7') #line3_e
        canvas.TKCanvas.create_line((pt_e,pt_e4), width=1,fill='#E0F8F7') #line4_e


        pt_w1= (x_w-(int(math.cos(angolo_w_min)*self.t)),y_w-(int(math.sin(angolo_w_min)*self.t)))
        pt_w2= (x_w-(int(math.cos(angolo1_w)*self.t)),y_w-(int(math.sin(angolo1_w)*self.t)))
        pt_w3= (x_w-(int(math.cos(angolo2_w)*self.t)),y_w-(int(math.sin(angolo2_w)*self.t)))
        pt_w4= (x_w-(int(math.cos(angolo3_w)*self.t)),y_w-(int(math.sin(angolo3_w)*self.t)))
        pt_w5= (x_w-(int(math.cos(angolo_w)*self.t)),y_w-(int(math.sin(angolo_w)*self.t)))

        canvas.TKCanvas.create_polygon((pt_w,pt_w1,pt_w2,pt_w3,pt_w4,pt_w5), width=1,outline='#E0F8F7',fill='#0B4C5F') # tenda_w

        canvas.TKCanvas.create_line((pt_w,pt_w2), width=1,fill='#E0F8F7') #line2_w
        canvas.TKCanvas.create_line((pt_w,pt_w3), width=1,fill='#E0F8F7') #line3_w
        canvas.TKCanvas.create_line((pt_w,pt_w4), width=1,fill='#E0F8F7') #line4_w
      #---------fine parte grafica ------#
