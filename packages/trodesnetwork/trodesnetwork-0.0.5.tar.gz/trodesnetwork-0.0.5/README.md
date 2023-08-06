[![PyPI version](https://badge.fury.io/py/trodesnetwork.svg)](https://badge.fury.io/py/trodesnetwork)

# trodesnetwork

TrodesNetwork Python SDK is used to receive network signals from Trodes in realtime.

This is a package for accessing streaming Trodes data for real-time analysis
in Python.

## Real-time Streaming Data From Trodes

When running Trodes doing a live recording or doing a simulated recording via
playback of a `.rec` file, data is streamed out. This data can include raw
neural data, processed local field potential (LFP), or processed spikes.

Some experimental protocols might make use of real-time data by detecting
certain events and responding by programmatically changing stimulation patterns
or delivering rewards.

## Installation

You can install `trodesnetwork` from PyPI:

`pip install trodesnetwork`



## Supported Datatypes

All data types are returned as a Python dictionary.

### Local field potential (LFP)
Use the local field potential by creating a subscriber object.

```
lfpSub = SourceSubscriber('source.lfp')
lfpSub.receive()
```

### Spikes
Use the unsorted spikes with waveforms by creating a subscriber object.

```
spikesSub = SourceSubscriber('source.spikes')
spikesSub.receive()
```

### Neural Data

Use the raw neural data by creating a subscriber object.

```
neuralSub = SourceSubscriber('source.neural')
neuralSub.receive()
```

### Camera Data
To subscribe to camera data, the `cameraModule` needs to be active. You can
play from a `.rec` file with a matching `.h264` video file with geometry
tracking set up. You can also do a live recording with tracking set up.

```
positionSub = SourceSubscriber('source.position')
positionSub.receive()
```

## Quickstart
After installing, testing out the library requires running a TrodesNetwork
server. It is possible to run one alone from C++ or Python, but this is not
readily supported yet.

The easiest way is to run the TrodesNetwork GUI application and play back a
`.rec` file.

## Guide

### Non-blocking socket receives

The `pyzmq` API supports non-blocking receives by [passing a flag](https://pyzmq.readthedocs.io/en/latest/api/zmq.html#zmq.Socket.recv)
to the receive function. This is not yet implemented in the library.

```
socket.recv(flag = zmq.NOBLOCK) # throws ZMQError if no message
```


## Usage

### Hardware Requests

Import trodes from the library. It contains a class for querying the hardware.

Establish a connection with the service located at `trodes.hardware`.

Send a message to start the group at slot 0.

Send a message to stop the group at slot 0.

```
from trodesnetwork import trodes
hardware = trodes.TrodesHardware()
harware.sendStimulationStartGroup(0)
harware.sendStimulationStopGroup(0)
```

### Info Requests

Import trodes from the library. It contains a class for querying the info.

Establish a connection with the service located at `trodes.info`.

Sent a request to the service.

```
from trodesnetwork import trodes
info = trodes.TrodesInfoRequester()
info.request_time()
info.request_timerate()
```

### Spikes

Create a subscriber object to subscribe to the spikes.

The location on the network is specified by "source.spikes", which is currently
hardcoded into the program to always publish at that location.

Then, receive a spike.

```
from trodesnetwork import socket
spikes = socket.SourceSubscriber('source.spikes')
spikes.receive()
```

#### Spikes Subscriber on a thread

```
from trodesnetwork import socket
import threading

spikes = SourceSubscriber('source.spikes')
spikes.receive()

def subscribe_spikes_thread():
    spikes = SourceSubscriber('source.spikes')
    while True:
        s = spikes.receive() 
        ts = s['localTimestamp']
        tid = s['nTrodeId']
        print(f'S: {ts} {tid}')

t1 = threading.Thread(target=subscribe_spikes_thread)
t1.start()
```

## Deploying to PyPi

This can only be done with package maintainer credentials.

```
python setup.py sdist
twine upload dist/*
```

## Contributing

Pull requests and issues are welcome.
