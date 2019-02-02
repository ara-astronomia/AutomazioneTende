import PySimpleGUI as sg
import time, config
from automazione_tende import AutomazioneTende

automazioneTende = AutomazioneTende()
coord = automazioneTende.park_curtains()
prevCoord = coord
sg.ChangeLookAndFeel('GreenTan')
# Design pattern 1 - First window does not remain active

menu_def = [['File', ['Exit']],
            ['Help', 'About...']]
layout = [[sg.Menu(menu_def, tearoff=True)],
         [sg.Text('Controllo movimento tende ', size=(30, 1), justification='center', font=("Helvetica", 15), relief=sg.RELIEF_RIDGE)],
         [sg.Text('altezza telescopio')],
         [sg.ProgressBar((automazioneTende.n_step_corsa_tot), orientation='h', size=(20, 20), key='progbar_e')],
         [sg.ProgressBar((automazioneTende.n_step_corsa_tot), orientation='h', size=(20, 20), key='progbar_w')],
         [sg.Button('StartTende')],[sg.Button('Exit')]]

win1 = sg.Window('Controllo tende Osservatorio').Layout(layout)
while True:
    ev1, vals1 = win1.Read()
    print ("corsa in step: "+str(automazioneTende.n_step_corsa_tot))
    print ("gradi escursione tende: "+ str(automazioneTende.alt_max_tend_e-automazioneTende.alt_min_tend_e))
    print ("gradi per step: "+ "{0:.3f}".format(automazioneTende.increm_e))
    print ("primi per step: "+ "{0:.3f}".format(automazioneTende.increm_e*60))
    #print (str(prog_e) +'progressivo')
    #win1.FindElement('progbar_e').UpdateBar(coord['alt'])
    #print(encoder_west.listen_until(current_step))
    coord = automazioneTende.read_altaz_mount_coordinate()
    if automazioneTende.diff_coordinates(prevCoord, coord):
        automazioneTende.move_curtains_height(coord)
        # solo se la differenza è misurabile imposto le coordinate precedenti uguali a quelle attuali
        # altrimenti muovendosi a piccoli movimenti le tendine non verrebbero mai spostate
        prevCoord = coord
    win1.FindElement('progbar_e').UpdateBar(coord['alt'])
    #win1.FindElement('progbar_w').UpdateBar(west)
