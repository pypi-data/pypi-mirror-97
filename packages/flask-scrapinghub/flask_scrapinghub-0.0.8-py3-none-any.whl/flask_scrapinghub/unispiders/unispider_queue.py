import abc


class UnispiderQueue(object):

    def __init__(self):
        self.unispider_queue = None
        self.leader = None
        self.mission_start_timepoint = None

    def add_leader(self, unispider):
        if self.unispider_queue:
            print("錯誤，已經存在大隊長，建議先嘗試 dismiss()")
        else:
            self.leader = unispider
            self.unispider_queue = []
            self.unispider_queue.append(self.leader)

    def add_teammate(self, unispider):
        if not self.unispider_queue:
            print("錯誤，尚未加入大隊長建立隊列，建議先嘗試 add_leader()")
        else:
            if not isinstance(unispider, self.leader):
                print("錯誤，隊員需與大隊長相同類別，建議先嘗試 dismiss() 再重新添加隊列")
            else:
                self.unispider_queue.append(self.leader)

    def dismiss(self):
        self.unispider_queue = None
        self.leader = None

