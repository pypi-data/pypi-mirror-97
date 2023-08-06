from jolly.services.jolly_resource_services.create_jolly_resource_service import CreateJollyResourceService
from jolly.models import JollyResource


def create_message(resource_id):
  return create_jolly_resource(JollyResource.MESSAGE_TYPE, resource_id)


def create_jolly_resource(resource_type, resource_id):
  # Initialize resource creation service.
  svc = CreateJollyResourceService(resource_type, resource_id)

  # Perform service.
  svc.perform()

  # Return the IP of the Jolly instance assigned to this resource.
  return svc.selected_instance_ip
