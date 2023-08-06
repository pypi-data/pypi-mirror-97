from jolly.services.abstract_jolly_service import AbstractJollyService
from jolly.exp import *
from jolly.logger import logger
from jolly.db import update_jolly_instance_load
from jolly.config import config


class UpdateJollyInstanceLoadService(AbstractJollyService):

  def __init__(self, jolly_instance, new_load, **kwargs):
    super(UpdateJollyInstanceLoadService, self).__init__(exp=UpdateJollyInstanceException, **kwargs)
    self.jolly_instance = jolly_instance
    self.new_load = new_load

  def perform(self):
    logger.info('Updating load of JollyInstance {} to {}...'.format(
      self.jolly_instance.instance, self.new_load))

    # Update load in the DB.
    self._update_jolly_instance()

    # Check if the Jolly cluster needs to scale.
    self._determine_if_cluster_should_scale()

    return self

  def _update_jolly_instance(self):
    try:
      update_jolly_instance_load(self.jolly_instance.instance, self.new_load)
    except JollyDBException as e:
      self.abort(e)
    except BaseException as e:
      self.abort('Unexpected error while updating load of JollyInstance '
                 '{}: {}'.format(self.jolly_instance.instance, e))

  def _determine_if_cluster_should_scale(self):
    if self._cluster_should_scale():
      self._schedule_scale_cluster_job()

  def _cluster_should_scale(self):
    return self.new_load > config.BALANCED_MAX_INSTANCE_LOAD

  def _schedule_scale_cluster_job(self):
    logger.info(
      'Balanced max instance load crossed on Jolly instance {} ({}/{}) -- '
      'Scheduling job to scale up the Jolly cluster...'.format(
        self.jolly_instance.instance, self.new_load, config.BALANCED_MAX_INSTANCE_LOAD))
    # TODO