# Structured Socket

A simple module to encapsulate the built-in socket with struct.pack so that the amount of data received can be forseen by the receiver to prevent sticking packets.

Repository: https://github.com/origamizyt/StructuredSocket
(I believe that you can understand the mechanisms without the source code.)

__Version: 1.0 (Final Release Perhaps)__

## Installation

This module is available on PyPI.
```
pip install structsock
```

Or you can install from source .tar.gz either.
```
python setup.py install
```

## Usage

The exposed interfaces in this module is pretty the same as the built-in module `socket`, only replacing `socket.socket` with `StructuredSocket`:
```py
# server side
from structsock import StructuredSocket

s = StructuredSocket()
s.bind(('0.0.0.0', 5000))
s.listen(5)
c, addr = s.accept()
c.send(b'data')
c.close()
s.close()
```

Note that the client socket returned is also a instance of `StructuredSocket`.
```py
# client side
from structsock import StructuredSocket

c = StructuredSocket()
c.connect(('127.0.0.1', 5000))
data = c.recv() # different, no bufsize
print(data.decode())
c.close()
```