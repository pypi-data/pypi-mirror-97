from koturn.config import config
from .stun import Stun
from .turn import Turn

configured_protocols = [Stun()] + ([Turn()] if config.is_turn_configured else [])