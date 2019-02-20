import socket, config#, gui
from automazione_tende import AutomazioneTende
  

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 3000        # Port to listen on (non-privileged ports are > 1023)




automazioneTende = AutomazioneTende()
#g_ui = gui.Gui()
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1)
                    if not data:

                        try:
                            conn.close()
                        finally:
                            break
                    elif (data == b"0" or data == b'E') and automazioneTende.started:
                        automazioneTende.started = False
                        if data == b'E':
                            try:
                                conn.close()
                            finally:
                                automazioneTende.exit_program()
                                break
                                       
                                
                    elif data == b"1"  and not automazioneTende.started:
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
                    conn.sendall(steps.encode("UTF-8"))
                    if data == b'-':
                        try:
                            conn.close()
                        finally:
                            automazioneTende.exit_program()
                            exit(0)

finally:
    automazioneTende.exit_program()
