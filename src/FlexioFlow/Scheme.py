from enum import Enum, unique


@unique
class Scheme(Enum):
    MAVEN: str = 'maven'
    PACKAGE: str = 'package'
    COMPOSER: str = 'composer'
    DOCKER: str = 'docker'
