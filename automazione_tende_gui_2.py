import time, config, gui
from automazione_tende import AutomazioneTende

#img = Image(file="cielo_stellato", imgtype=gif)
#img = open("cielo_stellato.gif", 'r+')

def window_prime():
    alpha_e=''
    alpha_w=''
    automazioneTende = AutomazioneTende()
    coord = automazioneTende.park_curtains()
    prevCoord = coord
    g_ui = gui.Gui()
    #g_ui.win.Finalize()
    #[sg.Canvas(size=(l,h), background_color='#045FB4', key= 'canvas')],
    #[sg.Image('cielo_stellato.gif',  key='canvas')],
    #fig_photo = draw_figure(window.FindElement('canvas').TKCanvas, fig)
    while True:
        ev1, vals1 = g_ui.win.Read()
        print(ev1)
        print(vals1)
        if ev1 is None or ev1 == 'exit' or ev1 == 'shutdown':
            exit(0)

        elif ev1 =='open-roof':
            g_ui.open_roof()

        elif ev1 == 'start-curtains':
            if vals1['aperturatetto']=='Tetto chiuso':
                g_ui.closed_roof_alert()
            else:

                print ("corsa in step: "+str(automazioneTende.n_step_corsa_tot))
                print ("gradi escursione tende: "+ str(automazioneTende.alt_max_tend_e-automazioneTende.alt_min_tend_e))
                print ("gradi per step: "+ "{0:.3f}".format(automazioneTende.increm_e))
                print ("primi per step: "+ "{0:.3f}".format(automazioneTende.increm_e*60))
                coord = automazioneTende.read_altaz_mount_coordinate()

                if automazioneTende.diff_coordinates(prevCoord, coord):
                    automazioneTende.move_curtains_height(coord)
                    # solo se la differenza e' misurabile imposto le coordinate precedenti uguali a quelle attuali
                    # altrimenti muovendosi a piccoli movimenti le tendine non verrebbero mai spostate
                    prevCoord = coord

                    #----------disegno struttura base----------#

                    g_ui.base_draw()

                    #----------update valori angolari tende-------#

                    alpha_e, alpha_w = g_ui.update_curtains_text(automazioneTende.encoder_est.current_step, automazioneTende.encoder_west.current_step)

                    g_ui.update_curtains_graphic(alpha_e, alpha_w)

                elif ev1 == 'stop-curtains':
                    automazioneTende.park_curtains()

        elif ev1 =='close-roof':
            #chiudi tetto - mette alto o bvasso il gpio di controllo del pin di chiusura della scheda motori
           pass


window_prime()
