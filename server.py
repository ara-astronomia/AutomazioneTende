import socket, config, json
from automazione_tende import AutomazioneTende

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

automazioneTende = AutomazioneTende()
try:
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    elif data == b"StopCurtains" and automazioneTende.started:
                        automazioneTende.started = False
                        automazioneTende.join()
                    elif data == b"StartCurtains" and not automazioneTende.started:
                        automazioneTende = AutomazioneTende()
                        automazioneTende.start()
                    elif data == b'Shutdown' and config.Config.getValue("test") is "1":
                        # solo su test dobbiamo prevedere la chiusura del server dal client
                        # pertanto non è necessario fare il cleanup del GPIO
                        if automazioneTende.started:
                            automazioneTende.started = False
                            automazioneTende.join()
                        exit(0)
                    steps = json.dumps({ "STEP_EST": automazioneTende.encoder_est.current_step, "STEP_WEST": automazioneTende.encoder_west.current_step })
                    conn.sendall(steps.encode("UTF-8"))

finally:
    if config.Config.getValue("test") is not "1":
        import RPi.GPIO as GPIO
        GPIO.cleanup()
