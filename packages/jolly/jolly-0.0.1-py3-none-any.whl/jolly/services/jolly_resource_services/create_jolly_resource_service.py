from jolly.services.abstract_jolly_service import AbstractJollyService
from jolly.services.jolly_instance_services.select_jolly_instance_service import SelectJollyInstanceService
from jolly.services.jolly_instance_services.update_jolly_instance_load_service import UpdateJollyInstanceLoadService
from jolly.exp import *
from jolly.logger import logger
from jolly.models import JollyResource
from jolly.db import create_jolly_resource


class CreateJollyResourceService(AbstractJollyService):

  @property
  def selected_instance_ip(self):
    return self.jolly_instance.ip if self.jolly_instance else None

  def __init__(self, resource_type, resource_id, **kwargs):
    super(CreateJollyResourceService, self).__init__(exp=CreateJollyResourceException, **kwargs)
    self.resource_type = resource_type
    self.resource_id = resource_id
    self.jolly_instance = None
    self.jolly_resource = None

  def perform(self):
    logger.info('Creating new JollyResource(resource_id={}, resource_type={})...'.format(
      self.resource_id, self.resource_type))

    # Validate resource type.
    self._validate_resource_type()

    # Select a jolly instance for this resource.
    self._select_jolly_instance()

    # Create the jolly resource in the DB.
    self._create_jolly_resource()

    # Update the selected jolly instance's load in the DB to account for the new resource.
    self._update_jolly_instance_load()

    return self

  def _validate_resource_type(self):
    if self.resource_type not in JollyResource.resource_types:
      self.abort('Invalid resource type: {}'.format(self.resource_type))

  def _select_jolly_instance(self):
    try:
      self.jolly_instance = SelectJollyInstanceService(
        self.resource_type
      ).perform().jolly_instance
    except SelectJollyInstanceException as e:
      self.abort(e)
    except BaseException as e:
      self.abort('Unexpected error while selecting '
                 'JollyInstance for {}: {}'.format(self.resource_type, e))

  def _create_jolly_resource(self):
    # Create JollyResource model.
    self.jolly_resource = JollyResource(
      self.resource_id,
      self.resource_type,
      self.jolly_instance.instance,
    )

    # Write JollyResource to the DB.
    try:
      create_jolly_resource(self.jolly_resource)
    except JollyDBException as e:
      self.abort(e)
    except BaseException as e:
      self.abort('Unexpected error while creating JollyResource(resource_id={}, '
                 'resource_type={}): {}'.format(self.resource_id, self.resource_type, e))

  def _update_jolly_instance_load(self):
    try:
      UpdateJollyInstanceLoadService(
        self.jolly_instance,
        self.jolly_instance.load + self.jolly_resource.load,
      ).perform()
    except UpdateJollyInstanceException as e:
      self.abort(e)
    except BaseException as e:
      self.abort('Unexpected error while updating load of '
                 'JollyInstance {}: {}'.format(self.jolly_instance.instance, e))
