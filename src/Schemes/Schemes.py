from enum import Enum, unique


@unique
class Schemes(Enum):
    MAVEN: str = 'maven'
    PACKAGE: str = 'package'
    COMPOSER: str = 'composer'
    DOCKER: str = 'docker'
