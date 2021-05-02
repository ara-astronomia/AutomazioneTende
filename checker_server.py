import getopt
import socket
import sys
from threading import Thread
from unittest import mock

from gpiozero import RotaryEncoder, OutputDevice, Motor, DigitalInputDevice
from time import sleep

from config import Config
from logger import Logger


def convert_steps(steps):
    return f'{steps:04}'


def when_rotated(rotary_encoder):
    Logger.getLogger().info(f"Step: %s", rotary_encoder.steps)
    # if rotary_encoder.steps <= 0:
    #     curtain_closed.pin.drive_low()
    # else:
    #     curtain_closed.pin.drive_high()
    # if rotary_encoder.steps >= Config.getInt("n_step_corsa", "encoder_step"):
    #     curtain_open.pin.drive_low()
    # else:
    #     curtain_open.pin.drive_high()


def __rotate__(*inputs):
    [input.pin.drive_low() for input in inputs]
    [input.pin.drive_high() for input in inputs]


def __fake_move_forward__(pin_a, pin_b):
    sleep(0.2)
    __rotate__(pin_a, pin_b)
    Logger.getLogger().debug("Clock Wise")
    # curtain.__check_curtains_limit__()


def __fake_move_backward__(pin_a, pin_b):
    sleep(0.2)
    __rotate__(pin_b, pin_a)
    Logger.getLogger().debug("Counter Clock Wise")
    # curtain.__check_curtains_limit__()


def __motor_thread__(motor, pin_a, pin_b):
    while True:
        while motor.is_active:
            Logger.getLogger().debug("Motor value = %s", motor.value)
            if motor.value == 1:
                __fake_move_forward__(pin_a, pin_b)
            else:
                __fake_move_backward__(pin_a, pin_b)


MOCK: bool = False
HOST: str = Config.getValue("loopback_ip", "server")
PORT: str = Config.getInt("port", "server")

try:
    opts, _ = getopt.getopt(sys.argv[1:], "m", ["mock"])
except getopt.GetoptError:
    Logger.getLogger().exception("parametri errati")
    exit(2)  # esce dall'applicazione con errore

for opt, _1 in opts:
    if opt in ('-m', '--mock'):
        MOCK = True
        from gpiozero import Device
        from gpiozero.pins.mock import MockFactory

        if Device.pin_factory is not None:
            Device.pin_factory.reset()
        Device.pin_factory = MockFactory()

step_sicurezza = Config.getInt("n_step_sicurezza", "encoder_step")
error_level: int = 0
east_rotary_encoder = RotaryEncoder(
                Config.getInt("clk_e", "encoder_board"),
                Config.getInt("dt_e", "encoder_board"),
                max_steps=step_sicurezza,
                wrap=True
            )
west_rotary_encoder = RotaryEncoder(
                Config.getInt("clk_w", "encoder_board"),
                Config.getInt("dt_w", "encoder_board"),
                max_steps=step_sicurezza,
                wrap=True
            )
east_rotary_encoder.steps = 0
west_rotary_encoder.steps = 0
east_rotary_encoder.when_rotated = when_rotated
west_rotary_encoder.when_rotated = when_rotated

motor_roof = OutputDevice(Config.getInt("switch_roof", "roof_board"))
panel_flat = OutputDevice(Config.getInt("switch_panel", "panel_board"))
switch_power_tele = OutputDevice(Config.getInt("switch_power", "panel_board"))
switch_light = OutputDevice(Config.getInt("switch_light", "panel_board"))
switch_aux = OutputDevice(Config.getInt("switch_aux", "panel_board"))

motor_east = Motor(
    Config.getInt("motorE_A", "motor_board"),
    Config.getInt("motorE_B", "motor_board"),
    Config.getInt("motorE_E", "motor_board"),
    pwm=False
)

motor_west = Motor(
    Config.getInt("motorW_A", "motor_board"),
    Config.getInt("motorW_B", "motor_board"),
    Config.getInt("motorW_E", "motor_board"),
    pwm=False
)

if MOCK:
    thread_east = Thread(target=__motor_thread__, args=(motor_east, east_rotary_encoder.a, east_rotary_encoder.b))
    thread_east.start()
    thread_west = Thread(target=__motor_thread__, args=(motor_west, west_rotary_encoder.a, west_rotary_encoder.b))
    thread_west.start()

roof_closed_switch = DigitalInputDevice(Config.getInt("roof_verify_closed", "roof_board"), pull_up=True)
roof_open_switch = DigitalInputDevice(Config.getInt("roof_verify_open", "roof_board"), pull_up=True)

east_curtain_closed = DigitalInputDevice(Config.getInt("curtain_E_verify_open", "curtains_limit_switch"), pull_up=True)
east_curtain_open = DigitalInputDevice(Config.getInt("curtain_E_verify_closed", "curtains_limit_switch"), pull_up=True)
west_curtain_closed = DigitalInputDevice(Config.getInt("curtain_W_verify_open", "curtains_limit_switch"), pull_up=True)
west_curtain_open = DigitalInputDevice(Config.getInt("curtain_W_verify_closed", "curtains_limit_switch"), pull_up=True)

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
                        motor_roof.on()
                        Logger.getLogger().debug("MOTORE TETTO: %s", motor_roof.value)
                    if roof == 'C':
                        Logger.getLogger().debug("test chiusura tetto")
                        motor_roof.off()
                        Logger.getLogger().debug("MOTORE TETTO: %s", motor_roof.value)

                    # PANEL FLAT
                    if panel == 'A':
                        Logger.getLogger().debug("test accensione pannello flat")
                        panel_flat.on()
                        Logger.getLogger().debug("PANEL FLAT: %s", panel_flat.value)
                    if panel == 'S':
                        Logger.getLogger().debug("test spegnimento panel flat")
                        panel_flat.off()
                        Logger.getLogger().debug("PANEL FLAT: %s", panel_flat.value)

                    # POWER SWITCH TELE
                    if power_tele == 'A':
                        Logger.getLogger().debug("test accensione alimentatore telescopio")
                        switch_power_tele.on()
                        Logger.getLogger().debug("ALIMENTATORE TELE: %s", switch_power_tele.value)
                    if power_tele == 'S':
                        Logger.getLogger().debug("test spegnimento alimentatore telescopio")
                        switch_power_tele.off()
                        Logger.getLogger().debug("ALIMENTATORE TELE: %s", switch_power_tele.value)

                    # LIGHT
                    if light == 'A':
                        Logger.getLogger().debug("test accensioni luci cupola ")
                        switch_light.on()
                        Logger.getLogger().debug("LUCI CUPOLA: %s", switch_light.value)
                    if light == 'S':
                        Logger.getLogger().debug("test spegnimento luci cupola ")
                        switch_light.off()
                        Logger.getLogger().debug("LUCI CUPOLA: %s", switch_light.value)

                    # POWER SWITCH CCD
                    if power_ccd == 'A':
                        Logger.getLogger().debug("test accensione alimentatore CCD ")
                        switch_aux.on()
                        Logger.getLogger().debug("ALIMENTATORE CCD: %s", switch_aux.value)
                    if power_ccd == 'S':
                        Logger.getLogger().debug("test spegnimento alimentatore CCD ")
                        switch_aux.off()
                        Logger.getLogger().debug("ALIMENTATORE CCD: %s", switch_aux.value)

                    if curtain_west == 'O':
                        Logger.getLogger().debug("chiamata del metodo per apertura tenda west (automazioneTende.open_all_curtains.curtain_west.open_up) ")
                        motor_west.forward()
                    if curtain_west == 'C':
                        Logger.getLogger().debug("chiamata del metodo per chiusura tenda west (automazioneTende.open_all_curtains.curtain_west.bring_down) ")
                        motor_west.backward()
                    if curtain_west == 'S':
                        Logger.getLogger().debug("metodo per stop tenda west in stand-by ")
                        motor_west.stop()

                    if curtain_east == 'O':
                        Logger.getLogger().debug("chiamata del metodo per apertura tenda east (automazioneTende.open_all_curtains.curtain_east.open_up) ")
                        motor_east.forward()
                    if curtain_east == 'C':
                        Logger.getLogger().debug("chiamata del metodo per chiusura tenda east (automazioneTende.open_all_curtains.curtain_east.bring_down) ")
                        motor_east.backward()
                    if curtain_east == 'S':
                        Logger.getLogger().debug("metodo per stop tenda east in stand-by ")
                        motor_east.stop()

                    wa = motor_west.forward_device.value
                    wb = motor_west.backward_device.value
                    we = motor_west.enable_device.value
                    Logger.getLogger().debug("Tenda west A: %s", motor_west.forward_device.value)
                    Logger.getLogger().debug("Tenda west B: %s", motor_west.backward_device.value)
                    Logger.getLogger().debug("Tenda west E: %s", motor_west.enable_device.value)

                    if wa and not wb and we:
                        curtain_east = "O"
                    elif not wa and wb and we:
                        curtain_west = "C"
                    elif not wa and not wb and not we:
                        curtain_west = "S"
                    else:
                        Exception("ERROR WEST CURTAIN")

                    ea = motor_east.forward_device.value
                    eb = motor_east.backward_device.value
                    ee = motor_east.enable_device.value
                    Logger.getLogger().debug("Tenda east A: %s", motor_east.forward_device.value)
                    Logger.getLogger().debug("Tenda east B: %s", motor_east.backward_device.value)
                    Logger.getLogger().debug("Tenda east E: %s", motor_east.enable_device.value)

                    if ea and not eb and ee:
                        curtain_east = "O"
                    elif not ea and eb and ee:
                        curtain_east = "C"
                    elif not ea and not eb and not ee:
                        curtain_east = "S"
                    else:
                        Exception("ERROR EAST CURTAIN")
                    # verify root status
                    roof_status = 1 if motor_roof.is_active else 0
                    # verify motor West status
                    motor_west_status = 2 if motor_west.value == -1 else motor_west.value
                    # verify motor East status
                    motor_east_status = 2 if motor_east.value == -1 else motor_east.value
                    # verity roof if open or closed
                    sor = 1 if roof_open_switch.is_active else 0
                    scr = 1 if roof_closed_switch.is_active else 0
                    # verity curtain West open or closed
                    sow = 1 if west_curtain_open.is_active else 0
                    scw = 1 if west_curtain_closed.is_active else 0
                    # verity curtain East open or closed
                    soe = 1 if east_curtain_open.is_active else 0
                    sce = 1 if east_curtain_closed.is_active else 0
                    # number step west east
                    nee = convert_steps(east_rotary_encoder.steps)
                    nwe = convert_steps(west_rotary_encoder.steps)

                    panel_status = 1 if panel_flat.is_active else 0
                    power_tele_status = 1 if switch_power_tele.is_active else 0
                    light_status = 1 if switch_light.is_active else 0
                    switch_aux_status = 1 if switch_aux.is_active else 0

                    test_status = (
                        str(roof_status) +
                        str(motor_west_status) +
                        str(motor_east_status) +
                        str(sor) + str(scr) +
                        str(sow) + str(scw) +
                        str(soe) + str(sce) +
                        str(nwe) + str(nee) +
                        str(panel_status) +
                        str(power_tele_status) +
                        str(light_status) +
                        str(switch_aux_status)
                    )

                    Logger.getLogger().info("test_status: %s", test_status)
                    Logger.getLogger().info("Encoder est: %s", nee)
                    Logger.getLogger().info("Encoder west: %s", nwe)
                    conn.sendall(test_status.encode("UTF-8"))

except (KeyboardInterrupt, SystemExit) as e:
    Logger.getLogger().info("Intercettato CTRL+C: " + str(e))
except Exception as e:
    Logger.getLogger().exception("altro errore: " + str(e))
    error_level = -1
