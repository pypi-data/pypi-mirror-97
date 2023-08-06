class KoturnException(BaseException):

  def __init__(self, err='', **kwargs):
    super(KoturnException, self).__init__(
      'Koturn exception: {} -- ({})'.format(err, kwargs))
