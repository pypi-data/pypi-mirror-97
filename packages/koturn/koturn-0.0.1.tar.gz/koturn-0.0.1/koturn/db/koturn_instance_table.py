from koturn.config import config
from koturn.definitions import koturn
from .dynamo_table import DynamoTable
from koturn.models import KoturnInstance


class KoturnInstanceTable(DynamoTable):

  INSTANCE_COL = 'Instance'
  IP_COL = 'IP'

  def __init__(self):
    super(KoturnInstanceTable, self).__init__(
      koturn.capitalize() + config.ENV.capitalize()
    )

  def get_all(self):
    records = super(KoturnInstanceTable, self).get_all()

    return sorted([
      KoturnInstance(
        record.get(self.INSTANCE_COL),
        record.get(self.IP_COL)
      )
      for record in records
    ], key=lambda ki: ki.index)