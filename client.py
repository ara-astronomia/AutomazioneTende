import PySimpleGUI as sg
import time, config, socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 3000        # The port used by the server

sg.ChangeLookAndFeel('GreenTan')
# Design pattern 1 - First window does not remain active
n_step_corsa_tot = int(config.Config.getValue('n_step_corsa_tot', "encoder_step"))
menu_def = [['File', ['Exit']],
            ['Help', 'About...']]
layout = [[sg.Menu(menu_def, tearoff=True)],
         [sg.Text('Controllo movimento tende ', size=(30, 1), justification='center', font=("Helvetica", 15), relief=sg.RELIEF_RIDGE)],
         [sg.Text('altezza telescopio')],
         [sg.ProgressBar(n_step_corsa_tot, orientation='h', size=(20, 20), key='progbar_e')],
         [sg.ProgressBar(n_step_corsa_tot, orientation='h', size=(20, 20), key='progbar_w')],
         [sg.Button('StartCurtains')],[sg.Button('StopCurtains')]]

if config.Config.getValue("test") is "1":
    layout.append([sg.Button('Shutdown')])

win1 = sg.Window('Controllo tende Osservatorio').Layout(layout)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        ev1, vals1 = win1.Read(timeout=10)
        if ev1 is None or ev1 == "Exit":
            v = b"E"
        if ev1 == 'StartCurtains':
            v = b"1"
        elif ev1 == 'StopCurtains':
            v = b"0"
        elif ev1 == "Shutdown":
            v = b"-"
        else:
            v = b"c"
        s.sendall(v)
        rcv = s.recv(6)
        if ev1 is None or ev1 == "Exit" or ev1 == "Shutdown":
            s.close()
            break
        data = rcv.decode("UTF-8")
        win1.FindElement('progbar_e').UpdateBar(int(data[0:3]))
        win1.FindElement('progbar_w').UpdateBar(int(data[3:6]))

exit(0)
