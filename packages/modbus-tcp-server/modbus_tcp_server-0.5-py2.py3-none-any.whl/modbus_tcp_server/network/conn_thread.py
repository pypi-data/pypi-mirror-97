import logging
import socket
import time

from satella.coding import silence_excs
from satella.coding.concurrent import TerminableThread

from ..datagrams import MODBUSTCPMessage
from ..exceptions import InvalidFrame

logger = logging.getLogger(__name__)

MAX_TIME_WITHOUT_ACTIVITY = 60.0    # 60 seconds


class ConnectionThread(TerminableThread):
    def __init__(self, sock, addr, server):
        super().__init__(terminate_on=(socket.error, InvalidFrame), daemon=True)
        self.socket = sock
        self.server = server
        self.addr = addr
        self.socket.setblocking(True)
        self.socket.settimeout(5)
        self.buffer = bytearray()
        self.last_activity = time.monotonic()

    def cleanup(self) -> None:
        self.socket.close()

    @silence_excs(socket.timeout)
    def loop(self) -> None:
        # Check for termination conditions
        # noinspection PyProtectedMember
        if self.server._terminating:
            raise socket.error()
        if time.monotonic() - self.last_activity > MAX_TIME_WITHOUT_ACTIVITY:
            raise socket.error()

        # Get the data
        data = self.socket.recv(128)
        if not data:
            raise socket.error()
        logger.info('Received %s', repr(data))
        self.buffer.extend(data)

        # Extract MODBUS packets
        while self.buffer:
            try:
                packet = MODBUSTCPMessage.from_bytes(self.buffer)
            except ValueError:
                break
            del self.buffer[:len(packet)]
            msg = self.server.process_message(packet)
            b = bytes(msg)
            logger.debug('Sent %s', repr(b))
            try:
                self.socket.sendall(b)
            except socket.timeout:
                # Timeout on sendall means the client is extremely slow
                raise socket.error()
            self.last_activity = time.monotonic()
