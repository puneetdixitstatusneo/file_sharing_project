import os
from datetime import timedelta

import yaml
from yaml.loader import Loader

basedir = os.path.abspath(os.path.dirname(__file__))
env = os.getenv("FLASK_ENV") or "dev"


def construct_timedelta(loader, node):
    """
    A custom constructor that is used to parse the YAML tag !timedelta in the configuration
    file and convert it into a Python timedelta object.
    :param loader:
    :param node:
    :return:
    """
    value = loader.construct_scalar(node)
    return timedelta(**{value.split()[1]: int(value.split()[0])})


yaml.add_constructor("!timedelta", construct_timedelta)  # handle timedelta in yaml file.

with open(os.path.join(basedir, env + ".yaml")) as config_file:
    config = yaml.load(config_file, Loader=Loader)

with open(os.path.join(basedir, "test.yaml")) as test_config_file:
    test_config = yaml.load(test_config_file, Loader=Loader)

with open(os.path.join(basedir, "prod.yaml")) as prod_config_file:
    prod_config = yaml.load(prod_config_file, Loader=Loader)


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = config.get("SQLALCHEMY_DATABASE_URI")
    JWT_SECRET_KEY = config.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = config.get("JWT_ACCESS_TOKEN_EXPIRES")
    JWT_REFRESH_TOKEN_EXPIRES = config.get("JWT_REFRESH_TOKEN_EXPIRES")
    SECRET_KEY = config.get("SECRET_KEY")
    PROPAGATE_EXCEPTIONS = config.get("PROPAGATE_EXCEPTIONS")
    SERVER_PATH = config.get("SERVER_PATH")
    DEBUG = True


class TestingConfig:
    SQLALCHEMY_DATABASE_URI = test_config.get("SQLALCHEMY_DATABASE_URI")
    JWT_SECRET_KEY = test_config.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = test_config.get("JWT_ACCESS_TOKEN_EXPIRES")
    JWT_REFRESH_TOKEN_EXPIRES = test_config.get("JWT_REFRESH_TOKEN_EXPIRES")
    SECRET_KEY = test_config.get("SECRET_KEY")
    PROPAGATE_EXCEPTIONS = test_config.get("PROPAGATE_EXCEPTIONS")
    SERVER_PATH = config.get("SERVER_PATH")
    DEBUG = True


class ProductionConfig():
    SQLALCHEMY_DATABASE_URI = prod_config.get("SQLALCHEMY_DATABASE_URI")
    JWT_SECRET_KEY = prod_config.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = prod_config.get("JWT_ACCESS_TOKEN_EXPIRES")
    JWT_REFRESH_TOKEN_EXPIRES = prod_config.get("JWT_REFRESH_TOKEN_EXPIRES")
    SECRET_KEY = prod_config.get("SECRET_KEY")
    PROPAGATE_EXCEPTIONS = prod_config.get("PROPAGATE_EXCEPTIONS")
    SERVER_PATH = config.get("SERVER_PATH")
    DEBUG = False


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)
print(config_by_name)
