import gui
import time
import socket
import config
import crac_status
from gui_constants import GuiLabel, GuiKey
from logger import LoggerClient
from status import Status, CurtainsStatus, TelescopeStatus, ButtonStatus, TrackingStatus


def connection() -> str:
    cs = crac_status.CracStatus()
    LoggerClient.getLogger().debug("Data cs start connection method: %s", cs)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            v, _ = g_ui.win.Read(timeout=5000)

            LoggerClient.getLogger().info("e' stato premuto il tasto %s", v)

            if v is None:
                v = GuiKey.EXIT

            elif v is GuiKey.TIMEOUT:
                v = GuiKey.CONTINUE

            elif v is GuiKey.CLOSE_ROOF:
                if crac_status.curtain_east_status is CurtainsStatus.ENABLED or crac_status.curtain_west_status is CurtainsStatus.ENABLED:
                    g_ui.status_alert(GuiLabel.ALERT_CURTAINS_ENABLED)
                    continue

                if cs.telescope_status >= TelescopeStatus.NORTHEAST:
                    g_ui.status_alert(GuiLabel.ALERT_TELESCOPE_OPERATIVE.format(status=cs.telescope_status))
                    continue

            elif v is GuiKey.ENABLED_CURTAINS:
                if crac_status.roof_status is Status.CLOSED:
                    g_ui.status_alert(GuiLabel.ALERT_ROOF_CLOSED)
                    continue

            LoggerClient.getLogger().info("invio paramentri con sendall: %s", v.encode("utf-8"))
            s.sendall(v.encode("utf-8"))

            rcv = s.recv(cs.lenght())
            data = rcv.decode("utf-8")
            cs = crac_status.CracStatus(data)
            LoggerClient.getLogger().debug("Data cs in the middle of connection method: %s", cs)

            if v is GuiKey.EXIT or v is GuiKey.SHUTDOWN:
                s.close()
                return GuiKey.EXIT

            # ROOF
            if cs.roof_status == Status.OPEN:
                g_ui.show_background_image()
                g_ui.update_status_roof(GuiLabel.ROOF_OPEN, text_color="#2c2825", background_color="green")
                g_ui.update_enable_disable_button()

            elif cs.roof_status == Status.CLOSED:
                g_ui.hide_background_image()
                g_ui.update_status_roof(GuiLabel.ROOF_CLOSED)
                g_ui.update_enable_button_open_roof()

            # TELESCOPE
            if cs.telescope_status == TelescopeStatus.PARKED:
                LoggerClient.getLogger().info("telescopio in park")
                g_ui.update_status_tele(GuiLabel.TELESCOPE_PARKED, text_color="red", background_color="white")

            elif cs.telescope_status == TelescopeStatus.FLATTER:
                LoggerClient.getLogger().info("telescopio in flat")
                g_ui.update_status_tele(GuiLabel.TELESCOPE_FLATTER, text_color="red", background_color="white")

            elif cs.telescope_status == TelescopeStatus.FLATTER:
                LoggerClient.getLogger().info("telescopio in flat")
                g_ui.update_status_tele(GuiLabel.TELESCOPE_FLATTER)

            elif cs.telescope_status == TelescopeStatus.SECURE:
                LoggerClient.getLogger().info("telescopio in sicurezza ")
                g_ui.update_status_tele(GuiLabel.TELESCOPE_SECURED, text_color="red", background_color="white")

            elif cs.telescope_status == TelescopeStatus.LOST:
                LoggerClient.getLogger().info("telescopio ha perso la conessione con thesky ")
                g_ui.update_status_tele(GuiLabel.TELESCOPE_ANOMALY)
                g_ui.status_alert(GuiLabel.ALERT_THE_SKY_LOST)

            elif cs.telescope_status == TelescopeStatus.ERROR:
                LoggerClient.getLogger().info("telescopio ha ricevuto un errore da the sky ")
                g_ui.update_status_tele(GuiLabel.TELESCOPE_ERROR)
                g_ui.status_alert(GuiLabel.ALERT_THE_SKY_ERROR)

            else:
                cardinal = vars(GuiLabel).get(f"TELESCOPE_{cs.telescope_status.abbr}")
                LoggerClient.getLogger().info("telescopio operativo: %s", cardinal)
                g_ui.update_status_tele(cardinal, text_color="#2c2825", background_color="green")

            # CURTAINS
            if cs.are_curtains_in_danger():
                g_ui.update_status_curtains(GuiLabel.CURTAINS_ANOMALY)
                g_ui.status_alert(GuiLabel.ALERT_CHECK_CURTAINS_SWITCH)

            elif crac_status.are_curtains_closed():
                g_ui.update_status_curtains(GuiLabel.CURTAINS_DISABLED)
                g_ui.update_disable_button_deactive_curtains()

            else:
                g_ui.update_status_curtains(GuiLabel.CURTAINS_ACTIVED, text_color="#2c2825", background_color="green")
                g_ui.update_disable_button_close_roof()

            # PANEL FLAT
            if cs.panel_status == ButtonStatus.ON:
                LoggerClient.getLogger().info("pannello flat acceso")
                g_ui.update_disable_button_on()

            if cs.panel_status == ButtonStatus.OFF:
                LoggerClient.getLogger().info("pannello flat spento")
                g_ui.update_disable_button_off()

            # POWER SWITCH
            if cs.power_status == ButtonStatus.ON:
                LoggerClient.getLogger().info("Alimentari accesi")
                g_ui.update_disable_button_power_switch_on()

            if cs.power_status == ButtonStatus.OFF:
                LoggerClient.getLogger().info("Alimentatori spenti")
                g_ui.update_disable_button_power_switch_off()

            # LIGHT DOME
            if cs.light_status == ButtonStatus.ON:
                LoggerClient.getLogger().info("Luci cupola acccese")
                g_ui.update_disable_button_light_on()

            if cs.light_status == ButtonStatus.OFF:
                LoggerClient.getLogger().info("Luci cupola spente")
                g_ui.update_disable_button_light_off()

            # AUXILIARY
            if cs.aux_status == ButtonStatus.ON:
                LoggerClient.getLogger().info("ausiliare acceso")
                g_ui.update_disable_button_aux_on()

            if cs.aux_status == ButtonStatus.OFF:
                LoggerClient.getLogger().info("ausiliare spento")
                g_ui.update_disable_button_aux_off()


            # TRACKING
            if cs.tracking_status == TrackingStatus.ON:
                g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_ON, text_color="#2c2825", background_color="green")
            elif cs.tracking_status == TrackingStatus.OFF:
                g_ui.update_status_tracking(GuiLabel.TELESCOPE_TRACKING_OFF, text_color="red", background_color="white")

            # ALERT
            if cs.is_in_anomaly():
                g_ui.status_alert(GuiLabel.ALERT_CRAC_ANOMALY)

            elif cs.telescope_in_secure_and_roof_is_closed():
                LoggerClient.getLogger().info("telescopio > park e tetto chiuso")
                g_ui.status_alert(GuiLabel.ALERT_TELESCOPE_ROOF)

            elif cs.telescope_in_secure_and_roof_is_closed():
                LoggerClient.getLogger().info("telescopio > park e tetto in chiusura")
                g_ui.status_alert(GuiLabel.ALERT_TELESCOPE_ROOF_CLOSING)

            else:
                LoggerClient.getLogger().info(GuiLabel.NO_ALERT)
                g_ui.status_alert(GuiLabel.NO_ALERT)

            alpha_e, alpha_w = g_ui.update_curtains_text(int(cs.curtain_east_steps), int(cs.curtain_west_steps))
            g_ui.update_curtains_graphic(alpha_e, alpha_w)
            g_ui.update_tele_text(cs.telescope_coords)


crac_status.APP = "CLIENT"
# The server's hostname or IP address
HOST = config.Config.getValue("ip", "server")
# The server's hostname or IP address
PORT = config.Config.getInt("port", "server")

g_ui = gui.Gui()

while True:
    LoggerClient.getLogger().debug("connessione a: " + HOST + ":" + str(PORT))
    key = connection()
    if key == "E":
        exit(0)
