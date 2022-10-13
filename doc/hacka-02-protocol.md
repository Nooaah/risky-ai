# Hackagames Communication Protocol

The idea is to use cleint/server architecture to permt any code in any language to seat to a games (ie. connect to act as a player).
For that we choose to use a hight level messaging librairie and esitate between [mosquitto](https://mosquitto.org), [zeromq](http://czmq.zeromq.org) and [ros2](https://docs.ros.org/en/foxy/index.html)

## High level Message Queuing API

- **Mosquitto** is a MQTT standar light implementation. MQTT defines protocols for topic based process interconnection. a Broker server serves as a central point to connect all the other node.
- **zeromq** follows its own protocols and propose a high level interface to interprocess communication via difference communication architecture and diferent low level protocols including in-procecus communication. 
- **ROS2** is developed for robotic purpose.


## Applyed API

## HackaGames' Protocol

