from scrapinghub import ScrapinghubClient
from flask_scrapinghub.utils.tag import Tag
from flask_scrapinghub.utils.color import Color
from flask_scrapinghub.utils.execution import Execution


class SpiderSettings:

    def __init__(self, apikey: str, projects: list):
        self.api_key = apikey
        self.projects = projects


class SpiderSig:

    def __init__(self, spider_id):
        self.id = spider_id
        self.tag = Tag.STAND_BY
        self.__job_key = None

    def set_job_key(self, job_key):
        self.__job_key = job_key

    def release_job_key(self):
        self.__job_key = None

    def job_key(self):
        return self.__job_key

    def to_standby(self):
        self.tag = Tag.STAND_BY

    def to_running(self):
        self.tag = Tag.RUNNING

    def to_finished(self):
        self.tag = Tag.FINISHED

    def to_stop(self):
        self.tag = Tag.STOP


class ScrapinghubService:

    def __init__(self, api_key):
        self.client = ScrapinghubClient(api_key)

    def __get_project(self, project_id):
        """

        :param project_id: string project id
        :return: Project 實體 (class: ~scrapinghub.client.projects.Project)
        """
        return self.client.projects.get(project_id)

    def __get_jobs(self, project_id):
        """

        :param project_id: string project id
        :return: Jobs 實體 (class: ~scrapinghub.client.jobs.Jobs)
        """
        return self.client.projects.get(project_id).jobs

    def run_spider_job(self, project_id, unit: SpiderSig):
        """

        :param project_id: string project id
        :param unit: unit of project (class: SpiderUnit).
        :return: a string of executed job key
        """
        job = self.__get_jobs(project_id).run(
                                      spider=unit.id,
                                      units=None, priority=None, meta=None,
                                      add_tag=None, job_args=None, job_settings=None, cmd_args=None,
                                      environment=None)
        return job.key

    def cancel_job(self, project_id, job_key: str):
        """

        :param project_id: string project id
        :param job_key: a string of executed job key
        """
        self.__get_jobs(project_id).get(job_key).cancel()

    def retrieve_unit_state(self, project_id, unit: SpiderSig):
        """

        :param project_id: string project id
        :param unit: unit of project (class: SpiderSig).
        :return: a string of unit job state
        """
        state = self.__get_jobs(project_id).get(unit.job_key()).metadata.get('state') \
            if unit.job_key else None
        return state

    def retrieve_unit_items(self, project_id, unit: SpiderSig):
        """

        :param project_id: string project id
        :param unit: unit of project (class: SpiderSig).
        :return: items (class:`~scrapinghub.client.items.Items` resource object).
        """

        items = self.__get_jobs(project_id).get(unit.job_key()).items \
            if unit.job_key else None

        return items

    def retrieve_unit_logs(self, project_id, unit: SpiderSig):
        """

        :param project_id: string project id
        :param unit: unit of project (class: SpiderSig).
        :return: logs (class:`~scrapinghub.client.logs.Logs` resource object).
        """
        logs = self.__get_project(project_id).jobs.get(unit.job_key).logs \
            if unit.job_key else None
        return logs

    def get_project_spiders_list(self, project_id):
        """

        :param project_id: string project id
        :return: a list of spiders for a project
        [{'id': 'spider1', 'tags': [], 'type': 'manual', 'version': '123'},
         {'id': 'spider2', 'tags': [], 'type': 'manual', 'version': '123'}]
        """
        spiders_list = self.__get_project(project_id).spiders.list()
        return spiders_list


class SpiderSignalsCenter:

    def __init__(self):
        self.__spider_signals = {}

    @classmethod
    def build_signals_center(cls, projects_list, center_client: ScrapinghubService):
        sig_center = SpiderSignalsCenter()
        for project_id in projects_list:
            project_spiders_list = center_client.get_project_spiders_list(project_id)
            sig_center.__spider_signals[project_id] = {}
            sig_center.__spider_signals[project_id]["spiders"] = list()
            for spider_item in project_spiders_list:
                sig_center.__spider_signals[project_id]["spiders"].append(SpiderSig(spider_item['id']))
        return sig_center

    def __get_spider(self, project_id, spider_id):
        """ 取得 spider

        :param project_id: string
        :param spider_id: string
        :return: self.spider_signals 中 project_id底下的spiders陣列中的spider

        ex: {'name': 'spider1',
             'status': (Tag type)}
        """
        project = self.__spider_signals.get(project_id, None)
        if not project:
            return None
        spiders = project.get("spiders", None)
        if not spiders or len(spiders) == 0:
            return None
        for spider in spiders:
            if spider.id == spider_id:
                return spider
        return None

    def try_get_sig(self, project_id, spider_id):
        spider_sig = self.__get_spider(project_id, spider_id)
        if not spider_sig:
            return None
        return spider_sig

    def tag_stand_by(self, project_id, spider_id):
        spider_sig = self.__get_spider(project_id, spider_id)
        if not spider_sig:
            raise Exception
        spider_sig.to_standby()

    def tag_running(self, project_id, spider_id):
        spider_sig = self.__get_spider(project_id, spider_id)
        if not spider_sig:
            raise Exception
        spider_sig.to_running()

    def tag_finished(self, project_id, spider_id):
        spider_sig = self.__get_spider(project_id, spider_id)
        if not spider_sig:
            raise Exception
        spider_sig.to_finished()

    def tag_stop(self, project_id, spider_id):
        spider_sig = self.__get_spider(project_id, spider_id)
        if not spider_sig:
            raise Exception
        spider_sig.to_stop()


class SpiderExecutor:

    def __init__(self, settings: SpiderSettings):
        self.client = ScrapinghubService(settings.api_key)

    def check_spider_color(self, project_id, sig: SpiderSig):
        """

        :param project_id:  a string of project id.
        :param sig: (class: `SpiderSig`).
        :return: color (class:`~flask_scrapinghub.utils.color.Color`) or None.
        """
        tag = sig.tag
        if tag is Tag.FINISHED:
            return Color.Red
        if tag is Tag.STAND_BY:
            return Color.GREEN
        state = self.client.retrieve_unit_state(project_id, sig)
        if tag is Tag.RUNNING:
            if state == "finished":
                sig.to_finished()
                return Color.Red
            else:
                return Color.YELLOW
        if tag is Tag.STOP:
            if state == "running":
                return Color.BLACK
            else:
                sig.to_standby()
                sig.release_job_key()
                return Color.GREEN

    def run_spider(self, project_id, sig: SpiderSig):
        """

        :param project_id:  a string of project id.
        :param sig: (class: `SpiderSig`).
        :return: execution (class:`~flask_scrapinghub.utils.execution.Execution`) or None.
        """
        tag = sig.tag
        if tag is Tag.FINISHED:
            return Execution.FAIL
        if tag is Tag.RUNNING:
            return Execution.FAIL
        if tag is Tag.STOP:
            return Execution.FAIL
        if tag is Tag.STAND_BY:
            job_key = self.client.run_spider_job(project_id, sig)
            sig.to_running()
            sig.set_job_key(job_key)
            return Execution.SUCCESS

    def stop_spider(self, project_id, sig: SpiderSig):
        """

        :param project_id:  a string of project id.
        :param sig: (class: `SpiderSig`).
        :return: execution (class:`~flask_scrapinghub.utils.execution.Execution`) or None.
        """
        tag = sig.tag
        if tag is Tag.FINISHED:
            return Execution.FAIL
        if tag is Tag.STAND_BY:
            return Execution.FAIL
        if tag is Tag.STOP:
            return Execution.FAIL
        if tag is Tag.RUNNING:
            self.client.cancel_job(project_id, sig.job_key())
            sig.to_stop()
            return Execution.SUCCESS

    def take_items_from_spider(self, project_id, sig: SpiderSig):
        """

        :param project_id:  a string of project id.
        :param sig: (class: `SpiderSig`).
        :return: items (class:`~scrapinghub.client.items.Items` resource object).
        """

        tag = sig.tag
        if tag is Tag.STAND_BY:
            return None
        if tag is Tag.STOP:
            return None
        if tag is Tag.RUNNING:
            return None
        if tag is Tag.FINISHED:
            return self.client.retrieve_unit_items(project_id, sig)

    def resume_spider(self, sig: SpiderSig):
        """

        :param sig: (class: `SpiderSig`).
        :return: execution (class:`~flask_scrapinghub.utils.execution.Execution`) or None.
        """
        tag = sig.tag
        if tag is Tag.STAND_BY:
            return Execution.FAIL
        if tag is Tag.STOP:
            return Execution.FAIL
        if tag is Tag.RUNNING:
            return Execution.FAIL
        if tag is Tag.FINISHED:
            sig.to_standby()
            return Execution.SUCCESS


class SpiderConsole:

    def __init__(self, settings: SpiderSettings):
        self.__executor = SpiderExecutor(settings)
        self.__sig_center = SpiderSignalsCenter\
            .build_signals_center(settings.projects, self.__executor.client)

    def check_spider_color(self, project_id, spider_id):
        sig = self.__sig_center.try_get_sig(project_id, spider_id)
        if not sig:
            return None
        return self.__executor.check_spider_color(project_id, sig)

    def run_spider(self, project_id, spider_id):
        sig = self.__sig_center.try_get_sig(project_id, spider_id)
        if not sig:
            return None
        return self.__executor.run_spider(project_id, sig)

    def stop_spider(self, project_id, spider_id):
        sig = self.__sig_center.try_get_sig(project_id, spider_id)
        if not sig:
            return None
        return self.__executor.stop_spider(project_id, sig)

    def take_items_from_spider(self, project_id, spider_id):

        sig = self.__sig_center.try_get_sig(project_id, spider_id)
        if not sig:
            return None

        return self.__executor.take_items_from_spider(project_id, sig)

    def resume_spider(self, project_id, spider_id):
        sig = self.__sig_center.try_get_sig(project_id, spider_id)
        if not sig:
            return None
        return self.__executor.resume_spider(sig)
