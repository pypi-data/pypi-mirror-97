from jolly.services.abstract_jolly_service import AbstractJollyService
from jolly.exp import *
from jolly.logger import logger
from jolly.db import get_jolly_instances


class SelectJollyInstanceService(AbstractJollyService):

  def __init__(self, resource_type, **kwargs):
    super(SelectJollyInstanceService, self).__init__(exp=SelectJollyInstanceException, **kwargs)
    self.resource_type = resource_type
    self.jolly_instances = []
    self.jolly_instance = None

  def perform(self):
    logger.info('Selecting JollyInstance for {}...'.format(self.resource_type))

    # Get all current jolly instances.
    self._get_jolly_instances()

    # Select the instance with the least load.
    self.jolly_instance = self._get_instance_with_least_load()

    return self

  def _get_jolly_instances(self):
    try:
      self.jolly_instances = get_jolly_instances()
    except JollyDBException as e:
      self.abort(e)
    except BaseException as e:
      self.abort('Unexpected error while querying '
                 'for all jolly instances: {}'.format(e))

  def _get_instance_with_least_load(self):
    return sorted(self.jolly_instances, key=lambda ji: ji.load)[0]