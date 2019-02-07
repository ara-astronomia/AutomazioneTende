import PySimpleGUI as sg
import time, config
from graphics import *
import math
from automazione_tende import AutomazioneTende
import image

l=400
t=l/4.25
delta_pt= 1.5*t

h=int(l/1.8) # int((l/3)*2)
  
    
def window_prime():
    alpha_e=''
    alpha_w=''  
    automazioneTende = AutomazioneTende()
    coord = automazioneTende.park_curtains()
    prevCoord = coord
    sg.ChangeLookAndFeel('GreenTan')
    # Design pattern 1 - First window does not remain active

    menu_def = [['File', ['Exit']],
                ['Help', 'About...']]
    layout = [[sg.Menu(menu_def, tearoff=True)],
             
             [sg.Text('Controllo movimento tende ', size=(37, 1), justification='center', font=("Helvetica", 15), relief=sg.RELIEF_RIDGE)],
             [sg.Button('Apri tetto'),sg.Button('Start Tende')],
             [sg.ProgressBar((100), orientation='h', size=(37,25), key='progbar_tetto')],
             [sg.InputText('Tetto chiuso',size=(57, 1),justification='center', font=("Arial", 10), key='aperturatetto')],
             [sg.Canvas(size=(l,h), background_color='#045FB4', key= 'canvas')],
            
             [sg.Text('posizione tenda est -- apertura  °' , size=(28,1), justification='right', font=("Arial", 8), relief=sg.RELIEF_RIDGE),
             sg.InputText('  ' , size=(3, 1), justification='left', font=("Arial", 8),  key ='apert_e')],
             [sg.Text('posizione tenda west -- apertura  °', size=(28, 1), justification='right', font=("Arial", 8), relief=sg.RELIEF_RIDGE),
             sg.InputText('  ' , size=(3, 1), justification='left', font=("Arial", 8),  key ='apert_w')],
             [sg.Button('Chiudi tende'), sg.Button('Chiudi tetto'),sg.Button('Exit')]]
             

    win1 = sg.Window('Controllo tende Osservatorio', grab_anywhere=False).Layout(layout)
    #win1.Finalize()
    
    #fig_photo = draw_figure(window.FindElement('canvas').TKCanvas, fig)
    while True:
        ev1, vals1 = win1.Read()
        #print (vals1)
        if ev1 == 'Exit':
            exit(0)
        
        elif ev1 =='Apri tetto':
            win1.FindElement('progbar_tetto').UpdateBar(100)
            win1.FindElement('aperturatetto').Update('Tetto aperto')
            #apri tetto - mette alto o basso il gpio di controllo del pin di aperutra della scheda motori    
            #pass
        
           
        elif ev1 == 'Start Tende':
            if vals1['aperturatetto']=='Tetto chiuso':
                canvas = win1.FindElement('canvas')
                
                canvas= canvas.TKCanvas.create_text(l/2, h/2, font= ('Arial', 25), fill='#FE2E2E', text= "Attenzione aprire il tetto")
            else:
                #canvas = win1.FindElement('canvas')
                #create_text(l/2, h/2, font= ('Arial', 25), fill='#6E6E6E', text= "Tetto aperto")
                
                win1.FindElement('aperturatetto').Update('Tetto aperto')
                print ("corsa in step: "+str(automazioneTende.n_step_corsa_tot))
                print ("gradi escursione tende: "+ str(automazioneTende.alt_max_tend_e-automazioneTende.alt_min_tend_e))
                print ("gradi per step: "+ "{0:.3f}".format(automazioneTende.increm_e))
                print ("primi per step: "+ "{0:.3f}".format(automazioneTende.increm_e*60))
                #print (str(prog_e) +'progressivo')
                
                
                #print(encoder_west.listen_until(current_step))
                coord = automazioneTende.read_altaz_mount_coordinate()
                if automazioneTende.diff_coordinates(prevCoord, coord):
                    automazioneTende.move_curtains_height(coord)
                    # solo se la differenza e' misurabile imposto le coordinate precedenti uguali a quelle attuali
                    # altrimenti muovendosi a piccoli movimenti le tendine non verrebbero mai spostate
                    prevCoord = coord
                    e_e=(automazioneTende.encoder_est.current_step)
                    e_w=(automazioneTende.encoder_west.current_step)
     
                    pos_enc_e=e_e
                    pos_enc_w=e_w
                    
                    alpha_e_min= int(config.Config.getValue("park_est", "tende")) # questo equivale al parametro di altezza minima esistente nel file ini
                    alpha_w_min = int(config.Config.getValue("park_west", "tende")) 
                    #canvas = win1.FindElement('alpha_e').UpdateText(alpha_e)
                    win1.FindElement('apert_e').Update('10')
                    alpha_e = int(e_e*float("{0:.3f}".format(automazioneTende.increm_e))) # trasformazione posizione step in gradi
                    alpha_w = int(e_w*float("{0:.3f}".format(automazioneTende.increm_w))) # COME SOPRA
                    win1.FindElement('apert_e').Update(alpha_e)
                    win1.FindElement('apert_w').Update(alpha_w)
                    
                    conv=2*math.pi/360.0 # converisone gradi in radianti per potere applicare gli algoritimi trigonometrici in math
                    
                    angolo_e_min=alpha_e_min*conv # valore dell'inclinazione della base della tenda est in radianti
                    angolo_w_min=alpha_w_min*conv # valore dell'inclinazione della base della tenda west in radianti
                    
                 #-------definizione settori angolari tende --------------------# 
                    angolo1_e = ((alpha_e/4)+alpha_e_min) * conv
                    angolo2_e = ((alpha_e/2)+alpha_e_min) * conv
                    angolo3_e = (((alpha_e/4)*3)+alpha_e_min) * conv
                    angolo_e = (alpha_e + alpha_e_min) * conv
                    
                    angolo1_w = ((alpha_w/4)+alpha_w_min) * conv
                    angolo2_w = ((alpha_w/2)+alpha_w_min) * conv
                    angolo3_w = (((alpha_w/4)*3)+alpha_w_min) * conv
                    angolo_w = (alpha_w + alpha_w_min)* conv
                    
                   
                    #h_t =int(l/50) #parametro per definire la dimensione degli oggetti a schermo, in modo da scalarli con le misure della finestra
                 
                   
                  #-------------parametri grafici tende--------#  
                    #t=int(l*(1.7/5)) #proporzione lunghezza braccio tende in funzione della grandezza della window
                    
                    
                    #---origine tende----#
                    x_e = int((l/2)+(delta_pt/2)) # int(l/5)*3
                    y_e = int(h/3)*2
                    
                    x_w = int((l/2)-(delta_pt/2)) # int(l/5)*2
                    y_w = int(h/3)*2
                    
                    #-------vertici poligoni tende----------#
                    #delete = canvas.TKCanvas.delete(canvas)
                    canvas = win1.FindElement('canvas')
                    
                    pt_e = (x_e, y_e)
                    pt_w = (x_w, y_w)
                                   
                    pt_e0 = (x_e-t, y_e)
                    pt_w0 = (x_w+t, y_w)
                              
                    x_e1 = (math.cos(angolo_e_min)*t)+x_e
                    x_w1 = (math.cos(angolo_e_min)*t)+x_w
                           
                    pt_e1= (x_e+(int(math.cos(angolo_e_min)*t)),y_e-(int(math.sin(angolo_e_min)*t)))
                    pt_e2= (x_e+(int(math.cos(angolo1_e)*t)),y_e-(int(math.sin(angolo1_e)*t)))
                    pt_e3= (x_e+(int(math.cos(angolo2_e)*t)),y_e-(int(math.sin(angolo2_e)*t)))
                    pt_e4= (x_e+(int(math.cos(angolo3_e)*t)),y_e-(int(math.sin(angolo3_e)*t)))
                    pt_e5= (x_e+(int(math.cos(angolo_e)*t)),y_e-(int(math.sin(angolo_e)*t)))

                    canvas.TKCanvas.create_polygon((pt_e,pt_e1,pt_e2,pt_e3,pt_e4,pt_e5), width=1,outline='#E0F8F7',fill='#0B4C5F') # tenda_e
           
                    canvas.TKCanvas.create_line((pt_e,pt_e2), width=1,fill='#E0F8F7') #line2_e
                    canvas.TKCanvas.create_line((pt_e,pt_e3), width=1,fill='#E0F8F7') #line3_e
                    canvas.TKCanvas.create_line((pt_e,pt_e4), width=1,fill='#E0F8F7') #line4_e
             
                    
                    pt_w1= (x_w-(int(math.cos(angolo_w_min)*t)),y_w-(int(math.sin(angolo_w_min)*t)))
                    pt_w2= (x_w-(int(math.cos(angolo1_w)*t)),y_w-(int(math.sin(angolo1_w)*t)))
                    pt_w3= (x_w-(int(math.cos(angolo2_w)*t)),y_w-(int(math.sin(angolo2_w)*t)))
                    pt_w4= (x_w-(int(math.cos(angolo3_w)*t)),y_w-(int(math.sin(angolo3_w)*t)))
                    pt_w5= (x_w-(int(math.cos(angolo_w)*t)),y_w-(int(math.sin(angolo_w)*t)))
                    
                    canvas.TKCanvas.create_polygon((pt_w,pt_w1,pt_w2,pt_w3,pt_w4,pt_w5), width=1,outline='#E0F8F7',fill='#0B4C5F') # tenda_w
                              
                    canvas.TKCanvas.create_line((pt_w,pt_w2), width=1,fill='#E0F8F7') #line2_w
                    canvas.TKCanvas.create_line((pt_w,pt_w3), width=1,fill='#E0F8F7') #line3_w
                    canvas.TKCanvas.create_line((pt_w,pt_w4), width=1,fill='#E0F8F7') #line4_w
                    
                    
                elif ev1 == 'Chiudi Tende':
                    automazioneTende.park_curtains()        

        elif ev1 =='Chiudi tetto':
            #chiudi tetto - mette alto o bvasso il gpio di controllo del pin di chiusura della scheda motori    
           pass
   

   
    #win.getMouse()
    #win.close()
    
    
#window_graph()
#sg.ProgressBar((automazioneTende.n_step_corsa_tot), orientation='v', size=(20, 20), key='progbar_e'),
#sg.ProgressBar((automazioneTende.n_step_corsa_tot), orientation='v', size=(20, 20), key='progbar_w')

window_prime()
    
            