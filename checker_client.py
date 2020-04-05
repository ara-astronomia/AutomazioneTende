import time, config, socket
from electro_tests import gui
from gui_constants import GuiKey,GuiLabel
from logger import Logger
from crac_status import CracStatus
from status import Status, TelescopeStatus

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

            rcv = s.recv(3)

            data = rcv.decode("UTF-8")
            Logger.getLogger().debug("Data: %s", data)
            crac_status = CracStatus(data)
            Logger.getLogger().debug("CRAC_STATUS: %s", crac_status)

            if not v or v is GuiKey.EXIT or v is GuiKey.SHUTDOWN:
                s.close()
                return GuiKey.EXIT

            # # ROOF
            # if crac_status.roof_status == Status.OPEN:
            #     win.Find("Roof_open").update('Aperto', text_color='white', background_color='green')
            #     Logger.getLogger().info("tetto aperto")
            # else:
            #     win.Find("Roof_open").update('stand-by',background_color="white",text_color = 'DarkBlue')

            # if crac_status.roof_status == Status.CLOSED:
            #     win.Find("Roof_closed").update('Chiuso', text_color='white', background_color='green')
            #     Logger.getLogger().info("tetto chiuso")
            # else:
            #     win.Find("Roof_closed").update('stand-by',background_color="white",text_color = 'DarkBlue')

            # #CURTAINS
            # # GLI IF DI QUESTE CONDIIONI VANNO SOSTITUITI CON QUELLI ADATTI ALLA LETTURA DELLO STATO DEL PIN DEGLI STATUS CORRISPONDENTI
            # #CURTAIN WEST
            # if crac_status.curtain_west_status == Status.OPEN:
            #     win.Find("Curtain_W_is_open").update('Aperta', text_color='white', background_color='green')
            #     Logger.getLogger().info("tenda west aperta")
            # else:
            #     win.Find("Curtain_W_is_open").update('stand_by', background_color="white",text_color = 'DarkBlue')
            #     Logger.getLogger().info("tenda west in stan_by")

            # if crac_status.curtain_west_status == Status.CLOSED:
            #     win.Find("Curtain_W_is_closed").update('Chiusa', text_color='white', background_color='green')
            #     Logger.getLogger().info("tenda west chiusa")
            # else:
            #     win.Find("Curtain_W_is_closed").update('stand_by', background_color="white",text_color = 'DarkBlue')
            #     Logger.getLogger().info("tenda west in stan_by")

            # if crac_status.curtain_west_status == Status.STOPPED:
            #     win.Find("Curtain_W_is_open").update('stand_by', background_color="white",text_color = 'DarkBlue',)
            #     win.Find("Curtain_W_is_closed").update('stand_by', background_color="white",text_color = 'DarkBlue',)
            #     Logger.getLogger().info("tenda est in attesa")


            # #CURTAIN EAST
            # if crac_status.curtain_east_status == Status.OPEN:
            #     win.Find("Curtain_E_is_open").update('Aperta', text_color='white', background_color='green')
            #     Logger.getLogger().info("tenda est aperta")
            # else:
            #     win.Find("Curtain_E_is_open").update('stand_by', background_color="white",text_color = 'DarkBlue')
            #     Logger.getLogger().info("tenda est in stan_by")

            # if crac_status.curtain_east_status == Status.CLOSED:
            #     win.Find("Curtain_E_is_closed").update('Chiusa', text_color='white', background_color='green')
            #     Logger.getLogger().info("tenda est chiusa")
            # else:
            #     win.Find("Curtain_E_is_closed").update('stand_by', background_color="white",text_color = 'DarkBlue')
            #     Logger.getLogger().info("tenda est in stan_by")

            # if crac_status.curtain_east_status == Status.STOPPED:
            #     win.Find("Curtain_E_is_open").update('stand_by', background_color="white",text_color = 'DarkBlue',)
            #     win.Find("Curtain_E_is_closed").update('stand_by', background_color="white",text_color = 'DarkBlue',)
            #     Logger.getLogger().info("tenda est in attesa")
            

HOST = config.Config.getValue("ip", "server")  # The server's hostname or IP address
PORT = config.Config.getInt("port", "server")  # The port used by the server

while True:
    Logger.getLogger().debug("connessione a: " + HOST + ":" + str(PORT))
    key = connection()
    if key == "E":
        exit(0)
