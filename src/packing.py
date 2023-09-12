from socket import socket
import struct

# TODO
# [X] - VarInt
# [X] - VarLong
# [X] - Int
# [X] - UInt
# [X] - Long
# [X] - ULong
# [ ] - Float
# [ ] - Double
# [ ] - Short
# [ ] - UShort
# [ ] - String < varint string
# [ ] - SString < unsigned short string
# [ ] - IString < unsigned int string
# [ ] - LString < unsigned long string
# [ ] - Bool
# [ ] - Byte
# [ ] - UByte
# [ ] - UUID
# [ ] - Json


class VarInt():
    """Functions that have to do with the reading and writing of variable-length integers."""
    
    @staticmethod
    def Write(value: int) -> bytes:
        if value > 2147483647 or value < -2147483648:
            raise ValueError("Varint value must be between -2147483648 and 2147483647!")
        
        if value < 0:
            value = (1 << 32) + value  # Convert negative value to its two's complement equivalent

        varint_bytes = bytearray()

        # Encode the value as a VarInt
        while True:
            byte = value & 0x7F
            value >>= 7
            if value != 0:
                byte |= 0x80
            varint_bytes.append(byte)
            if value == 0:
                break
        
        return bytes(varint_bytes)

    @staticmethod
    def Read(_bytes: bytes) -> (bytes, int):
        b = bytearray(_bytes)
        data = 0
        shift = 0
        for _ in range(5):  # Up to 5 bytes can be used for 32-bit signed integers
            if len(b) == 0:
                break
            byte = b[0]
            del b[0]
            data |= (byte & 0x7F) << shift
            shift += 7
            if not byte & 0x80:
                break
        
        # Convert the two's complement representation back to a signed integer if needed
        if data & 0x80000000:
            data = -((1 << 32) - data)
        
        return bytes(b), data

    @staticmethod
    def ReadFromStream(sock: socket) -> int:
        data = 0
        for i in range(5):
            ordinal = sock.recv(1)
            if len(ordinal) == 0:
                break
            byte = ord(ordinal)
            data |= (byte & 0x7F) << 7*i
            if not byte & 0x80:
                break
        return data
    
    @staticmethod
    def WriteToStream(sock : socket, value : int):
        if value > 2147483647 or value < -2147483648:
            raise ValueError("Varint value must be between -2147483648 and 2147483647!")

        sock.sendall(VarInt.Write(value))

class VarLong():
    """Functions that have to do with the reading and writing of variable-length longs."""

    @staticmethod
    def Write(value: int) -> bytes:
        if value > 9223372036854775807 or value < -9223372036854775808:
            raise ValueError("VarLong value must be between -9223372036854775808 and 9223372036854775807!")

        if value < 0:
            value = (1 << 64) + value  # Convert negative value to its two's complement equivalent

        varlong_bytes = bytearray()

        # Encode the value as a VarLong
        while True:
            byte = value & 0x7F
            value >>= 7
            if value != 0:
                byte |= 0x80
            varlong_bytes.append(byte)
            if value == 0:
                break
        
        return bytes(varlong_bytes)

    @staticmethod
    def Read(_bytes: bytes) -> (bytes, int):
        b = bytearray(_bytes)
        data = 0
        shift = 0
        for _ in range(10):  # Up to 10 bytes can be used for 64-bit signed integers
            if len(b) == 0:
                break
            byte = b[0]
            del b[0]
            data |= (byte & 0x7F) << shift
            shift += 7
            if not byte & 0x80:
                break
        
        # Convert the two's complement representation back to a signed integer if needed
        if data & 0x8000000000000000:
            data = -((1 << 64) - data)
        
        return bytes(b), data

    @staticmethod
    def ReadFromStream(sock: socket) -> int:
        data = 0
        for i in range(10):  # Up to 10 bytes can be used for 64-bit signed integers
            ordinal = sock.recv(1)
            if len(ordinal) == 0:
                break
            byte = ord(ordinal)
            data |= (byte & 0x7F) << 7 * i
            if not byte & 0x80:
                break
        return data

    @staticmethod
    def WriteToStream(sock: socket, value: int):
        if value > 9223372036854775807 or value < -9223372036854775808:
            raise ValueError("VarLong value must be between -9223372036854775808 and 9223372036854775807!")

        if value < 0:
            value = (1 << 64) + value  # Convert negative value to its two's complement equivalent

        while True:
            byte = value & 0x7F
            value >>= 7
            if value != 0:
                byte |= 0x80
            sock.send(bytes([byte]))
            if value == 0:
                break

class Int():
    """Functions that have to do with the reading and writing of integers."""

    @staticmethod
    def Write(value : int):
        return struct.pack('>i', value)
    
    @staticmethod
    def Read(_bytes : bytes):
        _a = bytearray(_bytes)
        _b = struct.unpack('>i', _a[0 : 4])[0]
        del _a[0 : 4]
        return _a, _b
    
    @staticmethod
    def ReadFromStream(_sock : socket):
        return struct.unpack('>i', _sock.recv(4))[0]
    
    @staticmethod
    def WriteToStream(_sock : socket, value : int):
        return _sock.sendall(Int.Write(value))

class UInt():
    """Functions that have to do with the reading and writing of unsigned integers."""

    @staticmethod
    def Write(value : int):
        return struct.pack('>I', value)
    
    @staticmethod
    def Read(_bytes : bytes):
        _a = bytearray(_bytes)
        _b = struct.unpack('>I', _a[0 : 4])[0]
        del _a[0 : 4]
        return _a, _b
    
    @staticmethod
    def ReadFromStream(_sock : socket):
        return struct.unpack('>I', _sock.recv(4))[0]
    
    @staticmethod
    def WriteToStream(_sock : socket, value : int):
        return _sock.sendall(UInt.Write(value))

class Long():
    def Write(value : int):
        return struct.pack('>q', value)
    def Read(_bytes : bytes):
        return struct.unpack('>q', _bytes)[0]
    def ReadFromStream(_sock : socket):
        data = _sock.recv(8)
        _ret = Long.Read(data)
        return _ret
    def WriteToStream(_sock : socket, value : int):
        _sock.sendall(Long.Write(value))

class ULong():
    def Write(value : int):
        return struct.pack('>Q', value)
    def Read(_bytes : bytes):
        return struct.unpack('>Q', _bytes)[0]
    def ReadFromStream(_sock : socket):
        data = _sock.recv(8)
        _ret = ULong.Read(data)
        return _ret
    def WriteToStream(_sock : socket, value : int):
        _sock.sendall(ULong.Write(value))
