import time, config, socket, gui
from logger import Logger
from crac_status import CracStatus
from status import Status, TelescopeStatus, PanelStatus
from gui_constants import GuiLabel, GuiKey

def connection() -> str:
    crac_status = CracStatus()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            v, _ = g_ui.win.Read(timeout=10000)

            Logger.getLogger().info("e' stato premuto il tasto %s", v)

            if v is None:
                v = GuiKey.EXIT

            elif v is GuiKey.TIMEOUT:
                v = GuiKey.CONTINUE

            elif v is GuiKey.CLOSE_ROOF:
                if crac_status.curtain_east_status > Status.CLOSED or crac_status.curtain_west_status > Status.CLOSED:
                    g_ui.status_alert(GuiLabel.ALERT_CURTAINS_OPEN)
                    continue

                if crac_status.telescope_status is TelescopeStatus.OPERATIONAL:
                    g_ui.status_alert(GuiLabel.ALERT_TELESCOPE_OPERATIVE)
                    continue

            elif v is GuiKey.START_CURTAINS:
                if crac_status.roof_status is Status.CLOSED:
                    g_ui.status_alert(GuiLabel.ALERT_ROOF_CLOSED)
                    continue

            Logger.getLogger().info("invio paramentri con sendall: %s", v.encode("UTF-8"))
            s.sendall(v.encode("UTF-8"))
            rcv = s.recv(17)

            data = rcv.decode("UTF-8")
            crac_status = CracStatus(data)
            Logger.getLogger().debug("Data: %s", crac_status)

            if v is GuiKey.EXIT or v is GuiKey.SHUTDOWN:
                s.close()
                return GuiKey.EXIT

            # ROOF
            if crac_status.roof_status == Status.OPEN:
                g_ui.show_background_image()
                g_ui.update_status_roof(GuiLabel.ROOF_OPEN, text_color="#2c2825", background_color="green")
                g_ui.update_enable_disable_button()

            elif crac_status.roof_status == Status.CLOSED:
                g_ui.hide_background_image()
                g_ui.update_status_roof(GuiLabel.ROOF_CLOSED)
                g_ui.update_enable_button_open_roof()

            # TELESCOPE
            if crac_status.telescope_status == TelescopeStatus.PARKED:
                Logger.getLogger().info("telescopio in park")
                g_ui.update_status_tele(GuiLabel.TELESCOPE_PARKED)

            elif crac_status.telescope_status == TelescopeStatus.FLATTER:
                Logger.getLogger().info("telescopio in flat")
                g_ui.update_status_tele(GuiLabel.TELESCOPE_FLATTER)

            elif crac_status.telescope_status == TelescopeStatus.SECURE:
                Logger.getLogger().info("telescopio in sicurezza ")
                g_ui.update_status_tele(GuiLabel.TELESCOPE_SECURED)

            elif crac_status.telescope_status == TelescopeStatus.LOST:
                Logger.getLogger().info("telescopio ha perso la conessione con thesky ")
                g_ui.update_status_tele(GuiLabel.TELESCOPE_ANOMALY)
                g_ui.status_alert(GuiLabel.ALERT_THE_SKY_LOST)

            elif crac_status.telescope_status == TelescopeStatus.ERROR:
                Logger.getLogger().info("telescopio ha ricevuto un errore da the sky ")
                g_ui.update_status_tele(GuiLabel.TELESCOPE_ERROR)
                g_ui.status_alert(GuiLabel.ALERT_THE_SKY_ERROR)

            else:
                Logger.getLogger().info("telescopio operativo")
                g_ui.update_status_tele(GuiLabel.TELESCOPE_OPERATIVE, text_color="#2c2825", background_color="green")

            # CURTAINS
            if crac_status.are_curtains_in_danger():
                g_ui.update_status_curtains(GuiLabel.CURTAINS_ANOMALY)
                g_ui.status_alert(GuiLabel.ALERT_CHECK_CURTAINS_SWITCH)

            elif crac_status.are_curtains_closed():
                g_ui.update_status_curtains(GuiLabel.CURTAINS_CLOSED)

            else:
                g_ui.update_status_curtains(GuiLabel.CURTAINS_OPEN, text_color="#2c2825", background_color="green")
                g_ui.update_disable_button_close_roof()

            #PANEL FLAT
            if crac_status.panel_status == PanelStatus.ON:
                Logger.getLogger().info("pannello flat acceso")
                g_ui.update_status_panel(GuiLabel.PANEL_ON, text_color="#2c2825", background_color="green")
                g_ui.update_disable_button_panel_on()
                g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_ON, text_color="#2c2825", background_color="green")

            if crac_status.panel_status == PanelStatus.OFF:
                Logger.getLogger().info("pannello flat spento")
                g_ui.update_status_panel(GuiLabel.PANEL_OFF)
                g_ui.update_disable_button_panel_off()
                g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_OFF)

            #TRACKING

            # ALERT
            if crac_status.is_in_anomaly():
                g_ui.status_alert(GuiLabel.ALERT_CRAC_ANOMALY)

            elif crac_status.telescope_in_secure_and_roof_is_closed():
                Logger.getLogger().info("telescopio > park e tetto chiuso")
                g_ui.status_alert(GuiLabel.ALERT_TELESCOPE_ROOF)

            elif crac_status.telescope_in_secure_and_roof_is_closed():
                Logger.getLogger().info("telescopio > park e tetto in chiusura")
                g_ui.status_alert(GuiLabel.ALERT_TELESCOPE_ROOF_CLOSING)

            else:
                Logger.getLogger().info(GuiLabel.NO_ALERT)
                g_ui.status_alert(GuiLabel.NO_ALERT)

            alpha_e, alpha_w = g_ui.update_curtains_text(int(crac_status.curtain_east_steps), int(crac_status.curtain_west_steps))
            g_ui.update_curtains_graphic(alpha_e, alpha_w)
            g_ui.update_tele_text(crac_status.telescope_coords)

HOST = config.Config.getValue("ip", "server")  # The server's hostname or IP address
PORT = config.Config.getInt("port", "server")  # The port used by the server

g_ui = gui.Gui()

while True:
    Logger.getLogger().debug("connessione a: " + HOST + ":" + str(PORT))
    key = connection()
    if key == "E":
        exit(0)
