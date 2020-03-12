import socket, config, getopt, sys
from automazione_tende import AutomazioneTende
from logger import Logger
import time
from status import Status

HOST = config.Config.getValue("loopback_ip", "server")  # Standard loopback interface address (localhost)
PORT = config.Config.getInt("port", "server")        # Port to listen on (non-privileged ports are > 1023)
THESKY=False
MOCK=False

try:
    opts, args = getopt.getopt(sys.argv[1:],"ms", ["mock", "sky"])
except getopt.GetoptError:
    Logger.getLogger().error("parametri errati")
    exit(2) #esce dall'applicazione con errore
for opt, arg in opts:
    if opt in ('-m', '--mock'):
        MOCK=True
    elif opt in ('-s', '--sky'):
        THESKY=True

automazioneTende = AutomazioneTende(MOCK, THESKY)
error_level = 0
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        Logger.getLogger().info("Server avviato")
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    print(automazioneTende.crac_status)
                    data = conn.recv(1)
                    if not data or (data == b"0" or data == b'E') and automazioneTende.started:
                        automazioneTende.started = False

                    elif data == b"1" and not automazioneTende.started:
                        automazioneTende.started = True

                    elif data == b'-':
                        if automazioneTende.started:
                            automazioneTende.started = False

                    elif data == b'R':
                        Logger.getLogger().debug("chiamata del metodo per apertura tetto (automazioneTende.open_roof) ")
                        automazioneTende.open_roof()

                    elif data == b'T':
                        Logger.getLogger().debug("chiamata del metodo per chiusura tetto (automazioneTende.open_roof) ")
                        automazioneTende.close_roof()

                    elif data == b'P':
                        automazioneTende.started = False
                        Logger.getLogger().debug("chiamata al metodo telescopio.park_tele")
                        automazioneTende.park_tele()

                    if data != b"R" and data != b"T" and data != b'P':
                        Logger.getLogger().debug("chiamata al metodo per muovere le tendine (automazioneTende.exec)")
                        automazioneTende.exec()

                    if not data or data == b'E':
                        automazioneTende.close_roof()
                        try:
                            conn.close()
                        finally:
                            break

                    if data == b'-':
                        automazioneTende.close_roof()
                        try:
                            conn.close()
                        finally:
                            automazioneTende.exit_program()
                            exit(0)

                    conn.sendall(repr(automazioneTende.read()).encode("UTF-8"))

except (KeyboardInterrupt, SystemExit):
    Logger.getLogger().info("Intercettato CTRL+C")
except Exception as e:
    Logger.getLogger().error("altro errore: "+str(e))
    error_level = -1
    raise
finally:
    automazioneTende.exit_program(error_level)
