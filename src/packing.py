from socket import socket

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
