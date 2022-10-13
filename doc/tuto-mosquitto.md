# Play with mosquitto MQTT

The idea is to use cleint/server architecture for HackaGames based on an existing API.
Here we present a tutorial to test _mosquitto_ solution.

<<<<<<< HEAD
- **Mosquitto** is a MQTT standar light implementation. MQTT defines protocols for topic based process interconnection. a Broker server serves as a central point to connect all the other node.
- **zeromq** follows its own protocols and propose a high level interface to interprocess communication via difference communication architecture and diferent low level protocols including in-procecus communication.

## Hello world,

Launch mosquitto on a specific port then a subscriber to `hackagames` topic.

```sh
mosquitto -p 2014 &
mosquitto_sub -p 2014 -t hackagames
```

On a new terminal, try to publish somme mesages:

```sh
mosquitto_pub -p 2014 -t hackagames -m "hello"
```

## Hello world,
=======
## play with Mosquitto

See [mosquitto documentation](http://mosquitto.org/documentation/) for more details.

### The broker

To start mosquitto:

```sh
mosquitto -p 14042 2> broker.log &
```

Mosquitto is the broker, the process wayting for node to connect and subscrybe to topics.
By default HackaGame use 14042 port.
So now a broker process wait.

to stop it use `ps` and `kill` command (`ps` list the process PIDs and kill stop a process knowing its PId).

### Subscrite to a new topic

```sh
mosquitto_sub -h localhost -p 14042 -t 'my_topic'
```

- `localhost`: the name of the broker server (host).
- `14042`: the broker port number.
- `my_topic`: the topic name to subscribe.

### Publish in this topic

On a new terminal: 

```sh
mosquitto_pub -h localhost -p 14042 -t 'my_topic' -m 'hello world'
```

- `localhost`: the name of the broker server (host).
- `14042`: the broker port number.
- `my_topic`: the topic name to subscribe.

## Connect in Python with paho

See [paho documentation](https://www.eclipse.org/paho/index.php?page=documentation.php) and  python [paho-mqtt](https://pypi.org/project/paho-mqtt) for more details.

Simple subscribers with receipt: 

```python
# TIG: Terminal Interface to Games
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("my_topic")

# The callback for when a PUBLISH message is received from the server.
ok= True
def on_message(client, userdata, msg):
    global ok
    print( userdata )
    print( msg.topic+" "+ str(msg.payload) )
    if ok :
        client.publish("my_topic", "OK")
        ok= False
    else :
        ok= True

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 14042, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
```
>>>>>>> dev-guillaume
