class RTCIceServer(object):

  def __init__(self, protocol, urls='', username=None, credential=None):
    self.protocol = protocol
    self.urls = urls
    self.username = username
    self.credential = credential

  def as_dict(self):
    data = dict(urls=self.urls)

    if self.username:
      data['username'] = self.username

    if self.credential:
      data['credential'] = self.credential

    return data
