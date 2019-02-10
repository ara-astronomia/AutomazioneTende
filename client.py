import PySimpleGUI as sg
import time, config, socket, gui

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
            g_ui.open_roof()
            continue
        elif ev1 == 'close-roof':
            continue
        elif ev1 == 'start-curtains':
            if vals1['aperturatetto']=='Tetto chiuso':
                g_ui.closed_roof_alert()
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
