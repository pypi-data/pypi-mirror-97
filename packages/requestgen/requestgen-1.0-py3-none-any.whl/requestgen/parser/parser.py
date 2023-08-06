from abc import abstractmethod, ABCMeta


class Parser(metaclass=ABCMeta):
    def __init__(self, command):
        self.command = command

    @abstractmethod
    def parse(self):
        print('parsing..')
        pass

    @abstractmethod
    def parse_args(self):
        print('Parsing args')
