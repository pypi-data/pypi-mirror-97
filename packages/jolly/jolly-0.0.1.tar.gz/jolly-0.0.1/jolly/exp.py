class JollyException(BaseException):

  def __init__(self, err='', **kwargs):
    super(JollyException, self).__init__(
      'Jolly exception: {} -- ({})'.format(err, kwargs))


class JollyDBException(JollyException):

  def __init__(self, err='', **kwargs):
    super(JollyDBException, self).__init__(
      'Jolly DB operation failed with exception: {} -- ({})'.format(err, kwargs))


class CreateJollyResourceException(JollyException):

  def __init__(self, err='', **kwargs):
    super(CreateJollyResourceException, self).__init__(
      'Creating Jolly resource failed with exception: {} -- ({})'.format(err, kwargs))


class SelectJollyInstanceException(JollyException):

  def __init__(self, err='', **kwargs):
    super(SelectJollyInstanceException, self).__init__(
      'Selecting Jolly instance failed with exception: {} -- ({})'.format(err, kwargs))


class UpdateJollyInstanceException(JollyException):

  def __init__(self, err='', **kwargs):
    super(UpdateJollyInstanceException, self).__init__(
      'Updating Jolly instance failed with exception: {} -- ({})'.format(err, kwargs))
