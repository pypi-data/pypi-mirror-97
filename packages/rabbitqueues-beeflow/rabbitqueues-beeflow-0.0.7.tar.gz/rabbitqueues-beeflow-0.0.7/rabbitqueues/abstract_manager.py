import abc


class AbstractManager(abc.ABC):
    @abc.abstractmethod
    def execute(self, data):
        pass
