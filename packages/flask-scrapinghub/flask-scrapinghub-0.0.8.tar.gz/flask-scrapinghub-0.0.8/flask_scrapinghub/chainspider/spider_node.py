from flask_scrapinghub.chainspider.spider_base import SpiderBase
from flask_scrapinghub.chainspider.spider_chain import SpiderChain
from scrapinghub.client.items import Items
from flask_scrapinghub.utils.color import Color
import abc


class SpiderNode(SpiderBase):

    def __init__(self, project_id, spider_id, check_interval_sec=30):
        self.check_interval_sec = check_interval_sec
        super().__init__(project_id, spider_id)

    def see_black(self, current_index, chain: SpiderChain):
        not_meet_count = self.__not_meet_color_count(chain, Color.BLACK)
        if not_meet_count == 0:
            chain.start()
        else:
            chain.shut_all()
            chain.try_execute_again_after_interval(self.check_interval_sec)

    def see_red(self, current_index, chain: SpiderChain):
        not_meet_count = self.__not_meet_color_count(chain, Color.Red)
        if not_meet_count == 0:
            items = chain.take_items(self)
            self.feed_items(items)
            if current_index + 1 == chain.length:
                chain.resume_all()
            else:
                chain.execute_next_node()
        else:
            chain.try_execute_again_after_interval(self.check_interval_sec)

    def see_green(self, current_index, chain: SpiderChain):
        not_meet_count = self.__not_meet_color_count(chain, Color.GREEN)
        if current_index == 0:
            if not_meet_count == 0:
                execution = chain.run_node(self)
                chain.execute_next_node()
            else:
                chain.try_execute_again_after_interval(self.check_interval_sec)
        else:
            execution = chain.run_node(self)
            chain.execute_next_node()

    def see_yellow(self, current_index, chain: SpiderChain):
        not_meet_count = self.__not_meet_color_count(chain, Color.Red)
        chain.try_execute_again_after_interval(self.check_interval_sec)
        # if not_meet_count == 0:
        #     chain.execute_next_node()
        # else:
        #     chain.try_execute_again_after_interval(self.check_interval_sec)

    @classmethod
    def __not_meet_color_count(cls, chain: SpiderChain, specific_color: Color):
        all_color = chain.check_all()
        not_meet_count = 0
        for color in all_color:
            if color is not specific_color:
                not_meet_count += 1
        return not_meet_count

    @abc.abstractmethod
    def feed_items(self, items):
        return NotImplemented
