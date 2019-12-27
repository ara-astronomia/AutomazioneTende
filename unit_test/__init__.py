from unittest.mock import patch, MagicMock

MockRPi = MagicMock()
MockSocket = MagicMock()
modules = {
    "RPi": MockRPi,
    "RPi.GPIO": MockRPi.GPIO,
    "socket": MockSocket,
    "socket.Socket": MockSocket.Socket
}
patcher = patch.dict("sys.modules", modules)
patcher.start()
