from koturn.config import config
from koturn.db import get_koturn_instances
from koturn.exp import KoturnException
from koturn.rtc_ice_server import RTCIceServer
from koturn.protocols import configured_protocols, Stun


def get_ice_servers():
  koturn_instances = get_koturn_instances()
  stun_servers = []
  turn_servers = []

  for koturn_instance in koturn_instances:
    for protocol in configured_protocols:
      ice_server = RTCIceServer(protocol.name, **protocol.format_ice_server_data(koturn_instance))

      if protocol.name == Stun.NAME:
        stun_servers.append(ice_server)
      else:
        turn_servers.append(ice_server)

  return stun_servers + turn_servers


def get_ice_server_data():
  return [ic.as_dict() for ic in get_ice_servers()]