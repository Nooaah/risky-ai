# Play with ZeroMQ

The idea is to use cleint/server architecture for HackaGames based on an existing API.
Here we present a tutorial to test _ZeroMQ_ solution.

## play with ZeroMQ

See [zeromq documentation](https://zeromq.org/get-started) for more details.

**zeromq** is based on a hight level implementation of [socket notion](https://zeromq.org/socket-api).
The zerom's socket is implemented with type, depending on the communication architecture to use (Messaging Patterns).

In a first step we are interested in [request/reply pattern](https://zeromq.org/socket-api/#request-reply-pattern), 
the `hello world` programme is implemented with:

**Server:**

```python
import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"World")
```

**client**

```python
import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
for request in range(10):
    print("Sending request %s …" % request)
    socket.send(b"Hello")

    #  Get the reply.
    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))
```

reference: [https://zeromq.org/languages/python/](zeromq.org/languages/python/)


## ZeroMQ in HackaGames

In Hackagames, the game process is the server and players are clients.
The game is the orchestrer and distribute decition making requests.
For that, the [router pattern](https://zeromq.org/socket-api/#router-pattern) for the game process seems more adapted.

To go deeper: https://pyzmq.readthedocs.io, https://zguide.zeromq.org/docs/chapter2/.

In fact we require router with identified clients (players) (still on [zguide.zeromq.org](https://zguide.zeromq.org/docs/chapter4/#Service-Oriented-Reliable-Queuing-Majordomo-Pattern)).
The secret is in the usage of multi-partmessaging (inerant to Router).
At this stage, a multi_message is splited on 3 parts: clients identifier, nothing, the mesage.

So without modification on the the client side, a router on espected 3 clients would look-like too: 

```python
# Simple router server
import zmq, signal

# Prepare our context and sockets
context = zmq.Context()
sockets = context.socket(zmq.ROUTER)
sockets.bind("tcp://*:1400")

# Prepare a clean stop:
runing= True
def handler(signum, frame):
    global runing
    print('Signal handler called with signal', signum)
    runing= False

signal.signal(signal.SIGTERM, handler)

# Switch messages between sockets
players= []
while runing:
    for i in range(3) :
        message = sockets.recv_multipart()
        print( message )
        players.append( message[0] )

    sockets.send_multipart( [players[0], b'', b'cool Astrid'] )
    sockets.send_multipart( [players[1], b'', b'cool Bob'] )
    sockets.send_multipart( [players[2], b'', b'cool Cedric'] )
```

## Classical use of router

It is possible (and classc) to see the `router` as an intermediate note: 

```python
# Simple request-reply broker
#
# Author: Lev Givon <lev(at)columbia(dot)edu>

import zmq

# Prepare our context and sockets
context = zmq.Context()
frontend = context.socket(zmq.ROUTER)
backend = context.socket(zmq.DEALER)
frontend.bind("tcp://*:5559")
backend.bind("tcp://*:5560")

# Initialize poll set
poller = zmq.Poller()
poller.register(frontend, zmq.POLLIN)
poller.register(backend, zmq.POLLIN)

# Switch messages between sockets
while True:
    socks = dict(poller.poll())

    if socks.get(frontend) == zmq.POLLIN:
        message = frontend.recv_multipart()
        backend.send_multipart(message)

    if socks.get(backend) == zmq.POLLIN:
        message = backend.recv_multipart()
        frontend.send_multipart(message)
```

In this architecture the game would be a kind of DEALER.
