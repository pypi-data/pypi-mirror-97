from enum import Enum


class EnvName(Enum):
    STAGING = "staging"
    PRODUCTION = "production"
    DEVELOPMENT = "development"
    TESTING = "testing"


def is_production(*, environment: str) -> bool:
    """Function that returns true if the environment passed as parameter is production
    :param str environment: The environment to compare
    :rtype: bool
    :return: If the environment is equal to production
    """
    return environment == EnvName.PRODUCTION.value


def is_staging(*, environment: str) -> bool:
    """Function that returns true if the environment passed as parameter is staging
    :param str environment: The environment to compare
    :rtype: bool
    :return: If the environment is equal to staging
    """
    return environment == EnvName.STAGING.value


def is_testing(*, environment: str) -> bool:
    """Function that returns true if the environment passed as parameter is testing
    :param str environment: The environment to compare
    :rtype: bool
    :return: If the environment is equal to testing
    """
    return environment == EnvName.TESTING.value


def is_development(*, environment: str) -> bool:
    """Function that returns true if the environment passed as parameter is development
    :param str environment: The environment to compare
    :rtype: bool
    :return: If the environment is equal to development
    """
    return environment == EnvName.DEVELOPMENT.value
