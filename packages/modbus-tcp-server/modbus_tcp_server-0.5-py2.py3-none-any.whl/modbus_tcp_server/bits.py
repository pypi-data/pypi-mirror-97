class BitStream:
    __slots__ = ('data', 'pointer')

    def __init__(self):
        self.pointer = 0
        self.data = bytearray()

    def __len__(self) -> int:
        return len(self.data)

    def __bytes__(self) -> bytes:
        return bytes(self.data)

    def add(self, bit: bool) -> None:
        ptr = self.pointer % 8
        value = 1 << ptr if bit else 0
        if not ptr:
            self.data += b'\x00'
        self.data[-1] = self.data[-1] | value
        self.pointer += 1


class BitConsumer:
    __slots__ = ('data', 'pointer')

    def __init__(self, data: bytes):
        self.data = bytearray(data)
        self.pointer = 0

    def __iter__(self):
        return self

    def __next__(self) -> bool:
        if not self.data:
            raise StopIteration()
        if self.pointer == 8:
            del self.data[0]
            self.pointer = 0
        try:
            return (self.data[0] >> self.pointer) & 1
        finally:
            self.pointer += 1
