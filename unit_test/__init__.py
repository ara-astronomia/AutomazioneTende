from unittest.mock import patch, MagicMock

MockSocket = MagicMock()
modules = {
    "socket": MockSocket,
    "socket.Socket": MockSocket.Socket
}
patcher = patch.dict("sys.modules", modules)
patcher.start()
