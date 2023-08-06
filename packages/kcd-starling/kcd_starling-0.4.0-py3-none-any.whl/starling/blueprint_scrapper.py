import abc

from starling.types import ScrapperData, TaskData


class BlueprintScrapper(abc.ABC):
    def __init__(self, data: ScrapperData, actions=None):
        self.data = data
        self.valid_actions = actions if actions is not None and len(actions) > 0 else self.actions

        for action in self.valid_actions:
            self.data.actions[action] = self.tasks(action)

    def tasks(self, action):
        return [TaskData(action=action)]

    @property
    @abc.abstractmethod
    def actions(self):
        return []

    @abc.abstractmethod
    def authenticate(self):
        pass
