import PySimpleGUI as sg
import time, config, socket, gui
from logger import Logger

def connection(error, roof, curtains):
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
            rcv = s.recv(6)

            if ev1 is None or ev1 == "exit" or ev1 == "shutdown":
                s.close()
                return "E"

            data = rcv.decode("UTF-8")
            Logger.getLogger().debug("Data: "+data)
            if data[0] == "R":
                if data[-1] == "1":
                    roof = True
                    g_ui.open_roof()
                    g_ui.update_status_roof("Aperto", text_color="#2c2825", background_color="green")
                elif data[-1] == "0":
                    roof = False
                    g_ui.closed_roof()
                    g_ui.update_status_roof('Chiuso')
                elif data[-1] == "P":
                    Logger.getLogger().info("telescopio inviato alla posizione di park (park_tele) ")
                    g_ui.update_status_tele('Parked')
            elif data[0] == "D":
                g_ui.update_status_curtains('controllare switch tende')
            elif data[0] == "E":
                # la if si potrebbe togliere, l'errore dovrebbe sempre essere bloccante
                # ma va testato meglio
                if data != "E0000S":
                    g_ui.roof_alert('Attenzione Errore Bloccante!')
                    error = True
            else:
                if data == "000000":
                    curtains = False
                    g_ui.update_status_curtains('Chiuse')
                    g_ui.update_status_tele('Parked')
                else:
                    curtains = True
                    g_ui.update_status_curtains('Aperte', text_color="#2c2825", background_color="green")
                    g_ui.update_status_tele('Unparked', text_color="#2c2825", background_color="green")
                alpha_e, alpha_w = g_ui.update_curtains_text(int(data[0:3]), int(data[3:6]))
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
