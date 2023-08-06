from jolly.config import config
from jolly.definitions import jolly
from .dynamo_table import DynamoTable
from jolly.models import JollyResource


class JollyResourcesTable(DynamoTable):

  RESOURCE_ID_COL = 'ResourceId'
  RESOURCE_TYPE_COL = 'ResourceType'
  INSTANCE_COL = 'Instance'

  def __init__(self):
    super(JollyResourcesTable, self).__init__(
      jolly.capitalize() + 'Resources' + config.ENV.capitalize()
    )

  def create_item(self, jolly_resource):
    return super(JollyResourcesTable, self).create_item(**{
      self.RESOURCE_ID_COL: jolly_resource.resource_id,
      self.RESOURCE_TYPE_COL: jolly_resource.resource_type,
      self.INSTANCE_COL: jolly_resource.instance,
    })
