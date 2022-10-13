### Dependencies:

**HackaGame** requires C/C++ development tools, CMake and [RayLib dependencies](https://github.com/raysan5/raylib/wiki/Working-on-GNU-Linux)

```sh
sudo apt update
sudo apt install -y \
  build-essential git cmake \
  libasound2-dev mesa-common-dev \
  libx11-dev libxi-dev xorg-dev \
  libgl1-mesa-dev libglu1-mesa-dev
```

The MQTT libs (C:mosquitto, python:paho):

```bash
./bin/get-raylib.sh
```

And finnally, get and build RayLib (version `3.0.0`):

```sh
./bin/get-raylib.sh
```


### **HackaGame**

A simple build scripts would generate the overall project:

```bash
./bin/build
```

It will enter each HackaGames submodules including games and build them with cmake, starting by hackagames libraries and tools.

To build only the librairies and tools, enter `hackagames` directory and build it with cmake.

```sh
cd hackagames
cmake .
make
```