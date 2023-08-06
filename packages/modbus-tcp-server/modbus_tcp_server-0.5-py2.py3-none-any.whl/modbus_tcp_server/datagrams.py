import struct

from satella.coding import rethrow_as

from .exceptions import InvalidFrame

STRUCT_HDR = struct.Struct('>HHHB')
SHDR_SIZE = STRUCT_HDR.size


class MODBUSTCPMessage:
    def __init__(self, tid: int, pid: int, unit_id: int, data: bytes):
        self.tid = tid
        self.pid = pid
        self.unit_id = unit_id
        self.data = data

    def __bytes__(self) -> bytes:
        return STRUCT_HDR.pack(self.tid, self.pid, len(self.data) + 1, self.unit_id) + self.data

    def __len__(self) -> int:
        return SHDR_SIZE + len(self.data)

    @classmethod
    @rethrow_as((IndexError, struct.error), ValueError)
    def from_bytes(cls, d: bytes) -> 'MODBUSTCPMessage':
        tid, pid, length, uid = STRUCT_HDR.unpack(d[:SHDR_SIZE])
        if pid != 0x00:
            raise InvalidFrame('Protocol ID not 0')
        data = d[SHDR_SIZE:SHDR_SIZE + length - 1]
        if len(data) < length - 1:
            raise ValueError('Input data too short')
        return MODBUSTCPMessage(tid, pid, uid, data)

    def respond(self, data: bytes, exception: bool = False) -> 'MODBUSTCPMessage':
        """
        Provide a response to this datagram

        :param data: data to respond with. This will be appended to the function code
            of this datagram!
        :param exception: is this an exceptional response?
        :return: a MODBUSTCPMessage
        """
        if exception:
            return MODBUSTCPMessage(self.tid, 0, self.unit_id, bytes([self.data[0] & 0x80]) + data)
        else:
            return MODBUSTCPMessage(self.tid, 0, self.unit_id, self.data[0:1] + data)
