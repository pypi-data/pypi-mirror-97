class Protocol(object):

  def __init__(self, name):
    self.name = name

  def format_url(self, host, port):
    return ':'.join((self.name, host, str(port)))

  def format_ice_server_data(self, koturn_instance):
    raise NotImplementedError
