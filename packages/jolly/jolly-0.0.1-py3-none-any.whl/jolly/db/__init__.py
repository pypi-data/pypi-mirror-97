from .jolly_instances_table import JollyInstancesTable
from .jolly_resources_table import JollyResourcesTable

# Create table references.
jolly_instances_table = JollyInstancesTable()
jolly_resources_table = JollyResourcesTable()


def create_jolly_resource(jolly_resource):
  return jolly_resources_table.create_item(jolly_resource)


def get_jolly_instances():
  return jolly_instances_table.get_all()


def update_jolly_instance_load(instance, load):
  return jolly_instances_table.update_load(instance, load)