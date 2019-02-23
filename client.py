import PySimpleGUI as sg
import time, config, socket, gui
if config.Config.getValue("test") is "1":
    import mock.roof_control as roof_control
else:
    import roof_control

HOST = config.Config.getValue("ip", "server")  # The server's hostname or IP address
PORT = config.Config.getInt("port", "server")        # The port used by the server

g_ui = gui.Gui()
roof = False
curtains = False
error = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        ev1, vals1 = g_ui.win.Read(timeout=10000)

        if ev1 is None or ev1 == "exit":
            v = "E"

        elif error:
            continue

        elif ev1 == 'open-roof':
            v = "R"

        elif ev1 == 'close-roof':
            if curtains is True:
                g_ui.roof_alert('Attenzione tendine aperte')
                continue
            v = "T"

        elif ev1 == 'start-curtains':
            if roof is False:
                g_ui.roof_alert('Attenzione tetto chiuso')
                continue

            g_ui.base_draw()
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
        rcv = s.recv(6)
        if ev1 is None or ev1 == "exit" or ev1 == "shutdown":
            s.close()
            break
        data = rcv.decode("UTF-8")
        print("Data: "+data)
        if data[0] == "R":
            if data[-1] == "1":
                roof = True
                g_ui.open_roof("Tetto Aperto")
            elif data[-1] == "0":
                roof = False
                g_ui.closed_roof("Tetto Chiuso")
        elif data[0] == "E":
            # la if si potrebbe togliere, l'errore dovrebbe sempre essere bloccante
            # ma va testato meglio
            if data != "E0000S":
                g_ui.roof_alert('Attenzione Errore Bloccante!')
                error = True
        else:
            if data == "000000":
                curtains = False
            else:
                curtains = True
            alpha_e, alpha_w = g_ui.update_curtains_text(int(data[0:3]), int(data[3:6]))
            g_ui.update_curtains_graphic(alpha_e, alpha_w)


exit(0)
