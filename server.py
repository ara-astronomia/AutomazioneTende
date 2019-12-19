import socket, config, getopt, sys
from automazione_tende import AutomazioneTende
from logger import Logger

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

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        Logger.getLogger().info("Server avviato")
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1)
                    if not data or (data == b"0" or data == b'E') and automazioneTende.started:
                        automazioneTende.started = False

                    elif data == b"1" and not automazioneTende.started:
                        automazioneTende.started = True

                    elif data == b'-':
                        if automazioneTende.started:
                            automazioneTende.started = False

                    elif data == b'R':
                        Logger.getLogger().info("chiamata del metodo per apertura tetto (automazioneTende.open_roof) ")
                        r = automazioneTende.open_roof()
                        if r == 0:
                            steps = "R00001"
                        else:
                            steps = "E00001"

                    elif data == b'T':
                        r = automazioneTende.close_roof()
                        if r == 1:
                            steps = "R00000"
                        else:
                            steps = "E00000"

                    if data != b"R" and data != b"T":
                        r = automazioneTende.exec()
                        if r == -1:
                            steps = "E0000S"
                        else:
                            steps = "{:0>3d}".format(automazioneTende.encoder_est.current_step)+"{:0>3d}".format(automazioneTende.encoder_west.current_step)

                    Logger.getLogger().debug("steps: "+steps)

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

                    conn.sendall(steps.encode("UTF-8"))

except Exception as e:
    Logger.getLogger().error("errore: "+str(e))
finally:
    automazioneTende.exit_program()
