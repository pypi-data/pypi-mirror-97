class Table(object):

  def __init__(self, name):
    self.name = name
    self._table = self._new_table()

  def _new_table(self):
    raise NotImplementedError

  def get_all(self):
    raise NotImplementedError