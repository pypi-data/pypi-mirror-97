# Koturn Python Client

Python client for [Koturn](https://github.com/whittlbc/koturn) (Coturn on Kubernetes) offering a simple 
interface to obtain the available [RTCIceServer](https://developer.mozilla.org/en-US/docs/Web/API/RTCIceServer/urls) 
instances in your Koturn cluster.

# Requirements

* Python 3+
* A running [Koturn](https://github.com/whittlbc/koturn) cluster

# Installation

```
$ pip install koturn
```

# Setup

Ensure the following environment variables are set and available:

```
export AWS_DEFAULT_REGION="<your-region>"
export AWS_ACCESS_KEY_ID="<your-access-key-id>"
export AWS_SECRET_ACCESS_KEY="<your-secret-access-key>"
export TURN_PORT="3478"
export TURN_USERNAME="<your-turn-username>"
export TURN_PASSWORD="<your-turn-password>"
```

`TURN_USERNAME` and `TURN_PASSWORD` only need to be set if you plan to accept TURN connections. Otherwise, only STUN 
server data will be returned by the main helper functions of this library.

# Usage

```python
from koturn import get_ice_servers, get_ice_server_data

# Get all available RTCIceServer instances in your Koturn cluster.
ice_servers = get_ice_servers()

# Get all available RTCIceServer instances in your Koturn cluster, formatted as shown below.
ice_server_data = get_ice_server_data()

print(ice_server_data)
# [
#   {
#     'urls': 'stun:1.2.3.4:3478',
#   },
#   {
#     'urls': 'stun:5.6.7.8:3478',
#   },
#   {
#     'urls': 'turn:1.2.3.4:3478', 
#     'username': 'diamond',
#     'credential': 'hands',
#   },
#   {
#     'urls': 'turn:5.6.7.8:3478', 
#     'username': 'diamond',
#     'credential': 'hands',
#   },
# ]
```

# License

MIT