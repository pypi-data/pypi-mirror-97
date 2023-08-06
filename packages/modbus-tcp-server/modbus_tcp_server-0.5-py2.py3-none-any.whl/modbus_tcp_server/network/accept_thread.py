import socket
import typing as tp

from satella.coding import silence_excs
from satella.coding.concurrent import TerminableThread

from .conn_thread import ConnectionThread
from ..data_source import BaseDataSource, TestingDataSource
from ..datagrams import MODBUSTCPMessage
from ..processor import ModbusProcessor


class ModbusTCPServer(TerminableThread):
    def __init__(self, bind_ifc: str, bind_port: int,
                 data_source: tp.Optional[BaseDataSource] = None,
                 backlog: int = 128):
        super().__init__(name='accept')
        if data_source is None:
            data_source = TestingDataSource()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((bind_ifc, bind_port))
        self.backlog = backlog
        self.processor = ModbusProcessor(data_source)

    def prepare(self) -> None:
        self.socket.listen(self.backlog)
        self.socket.setblocking(True)
        self.socket.settimeout(5)

    def process_message(self, msg: MODBUSTCPMessage) -> MODBUSTCPMessage:
        return self.processor.process(msg)

    def cleanup(self):
        self.socket.close()

    @silence_excs(socket.timeout)
    def loop(self) -> None:
        sock, addr = self.socket.accept()
        ConnectionThread(sock, addr, self).start()
