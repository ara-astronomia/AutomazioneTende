import socket
import time
import config
import crac_status
import gui
from gui_constants import GuiLabel, GuiKey
from logger import LoggerClient
from status import Status, CurtainsStatus, TelescopeStatus
from status import ButtonStatus, TrackingStatus


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
                if cs.curtain_east_status > CurtainsStatus.DISABLED or cs.curtain_west_status > CurtainsStatus.DISABLED:
                    g_ui.status_alert(GuiLabel.ALERT_CURTAINS_ENABLED)
                    continue

                if cs.telescope_status >= TelescopeStatus.NORTHEAST:
                    g_ui.status_alert(GuiLabel.ALERT_TELESCOPE_OPERATIVE.format(status=cs.telescope_status))
                    continue

            elif v is GuiKey.ENABLED_CURTAINS:
                if cs.roof_status is Status.CLOSED:
                    g_ui.status_alert(GuiLabel.ALERT_ROOF_CLOSED)
                    continue

            LoggerClient.getLogger().info("invio paramentri con sendall: %s", v.encode("utf-8"))
            s.sendall(v.encode("utf-8"))

            rcv = s.recv(cs.length)
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
            if cs.curtain_east_status is CurtainsStatus.DISABLED and cs.curtain_west_status is CurtainsStatus.DISABLED:
                g_ui.update_status_curtain_east(GuiLabel.CURTAINS_DISABLED)
                g_ui.update_status_curtain_west(GuiLabel.CURTAINS_DISABLED)
                g_ui.update_disable_button_disabled_curtains()

            else:
                if cs.curtain_east_status in [CurtainsStatus.ERROR, CurtainsStatus.DANGER]:
                    g_ui.update_status_curtain_east(GuiLabel.CURTAINS_ANOMALY)
                    g_ui.update_disable_button_close_roof()
                    g_ui.status_alert(GuiLabel.ALERT_CHECK_CURTAINS_SWITCH)

                elif cs.curtain_east_status is CurtainsStatus.CLOSED:
                    g_ui.update_status_curtain_east(GuiLabel.CURTAINS_CLOSED, text_color="#2c2825", background_color="green")
                    g_ui.update_disable_button_close_roof()

                elif cs.curtain_east_status is CurtainsStatus.STOPPED:
                    g_ui.update_status_curtain_east(GuiLabel.CURTAINS_STOPPED, text_color="#2c2825", background_color="green")
                    g_ui.update_disable_button_close_roof()

                elif cs.curtain_east_status is CurtainsStatus.OPEN:
                    g_ui.update_status_curtain_east(GuiLabel.CURTAINS_OPEN, text_color="#2c2825", background_color="green")
                    g_ui.update_disable_button_close_roof()

                if cs.curtain_west_status in [CurtainsStatus.ERROR, CurtainsStatus.DANGER]:
                    g_ui.update_status_curtain_west(GuiLabel.CURTAINS_ANOMALY)
                    g_ui.update_disable_button_close_roof()
                    g_ui.status_alert(GuiLabel.ALERT_CHECK_CURTAINS_SWITCH)

                elif cs.curtain_west_status is CurtainsStatus.CLOSED:
                    g_ui.update_status_curtain_west(GuiLabel.CURTAINS_CLOSED, text_color="#2c2825", background_color="green")
                    g_ui.update_disable_button_close_roof()

                elif cs.curtain_west_status is CurtainsStatus.STOPPED:
                    g_ui.update_status_curtain_west(GuiLabel.CURTAINS_STOPPED, text_color="#2c2825", background_color="green")
                    g_ui.update_disable_button_close_roof()

                elif cs.curtain_west_status is CurtainsStatus.OPEN:
                    g_ui.update_status_curtain_west(GuiLabel.CURTAINS_OPEN, text_color="#2c2825", background_color="green")
                    g_ui.update_disable_button_close_roof()

            # PANEL FLAT
            if cs.telescope_status not in [TelescopeStatus.SECURE, TelescopeStatus.FLATTER]:
                LoggerClient.getLogger().info("pannello flat disattivato")
                g_ui.update_disable_panel_all()

            elif cs.panel_status is ButtonStatus.ON:
                LoggerClient.getLogger().info("pannello flat acceso")
                g_ui.update_disable_panel_on()

            elif cs.panel_status is ButtonStatus.OFF:
                LoggerClient.getLogger().info("pannello flat spento")
                g_ui.update_disable_panel_off()

            # POWER SWITCH
            if cs.power_tele_status == ButtonStatus.ON:
                LoggerClient.getLogger().info("Alimentari accesi")
                g_ui.update_disable_button_power_switch_on()

            if cs.power_tele_status == ButtonStatus.OFF:
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
            if cs.power_ccd_status == ButtonStatus.ON:
                LoggerClient.getLogger().info("ausiliare acceso")
                g_ui.update_disable_button_power_on_ccd()

            if cs.power_ccd_status == ButtonStatus.OFF:
                LoggerClient.getLogger().info("ausiliare spento")
                g_ui.update_disable_button_power_off_ccd()

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
