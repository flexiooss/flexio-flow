import json
import os


class TestPackageHelper:
    PACKAGE_WITHOUT_DEV_DEPENDENCIES = 'package_without_dev_dependencies.json'
    PACKAGE_WITH_DEV_DEPENDENCIES = 'package_with_dev_dependencies.json'

    @classmethod
    def get_json_without_dev_dependencies(cls) -> dict:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/' + cls.PACKAGE_WITHOUT_DEV_DEPENDENCIES,
                  'r') as openfile:
            data = json.load(openfile)
            return data

    @classmethod
    def get_json_with_dev_dependencies(cls) -> dict:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/' + cls.PACKAGE_WITH_DEV_DEPENDENCIES,
                  'r') as openfile:
            data = json.load(openfile)
            return data
