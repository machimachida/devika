# socketio_instance.py
from flask_socketio import SocketIO
from src.logger import Logger


class EmitAgent:
    def __init__(self):
        self.socketio = SocketIO(cors_allowed_origins="*", async_mode="gevent")
        self.logger = Logger()

    def emit_content(self, channel, content, log=True):
        try:
            self.socketio.emit(channel, content)
            if log:
                self.logger.info(f"SOCKET {channel} MESSAGE: {content}")
            return True
        except Exception as e:
            self.logger.error(f"SOCKET {channel} ERROR: {str(e)}")
            return False
