import socket

import config

from electro_tests import gui
from gui_constants import GuiKey
from logger import LoggerClient
from status import ButtonStatus


def change_status(status_switch, key, win):
    if status_switch == "0":
        win.Find(key).update('On', text_color='white', background_color='green')
    elif status_switch == "1":
        win.Find(key).update('Off', text_color='white', background_color='red')


def change_status_button(status_button, key, win):
    status_button = ButtonStatus
    if status_button == "S":
        win.Find(key).update(disabled=True, text_color='white', background_color='green')
    elif status_button == "A":
        win.Find(key).update(disabled=False, text_color='yellow', background_color='purple')


def change_encoder(count, key, win):
    if count:
        win.Find(key).update(count, text_color='white', background_color='green')


def connection() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        win = gui.create_win()

        while True:
            v, values = win.Read(timeout=500)

            if not v:
                s.close()
                return GuiKey.EXIT

            roof = "S"
            curtain_west = "S"
            curtain_east = "S"
            panel = "S"
            power_tele = "S"
            light = "S"
            power_ccd = "S"

            for k, value in values.items():
                if value:
                    if k == "RO":
                        roof = "O"
                    elif k == "RC":
                        roof = "C"

                    elif k == GuiKey.PANEL_ON:
                        panel = "A"
                    elif k == GuiKey.PANEL_OFF:
                        panel = "S"

                    elif k is GuiKey.POWER_ON_TELE:
                        power_tele = "A"
                    elif k is GuiKey.POWER_OFF_TELE:
                        power_tele = "S"

                    elif k is GuiKey.LIGHT_ON:
                        light = "A"
                    elif k is GuiKey.LIGHT_OFF:
                        light = "S"

                    elif k is GuiKey.POWER_ON_CCD:
                        power_ccd = "A"
                    elif k is GuiKey.POWER_OFF_CCD:
                        power_ccd = "S"

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

            code = roof + panel + power_tele + light + power_ccd + curtain_west + curtain_east

            LoggerClient.getLogger().debug("Code: %s", code)

            s.sendall(code.encode("UTF-8"))

            rcv = s.recv(17)

            data = rcv.decode("UTF-8")
            LoggerClient.getLogger().debug("Data: %s", data)

            # # ROOF
            change_status(data[3], "Roof_open", win)
            change_status(data[4], "Roof_closed", win)

            # #CURTAINS W
            change_status(data[5], "Curtain_W_is_open", win)
            change_status(data[6], "Curtain_W_is_closed", win)

            # #CURTAINS W
            change_status(data[7], "Curtain_E_is_open", win)
            change_status(data[8], "Curtain_E_is_closed", win)

            change_encoder(data[9:13], "Count_W", win)
            change_encoder(data[13:], "Count_E", win)


# The server's hostname or IP address
HOST = config.Config.getValue("ip", "server")
# The port used by the server
PORT = config.Config.getInt("port", "server")

while True:
    LoggerClient.getLogger().debug("connessione a: " + HOST + ":" + str(PORT))
    key = connection()
    if key == "E":
        exit(0)
