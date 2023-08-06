class JollyInstance(object):

  def __init__(self, instance, ip, load=0):
    self.instance = instance
    self.ip = ip
    self.load = load


class JollyResource(object):

  MESSAGE_TYPE = 'message'
  CONVERSATION_TYPE = 'conversation'
  resource_types = [MESSAGE_TYPE, CONVERSATION_TYPE]

  @property
  def load(self):
    return {
      self.MESSAGE_TYPE: 1,
      self.CONVERSATION_TYPE: 5,
    }.get(self.resource_type)

  def __init__(self, resource_id, resource_type, instance):
    self.resource_id = resource_id
    self.resource_type = resource_type
    self.instance = instance
