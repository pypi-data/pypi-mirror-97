from .dynamo_db import dynamo_db
from .table import Table
from koturn.exp import KoturnException


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
    except BaseException as e:
      return KoturnException(e)
