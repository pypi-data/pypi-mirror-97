from .protocol import Protocol
from koturn.config import config


class Stun(Protocol):

  NAME = 'stun'

  def __init__(self):
    super(Stun, self).__init__(self.NAME)

  def format_ice_server_data(self, koturn_instance):
    return dict(
      urls=self.format_url(koturn_instance.ip, config.TURN_PORT),
    )
