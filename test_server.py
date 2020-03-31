import socket, config, getopt, sys
from automazione_tende import AutomazioneTende
from logger import Logger
import time
from status import Status

HOST: str = config.Config.getValue("loopback_ip", "server")  # Standard loopback interface address (localhost)
PORT: str = config.Config.getInt("port", "server")           # Port to listen on (non-privileged ports are > 1023)
THESKY: bool = False
MOCK: bool = False

try:
    opts, _ = getopt.getopt(sys.argv[1:], "ms", ["mock", "sky"])
except getopt.GetoptError:
    Logger.getLogger().exception("parametri errati")
    exit(2) #esce dall'applicazione con errore
for opt, _1 in opts:
    if opt in ('-m', '--mock'):
        MOCK = True
    elif opt in ('-s', '--sky'):
        THESKY = True

automazioneTende: AutomazioneTende = AutomazioneTende(MOCK, THESKY)
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
                    data: bytes = conn.recv(3)
                    Logger.getLogger().debug("Data: %s", data)
                    
                    # if not data or (data == b"0" or data == b'E') and automazioneTende.started:
                    #     automazioneTende.started = False
                    #     automazioneTende.park_curtains()

                    # elif data == b"1":
                    #     automazioneTende.started = True

                    # elif data == b'-':
                    #     automazioneTende.started = False

                    # elif data == b'R':
                    #     Logger.getLogger().debug("chiamata del metodo per apertura tetto (automazioneTende.open_roof) ")
                    #     automazioneTende.open_roof()

                    # elif data == b'T':
                    #     Logger.getLogger().debug("chiamata del metodo per chiusura tetto (automazioneTende.open_roof) ")
                    #     automazioneTende.close_roof()

                    # elif data == b'P':
                    #     Logger.getLogger().debug("chiamata al metodo telescopio.park_tele")
                    #     automazioneTende.park_tele()
                    
                    if not data or data == b'E' or data == b'-':
                        # automazioneTende.started = True
                        # automazioneTende.park_tele()
                        # automazioneTende.exec()
                        # automazioneTende.started = False
                        # automazioneTende.close_roof()
                        try:
                            conn.close()
                        finally:
                            if data == b'-':
                                # automazioneTende.exit_program()
                                exit(0)
                            break
                    
                    # if not MOCK or data == b'1' or data == b'c':
                    #     Logger.getLogger().debug("chiamata al metodo per muovere le tendine (automazioneTende.exec) %s", automazioneTende.started)
                    #     automazioneTende.exec()

                    conn.sendall(repr(automazioneTende.read()).encode("UTF-8"))

except (KeyboardInterrupt, SystemExit):
    Logger.getLogger().info("Intercettato CTRL+C")
except Exception as e:
    Logger.getLogger().exception("altro errore: ")
    error_level = -1
    raise
finally:
    automazioneTende.exit_program(error_level)
