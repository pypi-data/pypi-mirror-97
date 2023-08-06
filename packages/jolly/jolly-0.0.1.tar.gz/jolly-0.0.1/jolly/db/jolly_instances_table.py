from jolly.config import config
from jolly.definitions import jolly
from .dynamo_table import DynamoTable
from jolly.models import JollyInstance


class JollyInstancesTable(DynamoTable):

  INSTANCE_COL = 'Instance'
  IP_COL = 'IP'
  LOAD_COL = 'Load'

  def __init__(self):
    super(JollyInstancesTable, self).__init__(
      jolly.capitalize() + 'Instances' + config.ENV.capitalize()
    )

  def get_all(self):
    records = super(JollyInstancesTable, self).get_all()

    return [
      JollyInstance(
        record.get(self.INSTANCE_COL),
        record.get(self.IP_COL),
        record.get(self.LOAD_COL),
      )
      for record in records
    ]

  def update_load(self, instance, load):
    return super(JollyInstancesTable, self).update_item(
      Key={self.INSTANCE_COL: instance},
      AttributeUpdates={
        self.LOAD_COL: dict(Value=load, Action='PUT'),
      },
    )
