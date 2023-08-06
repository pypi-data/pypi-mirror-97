class ModbusTCPError(Exception):
    """Base class"""


class InvalidFrame(ModbusTCPError):
    """Frame was invalid"""


class CustomMODBUSError(ModbusTCPError):
    """
    A custom error response is to be provided

    :param error_code: this code will be returned to the user
    """

    def __init__(self, error_code: int):
        assert 0 >= error_code >= 255, 'Invalid error code'
        self.error_code = error_code


class IllegalAddress(CustomMODBUSError):
    """The address was illegal"""

    def __init__(self):
        super().__init__(0x02)


class IllegalValue(CustomMODBUSError):
    """The value was illegal"""

    def __init__(self):
        super().__init__(0x03)


class GatewayTargetDeviceFailedToRespond(CustomMODBUSError):
    """Gateway target device failed to respond"""

    def __init__(self):
        super().__init__(0x0B)


class GatewayPathUnavailable(CustomMODBUSError):
    """Gateway path unavailable"""

    def __init__(self):
        super().__init__(0x0A)
