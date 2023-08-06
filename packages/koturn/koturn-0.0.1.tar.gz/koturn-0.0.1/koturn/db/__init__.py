from .koturn_instance_table import KoturnInstanceTable

# Create reference to the koturn instance table.
koturn_instance_table = KoturnInstanceTable()


def get_koturn_instances():
  return koturn_instance_table.get_all()
