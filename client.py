import PySimpleGUI as sg
import time, config, socket, gui
if config.Config.getValue("test") is "1":
    import mock.roof_control as roof_control
else:
    import roof_control

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 3000        # The port used by the server

g_ui = gui.Gui()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        ev1, vals1 = g_ui.win.Read(timeout=10)
        if ev1 is None or ev1 == "exit":
            v = b"E"

        elif ev1 == 'open-roof':
            status_roof=roof_control.verify_closed_roof()
            g_ui.update_status_roof(status_roof[1])
            if status_roof[0] == 1:
                status_roof = 'Tetto in fase di apertura'
                g_ui.update_status_roof(status_roof)
                roof_control.open_roof()
                status_roof=roof_control.open_roof()
                if status_roof[0] == 0:
                    g_ui.open_roof(status_roof[1])

        elif ev1 == 'close-roof':
            if alpha_e and alpha_w !=0:
                g_ui.roof_alert('Attenzione chiudere le tende')
            else:
                status_roof=roof_control.verify_open_roof()
                g_ui.update_status_roof(status_roof[1])
                if status_roof[0] == 0:
                    status_roof = 'Tetto in fase di chiusura'
                    g_ui.update_status_roof(status_roof)
                    roof_control.closed_roof()
                    status_roof=roof_control.closed_roof()
                    if status_roof[0] == 1:
                        g_ui.closed_roof(status_roof[1])


            continue
        elif ev1 == 'start-curtains':
            if vals1['aperturatetto']=='Tetto chiuso' or vals1['aperturatetto']=='Stato del tetto' :
                g_ui.roof_alert('Attenzione tetto chiuso')

                continue

            g_ui.base_draw()
            v = b"1"

        elif ev1 == 'stop-curtains':
            v = b"0"

        elif ev1 == "shutdown":
            v = b"-"
        else:
            v = b"c"
        s.sendall(v)
        rcv = s.recv(6)
        if ev1 is None or ev1 == "exit" or ev1 == "shutdown":
            s.close()
            break
        data = rcv.decode("UTF-8")
        print("Data: "+data)
        alpha_e, alpha_w = g_ui.update_curtains_text(int(data[0:3]), int(data[3:6]))
        g_ui.update_curtains_graphic(alpha_e, alpha_w)


exit(0)
