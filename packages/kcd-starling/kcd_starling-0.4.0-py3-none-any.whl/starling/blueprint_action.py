import abc

from starling.types import TaskData, ScrapperData, FetchedData


class BlueprintAction(abc.ABC):
    def __init__(self, scrapper_data: ScrapperData, task_data: TaskData):
        self.scrapper_data: 'ScrapperData' = scrapper_data
        self.task_data: 'TaskData' = task_data

    @abc.abstractmethod
    def fetch(self) -> FetchedData:
        pass

    def interval(self):
        return 0
