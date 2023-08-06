import abc
from flask_scrapinghub.chainspider.spider_base import SpiderBase
from flask_scrapinghub.spider_console import SpiderConsole
from flask_scrapinghub.utils.color import Color
from datetime import datetime
import time


class SpiderChain:

    def __init__(self, head: SpiderBase, console: SpiderConsole):
        self.__console = console
        if not self.__console.check_spider_color(head.project_id, head.spider_id):
            # todo: 所輸入乃 console 記錄中不存在的 spider
            raise Exception
        self.__head = head
        self.__start_execution_time = None
        self.__current_index = 0
        self.__chain = []
        self.add(self.__head)

    def reset(self, head: SpiderBase):
        """
        note:
            初始化 chain
        """
        if not self.__console.check_spider_color(head.project_id, head.spider_id):
            # todo: 所輸入乃 console 記錄中不存在的 spider
            raise Exception
        self.__head = head
        self.__chain = []

    def add(self, mate: SpiderBase):
        """
        note:
            在 SpiderChain中添加 繼承至SpiderBase的物件。
            若當前為空 Chain，則加入的對象會成為 head，且會要求後來加入者與 head 為同類型;
            若當前為空 Chain，則加入對象為 mate，並且會檢查是否與head同類型、且檢查是否有相同 mate 的存在。。

        :type mate: SpiderBase
        """
        # if not isinstance(mate, type(self.head)):
        #     # todo: 加入與 head 不同類型的 mate
        #     raise Exception
        for m in self.__chain:
            if mate.project_id == m.project_id and mate.spider_id == m.spider_id:
                # todo: 已存在相同 mate
                raise Exception
        if not self.__console.check_spider_color(mate.project_id, mate.spider_id):
            # todo: 所輸入乃 console 記錄中不存在的 spider
            raise Exception
        self.__chain.append(mate)

    @property
    def length(self):
        return len(self.__chain)

    def start(self):
        if not self.shall_start(self.__head):
            # todo: 未通過 shall start 檢測
            return
        self.__start_execution_time = datetime.now()
        self.__current_index = 0
        self.execute_node()

    def execute_node(self):
        node = self.__chain[self.__current_index]
        color = self.__console.check_spider_color(node.project_id, node.spider_id)
        if color is Color.Red:
            node.see_red(self.__current_index, self)
        elif color is Color.YELLOW:
            node.see_yellow(self.__current_index, self)
        elif color is Color.BLACK:
            node.see_black(self.__current_index, self)
        else:
            node.see_green(self.__current_index, self)

    def execute_next_node(self):
        self.__current_index = 0 if self.__current_index + 1 >= len(self.__chain) \
                                 else self.__current_index + 1
        self.execute_node()

    def try_execute_again_after_interval(self, check_interval_sec: int = 30):
        time.sleep(check_interval_sec)
        self.execute_node()

    def take_items(self, mate: SpiderBase):
        items = self.__console.take_items_from_spider(mate.project_id, mate.spider_id)
        return items

    def run_node(self, mate: SpiderBase):
        execution = self.__console.run_spider(mate.project_id, mate.spider_id)
        return execution

    def shut_all(self):
        for node in self.__chain:
            execution = self.__console.stop_spider(node.project_id, node.spider_id)
            if not execution:
                # todo: project_id 或 spider_id 異常
                raise Exception

    def resume_all(self):
        for node in self.__chain:
            execution = self.__console.resume_spider(node.project_id, node.spider_id)
            if not execution:
                # todo: project_id 或 spider_id 異常
                raise Exception

    def check_all(self):
        status_list = list()
        for node in self.__chain:
            color = self.__console.check_spider_color(node.project_id, node.spider_id)
            if not color:
                # todo: project_id 或 spider_id 異常
                raise Exception
            status_list.append(color)
        return status_list

    def execution_total_time(self):
        """

        :return: todo: 回傳值
        """
        if not self.__start_execution_time:
            return None
        return datetime.now() - self.__start_execution_time

    @abc.abstractmethod
    def shall_start(self, head):
        return True
