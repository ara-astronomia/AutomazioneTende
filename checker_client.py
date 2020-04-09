import time, config, socket
from electro_tests import gui
from gui_constants import GuiKey,GuiLabel
from logger import Logger
from crac_status import CracStatus
from status import Status, TelescopeStatus

def change_status(status_switch, key, win):
    if status_switch == "1":
        win.Find(key).update('Attivo', text_color='white', background_color='green')
    elif status_switch == "0":
        win.Find(key).update('Disattivo', text_color='white', background_color='red')

def connection() -> str:
    # crac_status = CracStatus()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        win = gui.create_win()

        while True:
            v, values = win.Read(timeout=2000)

            roof = "S"
            curtain_west = "S"
            curtain_east = "S"

            if values:

                for k, value in values.items():
                    if value:
                        if k == "RO":
                            roof = "O"
                        elif k == "RC":
                            roof = "C"
                        elif k == "RS":
                            roof = "S"

                        elif k == "WO":
                            curtain_west = "O"
                        elif k == "WC":
                            curtain_west = "C"
                        elif k == "WS":
                            curtain_west = "S"

                        elif k == "EO":
                            curtain_east = "O"
                        elif k == "EC":
                            curtain_east = "C"
                        elif k == "ES":
                            curtain_east = "S"

            code = roof + curtain_west + curtain_east

            Logger.getLogger().debug("Code: %s", code)

            s.sendall(code.encode("UTF-8"))

            rcv = s.recv(9)

            data = rcv.decode("UTF-8")
            Logger.getLogger().debug("Data: %s", data)
            crac_status = CracStatus(data)
            Logger.getLogger().debug("CRAC_STATUS: %s", crac_status)

            # # ROOF
            change_status(data[3], "Roof_open", win)
            change_status(data[4], "Roof_closed", win)

            # #CURTAINS W
            change_status(data[5], "Curtain_W_is_open", win)
            change_status(data[6], "Curtain_W_is_closed", win)

            # #CURTAINS W
            change_status(data[7], "Curtain_E_is_open", win)
            change_status(data[8], "Curtain_E_is_closed", win)

            if not v or v is GuiKey.EXIT or v is GuiKey.SHUTDOWN:
                s.close()
                return GuiKey.EXIT

        

HOST = config.Config.getValue("ip", "server")  # The server's hostname or IP address
PORT = config.Config.getInt("port", "server")  # The port used by the server

while True:
    Logger.getLogger().debug("connessione a: " + HOST + ":" + str(PORT))
    key = connection()
    if key == "E":
        exit(0)
