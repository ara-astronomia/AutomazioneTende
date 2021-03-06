import socket
from status import Orientation
import config
from logger import Logger
from gpio_config import GPIOConfig
from gpio_pin import GPIOPin
from components.curtains.factory_curtain import FactoryCurtain


# Standard loopback interface address (localhost)
HOST: str = config.Config.getValue("loopback_ip", "server")
# Port to listen on (non-privileged ports are > 1023)
PORT: str = config.Config.getInt("port", "server")
error_level: int = 0
gpioConfig = GPIOConfig()
curtain_east = FactoryCurtain.curtain(orientation=Orientation.EAST)
curtain_west = FactoryCurtain.curtain(orientation=Orientation.WEST)


def convert_steps(steps):
    return f'{steps:03}'


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        Logger.getLogger().info("Server avviato")
        while True:
            conn, _ = s.accept()
            with conn:
                while True:
                    data = conn.recv(7).decode("UTF-8")
                    Logger.getLogger().debug("Data: %s", data)
                    if data:
                        roof = data[0]
                        panel = data[1]
                        power_tele = data[2]
                        light = data[3]
                        power_ccd = data[4]
                        curtain_west = data[5]
                        curtain_east = data[6]
                    else:
                        try:
                            conn.close()
                        finally:
                            break
                    # ROOF
                    if roof == 'O':
                        Logger.getLogger().debug("test apertura tetto")
                        gpioConfig.turn_on(GPIOPin.SWITCH_ROOF)
                        Logger.getLogger().debug("MOTORE TETTO: %s", gpioConfig.status(GPIOPin.SWITCH_ROOF))
                    if roof == 'C':
                        Logger.getLogger().debug("test chiusura tetto")
                        gpioConfig.turn_off(GPIOPin.SWITCH_ROOF)
                        Logger.getLogger().debug("MOTORE TETTO: %s", gpioConfig.status(GPIOPin.SWITCH_ROOF))

                    # PANEL FLAT
                    if panel == 'A':
                        Logger.getLogger().debug("test accensione pannello flat")
                        gpioConfig.turn_on(GPIOPin.SWITCH_PANEL)
                        Logger.getLogger().debug("PANEL FLAT: %s", gpioConfig.status(GPIOPin.SWITCH_PANEL))
                    if panel == 'S':
                        Logger.getLogger().debug("test spegnimento panel flat")
                        gpioConfig.turn_off(GPIOPin.SWITCH_PANEL)
                        Logger.getLogger().debug("PANEL FLAT: %s", gpioConfig.status(GPIOPin.SWITCH_PANEL))

                    # POWER SWITCH TELE
                    if power_tele == 'A':
                        Logger.getLogger().debug("test accensione alimentatore telescopio")
                        gpioConfig.turn_on(GPIOPin.SWITCH_POWER_TELE)
                        Logger.getLogger().debug("ALIMENTATORE TELE: %s", gpioConfig.status(GPIOPin.SWITCH_POWER_TELE))
                    if power_tele == 'S':
                        Logger.getLogger().debug("test spegnimento alimentatore telescopio")
                        gpioConfig.turn_off(GPIOPin.SWITCH_POWER_TELE)
                        Logger.getLogger().debug("ALIMENTATORE TELE: %s", gpioConfig.status(GPIOPin.SWITCH_POWER_TELE))

                    # LIGHT
                    if light == 'A':
                        Logger.getLogger().debug("test accensioni luci cupola ")
                        gpioConfig.turn_on(GPIOPin.SWITCH_LIGHT)
                        Logger.getLogger().debug("LUCI CUPOLA: %s", gpioConfig.status(GPIOPin.SWITCH_LIGHT))
                    if light == 'S':
                        Logger.getLogger().debug("test spegnimento luci cupola ")
                        gpioConfig.turn_off(GPIOPin.SWITCH_LIGHT)
                        Logger.getLogger().debug("LUCI CUPOLA: %s", gpioConfig.status(GPIOPin.SWITCH_LIGHT))

                    # POWER SWITCH CCD
                    if power_ccd == 'A':
                        Logger.getLogger().debug("test accensione alimentatore CCD ")
                        gpioConfig.turn_on(GPIOPin.SWITCH_POWER_CCD)
                        Logger.getLogger().debug("ALIMENTATORE CCD: %s", gpioConfig.status(GPIOPin.SWITCH_POWER_CCD))
                    if power_ccd == 'S':
                        Logger.getLogger().debug("test spegnimento alimentatore CCD ")
                        gpioConfig.turn_off(GPIOPin.SWITCH_POWER_CCD)
                        Logger.getLogger().debug("ALIMENTATORE CCD: %s", gpioConfig.status(GPIOPin.SWITCH_POWER_CCD))


                    if curtain_west == 'O':
                        Logger.getLogger().debug("chiamata del metodo per apertura tenda west (automazioneTende.open_all_curtains.curtain_west.open_up) ")
                        gpioConfig.turn_on(GPIOPin.MOTORW_A)
                        gpioConfig.turn_off(GPIOPin.MOTORW_B)
                        gpioConfig.turn_on(GPIOPin.MOTORW_E)
                    if curtain_west == 'C':
                        Logger.getLogger().debug("chiamata del metodo per chiusura tenda west (automazioneTende.open_all_curtains.curtain_west.bring_down) ")
                        gpioConfig.turn_off(GPIOPin.MOTORW_A)
                        gpioConfig.turn_on(GPIOPin.MOTORW_B)
                        gpioConfig.turn_on(GPIOPin.MOTORW_E)
                    if curtain_west == 'S':
                        Logger.getLogger().debug("metodo per stop tenda west in stand-by ")
                        gpioConfig.turn_off(GPIOPin.MOTORW_A)
                        gpioConfig.turn_off(GPIOPin.MOTORW_B)

                    if curtain_east == 'O':
                        Logger.getLogger().debug("chiamata del metodo per apertura tenda east (automazioneTende.open_all_curtains.curtain_east.open_up) ")
                        gpioConfig.turn_on(GPIOPin.MOTORE_A)
                        gpioConfig.turn_off(GPIOPin.MOTORE_B)
                        gpioConfig.turn_on(GPIOPin.MOTORE_E)
                    if curtain_east == 'C':
                        Logger.getLogger().debug("chiamata del metodo per chiusura tenda east (automazioneTende.open_all_curtains.curtain_east.bring_down) ")
                        gpioConfig.turn_off(GPIOPin.MOTORE_A)
                        gpioConfig.turn_on(GPIOPin.MOTORE_B)
                        gpioConfig.turn_on(GPIOPin.MOTORE_E)
                    if curtain_east == 'S':
                        Logger.getLogger().debug("metodo per stop tenda east in stand-by ")
                        gpioConfig.turn_off(GPIOPin.MOTORE_A)
                        gpioConfig.turn_off(GPIOPin.MOTORE_B)
                        gpioConfig.turn_off(GPIOPin.MOTORE_E)

                    wa = 1 if gpioConfig.status(GPIOPin.MOTORW_A) else 0
                    wb = 1 if gpioConfig.status(GPIOPin.MOTORW_B) else 0
                    we = 1 if gpioConfig.status(GPIOPin.MOTORW_E) else 0
                    Logger.getLogger().debug("Tenda west A: %s", gpioConfig.status(GPIOPin.MOTORW_A))
                    Logger.getLogger().debug("Tenda west B: %s", gpioConfig.status(GPIOPin.MOTORW_B))
                    Logger.getLogger().debug("Tenda west E: %s", gpioConfig.status(GPIOPin.MOTORW_E))

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

                    # verity roof if open or closed
                    sor = gpioConfig.status(GPIOPin.VERIFY_OPEN)
                    scr = gpioConfig.status(GPIOPin.VERIFY_CLOSED)
                    # verity curtain West open or closed
                    sow = gpioConfig.status(GPIOPin.CURTAIN_W_VERIFY_OPEN)
                    scw = gpioConfig.status(GPIOPin.CURTAIN_W_VERIFY_CLOSED)
                    # verity curtain East open or closed
                    soe = gpioConfig.status(GPIOPin.CURTAIN_E_VERIFY_OPEN)
                    sce = gpioConfig.status(GPIOPin.CURTAIN_E_VERIFY_CLOSED)
                    # number step west east
                    nwe = "999"  # convert_steps(west_curtain.steps)
                    nee = "666"  # convert_steps(east_curtain.steps)

                    test_status = roof + curtain_west + curtain_east + str(sor) + str(scr) + str(sow) + str(scw) + str(soe) + str(sce) + nwe + nee
                    Logger.getLogger().info("test_status: %s", test_status)
                    Logger.getLogger().info("Encoder est: %s", nee)
                    Logger.getLogger().info("Encoder west: %s", nwe)
                    conn.sendall(test_status.encode("UTF-8"))

except (KeyboardInterrupt, SystemExit):
    Logger.getLogger().info("Intercettato CTRL+C")
except Exception as e:
    Logger.getLogger().exception("altro errore: ")
    error_level = -1
    raise
finally:
    gpioConfig.cleanup(error_level)
