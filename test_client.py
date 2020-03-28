import time, config, socket
from electro_tests import gui
from gui_constants import GuiKey
from logger import Logger
from crac_status import CracStatus
from status import Status, TelescopeStatus

def connection() -> str:
    # crac_status = CracStatus()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        win = gui.create_win()
        while True:
            v, values = win.Read(timeout=5000)

            roof = "C"
            curtain_west = "C"
            curtain_east = "C"

            if values:

                for k, value in values.items():
                    if value:
                        if k == "RO":
                            roof = "O"
                        elif k == "RC":
                            roof = "C"
                        elif k == "WO":
                            curtain_west = "O"
                        elif k == "WC":
                            curtain_west = "C"
                        elif k == "EO":
                            curtain_east = "O"
                        elif k == "EC":
                            curtain_east = "C"
                    
            code = roof + curtain_west + curtain_east

            Logger.getLogger().debug("Code: %s", code)

            s.sendall(code.encode("UTF-8"))
            
            rcv = s.recv(16)

            data = rcv.decode("UTF-8")
            Logger.getLogger().debug("Data: %s", data)
            crac_status = CracStatus(data)
            Logger.getLogger().debug("CRAC_STATUS: %s", crac_status)

            if v is GuiKey.EXIT or v is GuiKey.SHUTDOWN:
                s.close()
                return GuiKey.EXIT

            # # ROOF
            # if crac_status.roof_status == Status.OPEN:
            #     # g_ui.show_background_image()
            #     # g_ui.update_status_roof(GuiLabel.ROOF_OPEN, text_color="#2c2825", background_color="green")
            #     # g_ui.update_enable_disable_button()
            #     pass

            # elif crac_status.roof_status == Status.CLOSED:
            #     # g_ui.hide_background_image()
            #     # g_ui.update_status_roof(GuiLabel.ROOF_CLOSED)
            #     # g_ui.update_enable_button_open_roof()
            #     pass

            # # TELESCOPE
            # if crac_status.telescope_status == TelescopeStatus.PARKED:
            #     Logger.getLogger().info("telescopio in park")
            #     # g_ui.update_status_tele(GuiLabel.TELESCOPE_PARKED)

            # elif crac_status.telescope_status == TelescopeStatus.SECURE:
            #     Logger.getLogger().info("telescopio in sicurezza ")
            #     # g_ui.update_status_tele(GuiLabel.TELESCOPE_SECURED)

            # elif crac_status.telescope_status == TelescopeStatus.LOST:
            #     Logger.getLogger().info("telescopio ha perso la conessione con thesky ")
            #     # g_ui.update_status_tele(GuiLabel.TELESCOPE_ANOMALY)
            #     # g_ui.status_alert(GuiLabel.ALERT_THE_SKY_LOST)
            
            # elif crac_status.telescope_status == TelescopeStatus.ERROR:
            #     Logger.getLogger().info("telescopio ha ricevuto un errore da the sky ")
            #     # g_ui.update_status_tele(GuiLabel.TELESCOPE_ERROR)
            #     # g_ui.status_alert(GuiLabel.ALERT_THE_SKY_ERROR)

            # else:
            #     Logger.getLogger().info("telescopio operativo")
            #     # g_ui.update_status_tele(GuiLabel.TELESCOPE_OPERATIVE, text_color="#2c2825", background_color="green")

            # # CURTAINS
            # if crac_status.are_curtains_in_danger():
            #     # g_ui.update_status_curtains(GuiLabel.CURTAINS_ANOMALY)
            #     # g_ui.status_alert(GuiLabel.ALERT_CHECK_CURTAINS_SWITCH)
            #     pass

            # elif crac_status.are_curtains_closed():
            #     # g_ui.update_status_curtains(GuiLabel.CURTAINS_CLOSED)
            #     pass

            # else:
            #     # g_ui.update_status_curtains(GuiLabel.CURTAINS_OPEN, text_color="#2c2825", background_color="green")
            #     # g_ui.update_disable_button_close_roof()
            #     pass

            # # ALERT
            # if crac_status.is_in_anomaly():
            #     # g_ui.status_alert(GuiLabel.ALERT_CRAC_ANOMALY)
            #     pass
            
            # elif crac_status.telescope_in_secure_and_roof_is_closed():
            #     # Logger.getLogger().info("telescopio > park e tetto chiuso")
            #     # g_ui.status_alert(GuiLabel.ALERT_TELESCOPE_ROOF)
            #     pass

            # elif crac_status.telescope_in_secure_and_roof_is_closed():
            #     # Logger.getLogger().info("telescopio > park e tetto in chiusura")
            #     # g_ui.status_alert(GuiLabel.ALERT_TELESCOPE_ROOF_CLOSING)
            #     pass

            # else:
            #     Logger.getLogger().info("Tutto ok")
            #     # g_ui.status_alert(GuiLabel.NO_ALERT)

            # alpha_e, alpha_w = g_ui.update_curtains_text(int(crac_status.curtain_east_steps), int(crac_status.curtain_west_steps))
            # g_ui.update_curtains_graphic(alpha_e, alpha_w)
            # g_ui.update_tele_text(crac_status.telescope_coords)

HOST = config.Config.getValue("ip", "server")  # The server's hostname or IP address
PORT = config.Config.getInt("port", "server")  # The port used by the server

while True:
    Logger.getLogger().debug("connessione a: " + HOST + ":" + str(PORT))
    key = connection()
    if key == "E":
        exit(0)
