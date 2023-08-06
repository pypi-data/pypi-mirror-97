import abc
# from flask_scrapinghub.chainspider.spider_chain import SpiderChain


class SpiderBase(abc.ABC):

    def __init__(self, project_id, spider_id):
        self.project_id = project_id
        self.spider_id = spider_id

    @abc.abstractmethod
    def see_black(self, current_index, chain):
        """

        :param chain:
        :param current_index: int. The self position in chain
        """
        return NotImplemented

    @abc.abstractmethod
    def see_red(self, current_index, chain):
        """

        :param chain:
        :param current_index: int. The self position in chain
        """
        return NotImplemented

    @abc.abstractmethod
    def see_green(self, current_index, chain):
        """

        :param chain:
        :param current_index: int. The self position in chain
        """
        return NotImplemented

    @abc.abstractmethod
    def see_yellow(self, current_index, chain):
        """

        :param chain:
        :param current_index: int. The self position in chain
        """
        return NotImplemented
