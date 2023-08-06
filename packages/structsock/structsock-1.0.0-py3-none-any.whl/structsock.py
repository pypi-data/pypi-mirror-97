'''
This module provides extension for the built-in socket module.

The TCP/IP socket based on the current operating system have no indicators how many data was sent (no packet barriers).
Therefore this module extends the socket, using the struct module to format packet length to 4 bytes.

The exposed interfaces of class 'StructuredSocket' is exactly the same as the built-in 'socket.socket',
but grabbing the packet with tools you will find the data header added to the packet.
'''

import struct, socket
from typing import Tuple, Optional

__all__ = ['StructuredSocket', 'PeerDisconnect']

RECV_SIZE = 4096

class PeerDisconnect(Exception):
    "The packet cannot be sent / received due to peer's disconnection."

class StructuredSocket:
    'Represents a socket wrapped with struct.pack.'
    def __init__(self, s: Optional[socket.socket] = None):
        self._socket = s or socket.socket()
        self._recvSize = RECV_SIZE
        self._buffer = b''
    def setRecvSize(self, size: int) -> None:
        'Sets the receive size of this socket.'
        self._recvSize = size
    def getRecvSize(self) -> int:
        'Gets the receive size of this socket.'
        return self._recvSize
    def listen(self, n: int) -> None:
        'Listen for specific number of clients.'
        self._socket.listen(n)
    def bind(self, addr: Tuple[str, int]) -> None:
        'Binds the socket with specific address.'
        self._socket.bind(addr)
    def connect(self, addr: Tuple[str, int]) -> None:
        'Connects to specific address.'
        self._socket.connect(addr)
    def send(self, data: bytes) -> None:
        'Sends the data and header.'
        length = len(data)
        head = struct.pack('>I', length)
        try:
            self._socket.send(head+data)
        except Exception:
            raise PeerDisconnect
    def recv(self) -> bytes:
        'Receives the data sent by peer.'
        if not self._buffer:
            try:
                head = self._socket.recv(4)
            except ConnectionError:
                raise PeerDisconnect
            if not head:
                raise PeerDisconnect
        else:
            head, self._buffer = self._buffer[:4], self._buffer[4:]
        length = struct.unpack('>I', head)[0]
        buffer = self._buffer
        while len(buffer) < length:
            buffer += self._socket.recv(RECV_SIZE)
        buffer, self._buffer = buffer[:length], buffer[length:]
        return buffer
    def close(self) -> None:
        'Closes the internal socket.'
        self._socket.close()
    def accept(self) -> Tuple['StructuredSocket', Tuple[str, int]]:
        'Accepts an incoming connection attempt.'
        c, addr = self._socket.accept()
        return StructuredSocket(c), addr