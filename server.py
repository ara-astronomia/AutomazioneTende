import socket, config
from automazione_tende import AutomazioneTende

HOST = config.Config.getValue("loopback_ip", "server")  # Standard loopback interface address (localhost)
PORT = config.Config.getInt("port", "server")        # Port to listen on (non-privileged ports are > 1023)

automazioneTende = AutomazioneTende()

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1)
                    if not data or (data == b"0" or data == b'E') and automazioneTende.started:
                        automazioneTende.started = False
                        if not data or data == b'E':
                            try:
                                conn.close()
                            finally:
                                break

                    elif data == b"1" and not automazioneTende.started:
                        automazioneTende.started = True

                    elif data == b"0":
                        automazioneTende.park_curtains()

                    elif data == b'-' and config.Config.getValue("test") is "1":
                        # solo su test dobbiamo prevedere la chiusura del server dal client
                        # pertanto non è necessario fare il cleanup del GPIO
                        if automazioneTende.started:
                            automazioneTende.started = False
                    automazioneTende.exec()
                    steps = "{:0>3d}".format(automazioneTende.encoder_est.current_step)+"{:0>3d}".format(automazioneTende.encoder_west.current_step)
                    print("steps: "+steps)
                    conn.sendall(steps.encode("UTF-8"))
                    if data == b'-':
                        try:
                            conn.close()
                        finally:
                            automazioneTende.exit_program()
                            exit(0)
except Exception as e:
    print("errore: "+str(e))
finally:
    automazioneTende.exit_program()
