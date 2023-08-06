from jolly.exp import JollyException


class AbstractJollyService(object):

  def __init__(self, *args, exp=JollyException, **kwargs):
    self.exp = exp

  def perform(self):
    raise NotImplementedError

  def abort(self, *args, **kwargs):
    raise self.exp(*args, **kwargs)
