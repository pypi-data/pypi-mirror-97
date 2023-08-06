from flask_scrapinghub.chainspider.spider_base import SpiderBase
from flask_scrapinghub.utils.color import Color
from flask_scrapinghub.spider_console import SpiderSettings, SpiderConsole
from scrapinghub import ScrapinghubClient
from scrapinghub.client.exceptions import DuplicateJobError, BadRequest
from requests import ConnectionError
from flask_scrapinghub.chainspider.spider_chain import SpiderChain
import logging
import json

logger = logging.getLogger(__name__)


class FlaskScrapinghub(object):

    def __init__(self, config_prefix="SCRAPINGHUB"):
        self.settings: SpiderSettings = None
        self.console: SpiderConsole = None
        self.spider_chain: SpiderChain = None
        self.config_prefix = config_prefix

    def init_app(self, app):
        setup_file = app.config.get(f"{self.config_prefix}_SETUP_FILE", 'setup.json')
        with open(setup_file, 'r') as json_file:
            settings = json.load(json_file)
        apikey = settings.get('api-key', None)
        projects = settings.get("projects", None)
        self.settings = SpiderSettings(apikey, projects)
        self.console = SpiderConsole(self.settings)
        return self

    def init_spider_chain(self, head: SpiderBase, spider_chain_type: type = None):
        if not self.console:
            raise Exception
        if spider_chain_type:
            try:
                spider_chain = spider_chain_type(head=head,
                                             console=self.console)
            except TypeError:
                raise Exception("spider_chain_type parameters 傳入型態有誤")
        else:
            spider_chain = SpiderChain(head=head,
                                       console=self.console)
        if not isinstance(spider_chain, SpiderChain):
            raise Exception
        self.spider_chain = spider_chain
        return self

    # def __getattr__(self, name):
    #     return getattr(self.console, name)

    # def __init__(self, app=None, config_prefix="SCRAPINGHUB", spiders_mode=False, spiders_tag='none', **kwargs):
    #     # 爬蟲模式
    #     self.spiders_mode = spiders_mode
    #     self.spiders_tag = spiders_tag
    #     self.spiders_mode_index = -1
    #     self.spiders = None
    #     # 基本配置
    #     self.client = None
    #     self.setup = None
    #     self.provider_kwargs = kwargs
    #     self.config_prefix = config_prefix
    #     self.spider_signals = {}
    #     self.initialized = False
    #     if app is not None:
    #         self.init_app(app)

    # def init_app(self, app, **kwargs):
    #     if self.spiders_mode:
    #         self.spiders = []
    #         self.spiders_mode_index = 0
    #     logger.info(f"Spider Mode: {self.spiders_mode}")
    #     # 讀取 setup_development.json (預設命名 SCRAPINGHUB_SETUP_FILE)
    #     setup_file = app.config.get(f"{self.config_prefix}_SETUP_FILE", 'setup.json')
    #     # 取得 api-key，以創建client
    #     with open(setup_file, 'r') as json_file:
    #         self.setup = json.load(json_file)
    #     apikey = self.setup.get('api-key', None)
    #     if not apikey:
    #         raise SyntaxError()
    #     self.client = ScrapinghubClient(apikey)
    #
    #     # app 讀入 client
    #     if not hasattr(app, "extensions"):
    #         app.extensions = {}
    #     if app.extensions.get(self.config_prefix.lower(), None):
    #         logger.warning(
    #             f"Another FlaskScrapinghub instance using the same prefix: \"{self.config_prefix.lower()}\"! ")
    #     app.extensions[self.config_prefix.lower()] = self
    #     self.provider_kwargs.update(kwargs)
    #     # 初始化 spider_signals
    #     self.init_spider_signals()
    #     self.initialized = True

    # def make_sure_initialized(self):
    #     if not self.initialized:
    #         raise Exception('Has not initialized Error')

    # def init_spider_signals(self):
    #     projects = self.setup.get("projects", None)
    #     if not projects or len(projects) == 0:
    #         self.spider_signals = {}
    #         return
    #     for project in projects:
    #         project_instance = self.client.get_project(project)
    #         self.spider_signals[project] = {}
    #         self.spider_signals[project]["jobs"] = project_instance.jobs
    #         self.spider_signals[project]["spiders"] = []
    #         for spider in project_instance.spiders.list():
    #             self.spider_signals[project]["spiders"].append({
    #                 "name": spider['id'],
    #                 "status": self.tag_stand_by(),
    #                 "jobs": project_instance.jobs,
    #                 "items": None,
    #                 "logs": None,
    #                 "job": None
    #             })

    # def check_and_get_spider(self, project_id, spider_id):
    #     self.make_sure_initialized()
    #     project = self.spider_signals.get(project_id, None)
    #     # -----若 project_id不存在-----
    #     if not project:
    #         return None
    #     spiders = project.get("spiders", None)
    #     # -----若 project_id不存在-----
    #     if not spiders or len(spiders) == 0:
    #         return None
    #     # -----若 project中 spider不存在-----
    #     if not any(spider.get("name", None) == spider_id for spider in spiders):
    #         return None
    #     specific_spider = None
    #     for spider in self.spider_signals[project_id]['spiders']:
    #         if spider["name"] == spider_id:
    #             specific_spider = spider
    #     return specific_spider
    #
    # def view_spider_info(self, project_id, spider_id):
    #     self.make_sure_initialized()
    #     spider = self.check_and_get_spider(project_id, spider_id)
    #     # -----所指定的 spider不存在-----
    #     if not spider:
    #         return None
    #     name = spider.get('name', None)
    #     status = spider.get('status', None)
    #     jobs = spider.get('jobs', None)
    #     job = spider.get('job', None)
    #     job_status = self.get_job_status(jobs, job) if job and jobs else None
    #     info = {
    #         'name': name,
    #         'spider_status': status,
    #         'job': job,
    #         'job_status': job_status
    #     }
    #     return info
    #
    # def check_spider(self, project_id, spider_id):
    #     self.make_sure_initialized()
    #     spider = self.check_and_get_spider(project_id, spider_id)
    #     # -----所指定的 spider不存在-----
    #     if not spider:
    #         return None
    #     # -----若 spider已完成-----
    #     if spider['status'] == self.tag_finished():
    #         return Color.Red
    #     # -----若 spider待命中-----
    #     if spider['status'] == self.tag_stand_by():
    #         return Color.GREEN
    #     # -----若 spider進行中-----
    #     if spider['status'] == self.tag_running():
    #         jobs = spider.get('jobs', None)
    #         job = spider.get('job', None)
    #         if not job or not jobs:
    #             raise Exception('spider停止，但無執行中工作，程式邏輯有誤')
    #         spider_status = self.get_job_status(jobs, job)
    #         # 若已結束工作
    #         if spider_status == "finished":
    #             spider['status'] = self.tag_finished()
    #             return Color.Red
    #         return Color.YELLOW
    #     # -----若 spider停止中-----
    #     if spider['status'] == self.tag_stop():
    #         jobs = spider.get('jobs', None)
    #         job = spider.get('job', None)
    #         if not job or not jobs:
    #             raise Exception('spider停止，但無最後工作，程式邏輯有誤')
    #         spider_status = self.get_job_status(jobs, job)
    #         # 若最後工作仍在運行中
    #         if spider_status == "running":
    #             return Color.BLACK
    #         # 若最後工作已處於非運行狀態
    #         else:
    #             spider['status'] = self.tag_stand_by()
    #             spider['items'] = None
    #             spider['logs'] = None
    #             spider['job'] = None
    #             return Color.GREEN
    #
    # def run_spider(self, project_id, spider_id, units=1, priority=4, tags=None,
    #                current_try_time=None, max_try_times=None):
    #
    #     self.make_sure_initialized()
    #     spider = self.check_and_get_spider(project_id, spider_id)
    #     # -----所指定的 spider不存在-----
    #     if not spider:
    #         return Execution.NO_SPIDER
    #     # -----若 spider已完成-----
    #     if spider['status'] == self.tag_finished():
    #         logger.warning(f"[{project_id}/{spider_id}] 已完成，需先進行資料轉移始可重新啟動")
    #         return Execution.FAIL
    #     # -----若 spider進行中-----
    #     if spider['status'] == self.tag_running():
    #         logger.warning(f"[{project_id}/{spider_id}] 進行中，無法啟動，請先停止爬蟲")
    #         return Execution.FAIL
    #     # -----若 spider停止中-----
    #     if spider['status'] == self.tag_stop():
    #         logger.warning(f"[{project_id}/{spider_id}] 停止中，再次確認當前狀態")
    #         light = self.check_spider(project_id, spider_id)
    #         if light != Color.GREEN:
    #             return Execution.FAIL
    #         else:
    #             logger.info(f"[{project_id}/{spider_id}] 已恢復，將自動嘗試啟動爬蟲")
    #             return self.run_spider(project_id, spider_id, units, priority, tags)
    #
    #     # -----若 spider待命中-----
    #     if spider['status'] == self.tag_stand_by():
    #         logger.info(f"[{project_id}/{spider_id}] 待命中，即將啟動，開始爬蟲作業")
    #
    #     try:
    #         job = self.client.get_project(project_id) \
    #             .jobs.run(spider=spider_id,
    #                       units=units,
    #                       priority=priority,
    #                       tags=tags)
    #     except DuplicateJobError:
    #         logger.warning(f"[{project_id}/{spider_id}] 相同爬蟲正在工作中，當前操作無效")
    #         spider['status'] = self.tag_running()
    #         running_summary = [i.get('summary') for i in spider['jobs'].summary() if i.get('name') == 'running'][0]
    #         if running_summary:
    #             found_spider_status = [s for s in running_summary if s.get('spider') == spider_id]
    #         else:
    #             found_spider_status = None
    #         if not found_spider_status:
    #             logger.warning(f"[{project_id}/{spider_id}] 當前無無任何爬蟲工作中記錄，邏輯有誤")
    #         elif len(found_spider_status) == 0:
    #             logger.warning(f"[{project_id}/{spider_id}] 查無此爬蟲並未工作中，邏輯有誤")
    #         else:
    #             spider_status = found_spider_status[0]
    #             key = spider_status.get('key')
    #             job = spider['jobs'].get(key)
    #             spider['job'] = key
    #             spider['items'] = job.items
    #             spider['logs'] = job.logs
    #             if key == f"{project_id}/spider['job']":
    #                 logger.info(f"[{project_id}/{spider_id}] 爬蟲存在相關工作紀錄，原任務繼續進行")
    #             else:
    #                 logger.warning(f"[{project_id}/{spider_id}] 爬蟲無相關紀錄，將立即取消該工作")
    #                 self.stop_spider(project_id, spider_id)
    #         return Execution.FAIL
    #     except BadRequest or ConnectionError:
    #         if not max_try_times:
    #             max_try_times = 5
    #         if not current_try_time:
    #             current_try_time = 1
    #         if current_try_time <= max_try_times:
    #             logger.error(f"[{project_id}/{spider_id}] 當前爬蟲請求操作失敗，嘗試次數已達上限，宣告失敗")
    #             return Execution.FAIL
    #         logger.warning(f"[{project_id}/{spider_id}] 當前爬蟲請求操作失敗，嘗試再次發送")
    #         return self.run_spider(project_id, spider_id, units, priority, tags, current_try_time + 1, max_try_times)
    #
    #     if spider["name"] == spider_id:
    #         spider['status'] = self.tag_running()
    #         spider['items'] = job.items
    #         spider['logs'] = job.logs
    #         spider['job'] = job.key
    #     return Execution.SUCCESS
    #
    # def stop_spider(self, project_id, spider_id):
    #
    #     self.make_sure_initialized()
    #     spider = self.check_and_get_spider(project_id, spider_id)
    #     # -----所指定的 spider不存在-----
    #     if not spider:
    #         return Execution.NO_SPIDER
    #     # -----若 spider已完成-----
    #     if spider['status'] == self.tag_finished():
    #         logger.warning(f"[{project_id}/{spider_id}] 已完成，無須中斷爬蟲")
    #         return Execution.FAIL
    #     # -----若 spider待命中-----
    #     if spider['status'] == self.tag_stand_by():
    #         logger.warning(f"[{project_id}/{spider_id}] 待命中，無須中斷爬蟲")
    #         return Execution.FAIL
    #     # -----若 spider停止中-----
    #     if spider['status'] == self.tag_stop():
    #         logger.warning(f"[{project_id}/{spider_id}] 停止中，無須中斷爬蟲")
    #         return Execution.FAIL
    #     # -----若 spider進行中-----
    #     if spider['status'] == self.tag_running():
    #         logger.info(f"[{project_id}/{spider_id}] 進行中，即將中斷爬蟲")
    #
    #     spider['jobs'].get(spider['job']).cancel()
    #     spider['status'] = self.tag_stop()
    #     spider['items'] = None
    #     spider['logs'] = None
    #
    #     return Execution.SUCCESS
    #
    # def resume_spider(self, project_id, spider_id):
    #
    #     self.make_sure_initialized()
    #     spider = self.check_and_get_spider(project_id, spider_id)
    #     # -----所指定的 spider不存在-----
    #     if not spider:
    #         return Execution.NO_SPIDER
    #     # -----若 spider待命中-----
    #     if spider['status'] == self.tag_stand_by():
    #         logger.warning(f"[{project_id}/{spider_id}] 待命中，無法恢復待命狀態")
    #         return Execution.FAIL
    #     # -----若 spider停止中-----
    #     if spider['status'] == self.tag_stop():
    #         logger.warning(f"[{project_id}/{spider_id}] 停止中，無法恢復待命狀態")
    #         return Execution.FAIL
    #     # -----若 spider進行中-----
    #     if spider['status'] == self.tag_running():
    #         logger.warning(f"[{project_id}/{spider_id}] 進行中，無法恢復待命狀態")
    #         return Execution.FAIL
    #     # -----若 spider已完成-----
    #     if spider['status'] == self.tag_finished():
    #         logger.info(f"[{project_id}/{spider_id}] 已完成，改為待命中狀態，並銷毀暫存資料實體")
    #         if spider["name"] == spider_id:
    #             spider['status'] = self.tag_stand_by()
    #             spider['items'] = None
    #             spider['logs'] = None
    #         return Execution.SUCCESS
    #
    # def retrieve_item(self, project_id, spider_id):
    #
    #     self.make_sure_initialized()
    #     spider = self.check_and_get_spider(project_id, spider_id)
    #     # -----所指定的 spider不存在-----
    #     if not spider:
    #         return None
    #     # -----若 spider待命中-----
    #     if spider['status'] == self.tag_stand_by():
    #         logger.warning(f"[{project_id}/{spider_id}] 待命中，不存在可供搬運資料")
    #         return None
    #     # -----若 spider停止中-----
    #     if spider['status'] == self.tag_stop():
    #         logger.warning(f"[{project_id}/{spider_id}] 停止中，不存在可供搬運資料")
    #         return None
    #     # -----若 spider進行中-----
    #     if spider['status'] == self.tag_running():
    #         logger.warning(f"[{project_id}/{spider_id}] 進行中，尚不提供可供搬運資料")
    #         return None
    #     # -----若 spider已完成-----
    #     if spider['status'] == self.tag_finished():
    #         logger.info(f"[{project_id}/{spider_id}] 已完成，將資料實體轉移至應用程式使用")
    #         job = spider.get('job', None)
    #         jobs = spider.get('jobs', None)
    #         if not job or not jobs:
    #             raise Exception("爬蟲已完成，無對應工作，程式邏輯異常")
    #         items = jobs.get(job).items
    #         if not items:
    #             raise Exception("爬蟲已完成，無可供操作實體，程式邏輯異常")
    #         return items

    # 以下為 spider mode 的功能
    # def add_spider(self, add_spider):
    #     self.make_sure_initialized()
    #     self.make_sure_spider_mode()
    #
    #     # 若傳入非 spider base物件則報錯
    #     if not isinstance(add_spider, SpiderBase):
    #         raise Exception("傳入非 spider_base 之子物件")
    #     if not self.check_and_get_spider(add_spider.project_id, add_spider.spider_id):
    #         raise Exception("傳入 spider 非紀錄之spider")
    #
    #     if not add_spider.tag:
    #         add_spider.add_tag(self.spiders_tag)
    #     # 若 add 相同 spider id 和 project id 的 spider，刪除並從後方插入
    #     index = 0
    #     for spider in self.spiders:
    #         if spider.project_id == add_spider.project_id and spider.spider_id == add_spider.spider_id:
    #             del self.spiders[index]
    #         else:
    #             index += 1
    #     self.spiders.append(add_spider)
    #     logger.info(
    #         f"[Spider Mode]: 已添加 {add_spider.project_id}/{add_spider.spider_id}, 序列:{len(self.spiders)}, 標籤: {add_spider.tag}")
    #
    # def wake_spider(self):
    #     self.make_sure_initialized()
    #     self.make_sure_spider_mode()
    #
    #     spider = self.spiders[self.spiders_mode_index]
    #
    #     light = self.check_spider(spider.project_id, spider.spider_id)
    #
    #     next_round = 0 if self.spiders_mode_index + 1 >= len(self.spiders) else self.spiders_mode_index + 1
    #
    #     self.spiders_mode_index = next_round
    #
    #     spider.react(light, next_round, self)
    #
    # def start_spider(self):
    #     self.make_sure_initialized()
    #     self.make_sure_spider_mode()
    #     # 並未加入爬蟲
    #     if len(self.spiders) == 0:
    #         logger.warning("Didn't add any spider into spiders. Cancel starting!")
    #         return
    #     logger.debug("try to start spider mode scraping")
    #     # 將當前爬蟲模式的次序歸零
    #     # new
    #     self.spiders_mode_index = 0
    #
    #     leader_spider = self.spiders[self.spiders_mode_index]
    #
    #     if leader_spider.shall_start(self):
    #         logger.debug("trying success. Spider mode scraping started")
    #         self.wake_spider()
    #
    #     else:
    #         logger.debug("trying fail. Spider mode scraping cannot pass 'shall_start()' restriction.")
    #     # old (v0.0.1)
    #     # index = self.spiders_mode_index + 1
    #     # if index >= len(self.spiders):
    #     #     index = 0
    #     # spider = self.spiders[index]
    #     # if spider.shall_start(self):
    #     #     self.wake_spider()
    #
    # def set_spiders_mode_index(self, order):
    #
    #     self.make_sure_initialized()
    #     self.make_sure_spider_mode()
    #
    #     if 0 <= order <= len(self.spiders) - 1:
    #         self.spiders_mode_index = order
    #         return True
    #     raise Exception("Setting index is out of spiders range")
    #
    # def check_spiders_status(self):
    #
    #     self.make_sure_initialized()
    #     self.make_sure_spider_mode()
    #
    #     spiders_status = {}
    #     index = 0
    #     for spider_item in self.spiders:
    #         spider = self.check_and_get_spider(spider_item.project_id, spider_item.spider_id)
    #         if not spider:
    #             raise Exception("自動爬蟲模式出現未被紀錄之spider，程式邏輯異常")
    #         spiders_status[f"{spider_item.project_id}/{spider_item.spider_id}"] = {
    #             "name": spider.get('name', None),
    #             "index": index,
    #             "status": spider.get('status', None)
    #         }
    #         index += 1
    #     return spiders_status
    #
    # def check_spiders(self):
    #
    #     self.make_sure_initialized()
    #     self.make_sure_spider_mode()
    #
    #     for spider in self.spiders:
    #         if not self.check_spider(spider.project_id, spider.spider_id):
    #             raise Exception("存在未被記錄之spider，程式邏輯異常")
    #
    # def make_sure_spider_mode(self):
    #     if not self.spiders_mode:
    #         raise Exception("Not turn on spider mode.")
    #
    # @staticmethod
    # def get_job_status(jobs, job):
    #     return jobs.get(job).metadata.get('state')

    # @classmethod
    # def tag_stand_by(cls):
    #     return "stand by"
    #
    # @classmethod
    # def tag_running(cls):
    #     return "running"
    #
    # @classmethod
    # def tag_finished(cls):
    #     return "finished"
    #
    # @classmethod
    # def tag_stop(cls):
    #     return "stop"
