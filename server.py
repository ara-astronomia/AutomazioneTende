import socket, config, getopt, sys
from automazione_tende import AutomazioneTende
from logger import Logger
import time
from status import Status

HOST: str = config.Config.getValue("loopback_ip", "server")  # Standard loopback interface address (localhost)
PORT: str = config.Config.getInt("port", "server")           # Port to listen on (non-privileged ports are > 1023)
TELESCOPE_PLUGIN: str = "simulator"
MOCK: bool = False
park_alt = config.Config.getValue("park_alt", "telescope")
park_az = config.Config.getValue("park_az", "telescope")
flat_alt = config.Config.getValue("flat_alt", "telescope")
flat_az = config.Config.getValue("flat_az", "telescope")

try:
    opts, _ = getopt.getopt(sys.argv[1:], "ms", ["mock", "sky"])
except getopt.GetoptError:
    Logger.getLogger().exception("parametri errati")
    exit(2) #esce dall'applicazione con errore
for opt, _1 in opts:
    if opt in ('-m', '--mock'):
        MOCK = True
    elif opt in ('-s', '--sky'):
        TELESCOPE_PLUGIN = "theskyx"

automazioneTende: AutomazioneTende = AutomazioneTende(TELESCOPE_PLUGIN, mock=MOCK)
error_level: int = 0
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        Logger.getLogger().info("Server avviato")
        while True:
            conn, _ = s.accept()
            with conn:
                while True:
                    Logger.getLogger().debug(automazioneTende.crac_status)
                    data: bytes = conn.recv(1)
                    Logger.getLogger().debug("Data: %s", data)

                    if not data or data == b'E':
                        if automazioneTende.started:
                            automazioneTende.started = False
                            automazioneTende.park_curtains()
                        automazioneTende.move_tele(0, park_alt, park_az)
                        automazioneTende.close_roof()
                        try:
                            conn.close()
                        finally:
                            if data == b'-':
                                automazioneTende.exit_program()
                                exit(0)
                            break

                    elif data == b"1":
                        automazioneTende.started = True

                    elif data == b'0':
                        automazioneTende.started = False

                    elif data == b'R':
                        Logger.getLogger().debug("chiamata del metodo per apertura tetto (automazioneTende.open_roof) ")
                        automazioneTende.open_roof()

                    elif data == b'T':
                        Logger.getLogger().debug("chiamata del metodo per chiusura tetto (automazioneTende.open_roof) ")
                        automazioneTende.close_roof()

                    elif data == b'P':
                        Logger.getLogger().debug("chiamata al metodo telescopio.park_tele")
                        automazioneTende.move_tele(0, park_alt, park_az)

                    elif data == b'F':
                        Logger.getLogger().debug("chiamata al metodo telescopio.flat_tele")
                        automazioneTende.move_tele(0, flat_alt, flat_az)

                    elif data == b'L':
                        Logger.getLogger().debug("chiamata al metodo accensione pannello flat")
                        automazioneTende.panel_on()

                    elif data == b'D':
                        Logger.getLogger().debug("chiamata al metodo spegnimento pannello flat")
                        automazioneTende.panel_off()

                    elif data == b'W':
                        Logger.getLogger().debug("chiamata al metodo accensione alimentatori")
                        automazioneTende.power_on_tele()

                    elif data == b'X':
                        Logger.getLogger().debug("chiamata al metodo spegnimento alimentatori")
                        automazioneTende.power_off_tele()

                    elif data == b'K':
                        Logger.getLogger().debug("chiamata al metodo accensione luci cupola")
                        automazioneTende.light_on()

                    elif data == b'J':
                        Logger.getLogger().debug("chiamata al metodo spegnimento luci cupola")
                        automazioneTende.light_off()

                    elif data == b'A':
                        Logger.getLogger().debug("chiamata al metodo accensione ausiliare")
                        automazioneTende.power_on_ccd()

                    elif data == b'O':
                        Logger.getLogger().debug("chiamata al metodo spegnimento ausiliare")
                        automazioneTende.power_off_ccd()

                    elif data == b'S':
                        Logger.getLogger().debug("chiamata al metodo sincronizzazione")
                        automazioneTende.time_sync()

                    Logger.getLogger().debug("chiamata al metodo per muovere le tendine (automazioneTende.exec) %s", automazioneTende.started)
                    automazioneTende.exec()

                    conn.sendall(repr(automazioneTende.read()).encode("UTF-8"))

except (KeyboardInterrupt, SystemExit):
    Logger.getLogger().info("Intercettato CTRL+C")
except Exception as e:
    Logger.getLogger().exception("altro errore: ")
    error_level = -1
    raise
finally:
    automazioneTende.exit_program(error_level)
