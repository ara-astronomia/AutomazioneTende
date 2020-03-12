import time, config, socket, gui
from logger import Logger
from automazione_tende import CracStatus
from status import Status, TelescopeStatus

def connection(error: bool, roof: bool, curtains: bool) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            ev1, _ = g_ui.win.Read(timeout=10000)

            if ev1 is None or ev1 == "exit":
                v = "E"
            elif error:
                continue

            elif ev1 == 'open-roof':
                v = "R"
                Logger.getLogger().info("e' stato premuto il tasto apri tetto (open_roof) ")

            elif ev1 == 'park-tele':
                v = "P"
                
            elif ev1 == 'close-roof':
                if curtains is True:
                    g_ui.roof_alert('Attenzione tende aperte')
                    continue
                v = "T"
                Logger.getLogger().info("funzione tetto in chiusura (close_roof) ")

            elif ev1 == 'start-curtains':
                if roof is False:
                    g_ui.roof_alert('Attenzione tetto chiuso')
                    continue
 #               g_ui.base_draw()
                v = "1"

            elif ev1 == 'stop-curtains':
                v = "0"

            elif ev1 == "shutdown":
                v = "-"

            else:
                if curtains is False:
                    continue
                v = "c"

            s.sendall(v.encode("UTF-8"))
            Logger.getLogger().info("invio paramentri con sendall")
            rcv = s.recv(16)

            if ev1 is None or ev1 == "exit" or ev1 == "shutdown":
                s.close()
                return "E"

            data = rcv.decode("UTF-8")
            crac_status = CracStatus(data)
            Logger.getLogger().debug("Tenda Est step: %s", crac_status.curtain_east_steps)
            Logger.getLogger().debug("Tenda west step: %s", crac_status.curtain_west_steps)
            Logger.getLogger().debug("Data: %s", crac_status)
            if crac_status.roof_status == Status.OPEN:
                roof = True
                g_ui.show_background_image()
                g_ui.update_status_roof("Aperto", text_color="#2c2825", background_color="green")
            elif crac_status.roof_status == Status.CLOSED:
                roof = False
                g_ui.hide_background_image()
                g_ui.update_status_roof('Chiuso')
            elif crac_status.telescope_status == TelescopeStatus.PARKED:
                    Logger.getLogger().info("telescopio in park")
                    g_ui.update_status_tele('Parked')
            elif crac_status.telescope_status == TelescopeStatus.SECURE:
                    Logger.getLogger().info("telescopio in sicurezza ")
                    g_ui.update_status_tele('In Sicurezza')
            elif crac_status.curtain_east_status == Status.DANGER or crac_status.curtain_west_status == Status.DANGER:
                g_ui.update_status_curtains('controllare switch tende')
            # elif data[0] == "E":
            #     # la if si potrebbe togliere, l'errore dovrebbe sempre essere bloccante
            #     # ma va testato meglio
            #     if data != "E0000S":
            #         g_ui.roof_alert('Attenzione Errore Bloccante!')
            #         error = True
            elif crac_status.curtain_east_status == Status.CLOSED and crac_status.curtain_west_status.CLOSED:
                curtains = False
                g_ui.update_status_curtains('Chiuse')
                g_ui.update_status_tele('Parked')
            else:
                curtains = True
                g_ui.update_status_curtains('Aperte', text_color="#2c2825", background_color="green")
                g_ui.update_status_tele('Unparked', text_color="#2c2825", background_color="green")
            alpha_e, alpha_w = g_ui.update_curtains_text(int(crac_status.curtain_east_steps), int(crac_status.curtain_west_steps))
            g_ui.update_curtains_graphic(alpha_e, alpha_w)

HOST = config.Config.getValue("ip", "server")  # The server's hostname or IP address
PORT = config.Config.getInt("port", "server")  # The port used by the server

g_ui = gui.Gui()
roof = False
curtains = False
error = False

while True:
    Logger.getLogger().debug("connessione a: " + HOST + ":" + str(PORT))
    key = connection(error, roof, curtains)
    if key == "E":
        exit(0)
