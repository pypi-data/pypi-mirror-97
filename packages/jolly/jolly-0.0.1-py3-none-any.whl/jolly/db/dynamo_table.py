from .dynamo_db import dynamo_db, DynamoError
from .table import Table
from jolly.exp import JollyDBException
from jolly.logger import logger


class DynamoTable(Table):

  LAST_EVALUATED_KEY = 'LastEvaluatedKey'
  ITEMS_KEY = 'Items'

  def __init__(self, name):
    super(DynamoTable, self).__init__(name)

  def _new_table(self):
    return dynamo_db.Table(self.name)

  def get_all(self):
    try:
      resp = self._table.scan() or {}
      items = resp.get(self.ITEMS_KEY) or []

      while self.LAST_EVALUATED_KEY in resp:
        resp = self._table.scan(ExclusiveStartKey=resp[self.LAST_EVALUATED_KEY]) or {}
        items.extend(resp.get(self.ITEMS_KEY) or [])

      return items
    except DynamoError as e:
      logger.error('Error querying DynamoDB table {} for all items: {}'.format(self.name, e))
      raise JollyDBException(e)

  def create_item(self, **kwargs):
    try:
      return self._table.put_item(Item=dict(**kwargs))
    except DynamoError as e:
      logger.error('Error creating new DynamoDB item in table {}: {}'.format(self.name, e))
      raise JollyDBException(e)

  def update_item(self, **kwargs):
    try:
      return self._table.update_item(**kwargs)
    except DynamoError as e:
      logger.error('Error updating DynamoDB item in table {}: {}'.format(self.name, e))
      raise JollyDBException(e)