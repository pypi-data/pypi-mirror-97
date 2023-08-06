from flask_scrapinghub.utils.color import Color
import abc
import time


class SpiderBase(object):

    def __init__(self, project_id, spider_id, tag=None):
        self.project_id = project_id
        self.spider_id = spider_id
        self.tag = tag

    def react(self, color, next_round, client):
        if not Color:
            return
        if type(color) != Color:
            raise Exception('spider only react to color')
        if color == Color.Red:
            self.see_red(next_round, client)
        elif color == Color.YELLOW:
            self.see_yellow(next_round, client)
        elif color == Color.BLACK:
            self.see_black(next_round, client)
        else:
            self.see_green(next_round, client)

    def add_tag(self, tag):
        self.tag = tag

    def shall_start(self, client):
        return True

    @abc.abstractmethod
    def see_black(self, next_round, client):
        return NotImplemented

    @abc.abstractmethod
    def see_red(self, next_round, client):
        return NotImplemented

    @abc.abstractmethod
    def see_green(self, next_round, client):
        return NotImplemented

    @abc.abstractmethod
    def see_yellow(self, next_round, client):
        return NotImplemented


class Butterfly(SpiderBase):

    def shall_start(self, client):
        return True

    def __init__(self, project_id, spider_id):
        super().__init__(project_id, spider_id)

    def see_black(self, next_round, client):
        pass

    def see_red(self, next_round, client):
        pass

    def see_green(self, next_round, client):
        print("I am Butterfly  with green")
        time.sleep(5)
        if next_round != 0:
            client.wake_spider()
        # client.run_spider(self.project_id, self.spider_id)

    def see_yellow(self, next_round, client):
        print("I am Butterfly  with yellow")


class Bee(SpiderBase):

    def __init__(self, project_id, spider_id):
        super().__init__(project_id, spider_id)

    def shall_start(self, client):
        return True

    def see_black(self, next_round, client):
        pass

    def see_red(self, next_round, client):
        pass

    def see_green(self, next_round, client):
        print("I am Bee with green")
        time.sleep(5)
        if next_round != 0:
            client.wake_spider()
        # client.run_spider(self.project_id, self.spider_id)

    def see_yellow(self, next_round, client):
        print("I am Butterfly  with yellow")
