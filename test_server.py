import socket, config, getopt, sys
from logger import Logger
import time
from status import Status
from gpio_config import GPIOConfig
from gpio_pin import GPIOPin

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

error_level: int = 0
gpioConfig = GPIOConfig()

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        Logger.getLogger().info("Server avviato")
        while True:
            conn, _ = s.accept()
            with conn:
                while True:
                    data = conn.recv(3).decode("UTF-8")
                    Logger.getLogger().debug("Data: %s", data)
                    roof = data[0]
                    curtain_west = data[1]
                    curtain_east = data[2]

                    if roof == 'O':
                        Logger.getLogger().debug("chiamata del metodo per apertura tetto (automazioneTende.open_roof) ")
                        gpioConfig.turn_on(GPIOPin.SWITCH_ROOF)
                    if curtain_west == 'O':
                        Logger.getLogger().debug("chiamata del metodo per apertura tenda west (automazioneTende.open_all_curtains.curtain_west.open_up) ")
                        gpioConfig.turn_on(GPIOPin.MOTORW_A)
                        gpioConfig.turn_off(GPIOPin.MOTORW_B)
                        gpioConfig.turn_on(GPIOPin.MOTORW_E)
                    if curtain_east == 'O':
                        Logger.getLogger().debug("chiamata del metodo per apertura tenda east (automazioneTende.open_all_curtains.curtain_east.open_up) ")
                        gpioConfig.turn_on(GPIOPin.MOTORE_A)
                        gpioConfig.turn_off(GPIOPin.MOTORE_B)
                        gpioConfig.turn_on(GPIOPin.MOTORE_E)

                    if roof == 'C':
                        Logger.getLogger().debug("chiamata del metodo per chiusura tetto (automazioneTende.open_roof) ")
                        gpioConfig.turn_off(GPIOPin.SWITCH_ROOF)
                    if curtain_west == 'C':
                        Logger.getLogger().debug("chiamata del metodo per chiusura tenda west (automazioneTende.open_all_curtains.curtain_west.bring_down) ")
                        gpioConfig.turn_off(GPIOPin.MOTORW_A)
                        gpioConfig.turn_on(GPIOPin.MOTORW_B)
                        gpioConfig.turn_on(GPIOPin.MOTORW_E)
                    if curtain_east == 'C':
                        Logger.getLogger().debug("chiamata del metodo per chiusura tenda east (automazioneTende.open_all_curtains.curtain_east.bring_down) ")
                        gpioConfig.turn_off(GPIOPin.MOTORE_A)
                        gpioConfig.turn_on(GPIOPin.MOTORE_B)
                        gpioConfig.turn_on(GPIOPin.MOTORE_E)

                    if curtain_west == 'S':
                        Logger.getLogger().debug("metodo per stop tenda west in stand-by ")
                        gpioConfig.turn_off(GPIOPin.MOTORW_A)
                        gpioConfig.turn_off(GPIOPin.MOTORW_B)
                        gpioConfig.turn_off(GPIOPin.MOTORW_E)
                    if curtain_east == 'S':
                        Logger.getLogger().debug("metodo per stop tenda east in stand-by ")
                        gpioConfig.turn_off(GPIOPin.MOTORE_A)
                        gpioConfig.turn_off(GPIOPin.MOTORE_B)
                        gpioConfig.turn_off(GPIOPin.MOTORE_E)
                    
                    roof = "O" if gpioConfig.status(GPIOPin.SWITCH_ROOF) else "C"

                    wa = 1 if gpioConfig.status(GPIOPin.MOTORW_A) else 0
                    wb = 1 if gpioConfig.status(GPIOPin.MOTORW_B) else 0
                    we = 1 if gpioConfig.status(GPIOPin.MOTORW_E) else 0

                    if wa and not wb and we:
                        curtain_east = "O"
                    elif not wa and wb and we:
                        curtain_west = "C"
                    elif not wa and not wb and not we:
                        curtain_west = "S"
                    else:
                        Exception("ERRORRRRRREW")

                    ea = 1 if gpioConfig.status(GPIOPin.MOTORE_A) else 0
                    eb = 1 if gpioConfig.status(GPIOPin.MOTORE_B) else 0
                    ee = 1 if gpioConfig.status(GPIOPin.MOTORE_E) else 0

                    if ea and not eb and ee:
                        curtain_east = "O"
                    elif not ea and eb and ee:
                        curtain_east = "C"
                    elif not ea and not eb and not ee:
                        curtain_east = "S"
                    else:
                        Exception("ERRORRRRRREW")

                    test_status = roof + curtain_west + curtain_east
                    Logger.getLogger().info("test_status: %s", test_status)
                    conn.sendall(test_status.encode("UTF-8"))

except (KeyboardInterrupt, SystemExit):
    Logger.getLogger().info("Intercettato CTRL+C")
except Exception as e:
    Logger.getLogger().exception("altro errore: ")
    error_level = -1
    raise
finally:
    gpioConfig.cleanup(error_level)
