import os

DEV = 'dev'
STAGING = 'staging'
PROD = 'prod'

ENV = os.environ.get('ENV') or DEV


def env():
  return ENV


def is_dev():
  return ENV == DEV


def is_staging():
  return ENV == STAGING


def is_prod():
  return ENV == PROD
