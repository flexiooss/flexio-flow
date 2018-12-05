import abc


class Scheme:
    @abc.abstractmethod
    def set_version(self):
        pass

    @abc.abstractmethod
    def release_plan(self):
        pass
