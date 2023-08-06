import time

from datetime import datetime, timedelta

import pytest

from starling.app import Scrapper
from starling.blueprint_action import BlueprintAction
from starling.blueprint_scrapper import BlueprintScrapper
from starling.exception import RetryTaskExitError, RetryTaskDoneError, RetryTaskError
from starling.types import ScrapperData, TaskData, MessageData, FetchedData, PloverDataType


class MyScrapper(BlueprintScrapper):
    def tasks(self, action):
        if action == 'tests.starling.test_app.MyAction1':
            return [
                TaskData(action=action, criteria={'from': '20191001', 'to': '20191031'}),
                TaskData(action=action, criteria={'from': '20191101', 'to': '20191130'})
            ]
        return [TaskData(action=action)]

    @property
    def actions(self):
        return [
            'tests.starling.test_app.MyAction1',
            'tests.starling.test_app.MyAction2',
            'tests.starling.test_app.MyAction3'
        ]

    def authenticate(self):
        pass


class MyValidScrapper(BlueprintScrapper):
    @property
    def actions(self):
        return [
            'tests.starling.test_app.MyAction4'
        ]

    def authenticate(self):
        pass


class MyInvalidScrapper(BlueprintScrapper):
    @property
    def actions(self):
        return [
            'tests.starling.test_app.MyAction5'
        ]

    def authenticate(self):
        pass


class MyAttributeErrorScrapper(BlueprintScrapper):
    @property
    def actions(self):
        return [
            'tests.starling.test_app.MyMyAction1'
        ]

    def authenticate(self):
        pass


class MyRetryScrapper(BlueprintScrapper):
    @property
    def actions(self):
        return [
            'tests.starling.test_app.MyAction1',
            'tests.starling.test_app.MyAction6',
            'tests.starling.test_app.MyAction7',
            'tests.starling.test_app.MyAction2'
        ]

    def authenticate(self):
        pass


class MyDurationScrapper(BlueprintScrapper):
    @property
    def actions(self):
        return [
            'tests.starling.test_app.MyAction8',
        ]

    def authenticate(self):
        time.sleep(1)
        pass


class MyAction1(BlueprintAction):
    def fetch(self) -> FetchedData:
        self.scrapper_data.broadcast_variables['v1'] = 1
        return FetchedData(data=self.scrapper_data.candidate, plover_data=self.scrapper_data.candidate,
                           plover_data_type=PloverDataType.DICT)

    def interval(self):
        return 0


class MyAction2(BlueprintAction):
    def fetch(self) -> FetchedData:
        if self.scrapper_data.broadcast_variables.get('v1') is None:
            raise RetryTaskExitError('v1 is required')
        return FetchedData(data=[{'a': 1}, {'a': 2}, {'a': 3}, {'a': 4}, {'a': 5}])


class MyAction3(BlueprintAction):
    def fetch(self):
        data = {
            'a': [{'a': 1}, {'a': 2}, {'a': 3}],
            'b': {'a': 1, 'b': 2}
        }
        return FetchedData(data=data, plover_data=data, plover_data_type=PloverDataType.COMBINED)


class MyAction4(BlueprintAction):
    def fetch(self):
        raise RetryTaskExitError('invalid id', {'is_valid': True})


class MyAction5(BlueprintAction):
    def fetch(self):
        raise RetryTaskExitError('ip blocked')


class MyAction6(BlueprintAction):
    def fetch(self):
        raise RetryTaskDoneError('done', {'name': 'test'})


class MyAction7(BlueprintAction):
    def fetch(self):
        raise RetryTaskError('retry')


class MyAction8(BlueprintAction):
    def fetch(self):
        time.sleep(0.5)
        return FetchedData(data=[], plover_data=[], plover_data_type=PloverDataType.LIST)

    def interval(self):
        return 0.3


def test_scrapper():
    res = Scrapper.run(
        MyScrapper(ScrapperData('scrap_id', 'place', {'place_id': '123123'},
                                MessageData(
                                    message={'contents': 'test'},
                                    visibility_timeout_at=datetime.strftime(datetime.now() + timedelta(minutes=10),
                                                                            '%Y%m%d%H%M%S')))))
    assert len(res.actions) == 3
    assert len(res.actions['tests.starling.test_app.MyAction1']) == 2
    assert len(res.actions['tests.starling.test_app.MyAction2']) == 1
    assert res.actions['tests.starling.test_app.MyAction1'][0].criteria['from'] == '20191001'
    assert res.actions['tests.starling.test_app.MyAction1'][1].criteria['from'] == '20191101'
    assert res.actions['tests.starling.test_app.MyAction1'][0].fetched_data.plover_data_type == PloverDataType.DICT
    assert res.actions['tests.starling.test_app.MyAction2'][0].fetched_data.data[0] == {'a': 1}
    assert res.actions['tests.starling.test_app.MyAction3'][
               0].fetched_data.plover_data_type == PloverDataType.COMBINED


def test_valid_scrapper(message_data):
    res = Scrapper.run(
        MyValidScrapper(ScrapperData('scrap_id', 'place', {'place_id': '123123'}, message=message_data)))
    assert len(res.actions) == 1
    assert res.is_valid is True


def test_invalid_scrapper(message_data):
    res = Scrapper.run(
        MyInvalidScrapper(ScrapperData('scrap_id', 'place', {'place_id': '123123'}, message=message_data)))
    assert len(res.actions) == 1
    assert res.is_valid is False


def test_scrapper_actions(message_data):
    res = Scrapper.run(MyScrapper(ScrapperData('scrap_id', 'place', {'place_id': '123123'}, message=message_data),
                                  actions=[
                                      'tests.starling.test_app.MyAction1',
                                      'tests.starling.test_app.MyAction3'
                                  ]))
    assert len(res.actions) == 2


def test_scrapper_with_attribute_error(message_data):
    with pytest.raises(AttributeError) as e:
        Scrapper.run(
            MyAttributeErrorScrapper(ScrapperData('scrap_id', 'place', {'place_id': '123123'}, message=message_data)))

    assert "module" in str(e.value)


def test_retry_scrapper(message_data):
    res = Scrapper.run(
        MyRetryScrapper(ScrapperData('scrap_id', 'place', {'place_id': '123123'}, message=message_data)))
    assert len(res.actions) == 4
    assert len(res.actions['tests.starling.test_app.MyAction2']) == 1
    assert res.actions['tests.starling.test_app.MyAction2'][0].is_done is False
    assert res.actions['tests.starling.test_app.MyAction6'][0].is_done is True
    assert res.actions['tests.starling.test_app.MyAction6'][0].error['msg'] == 'done'
    assert res.actions['tests.starling.test_app.MyAction6'][0].error['extra']['name'] == 'test'


def test_scrapper_durations(message_data):
    res = Scrapper.run(
        MyDurationScrapper(ScrapperData('scrap_id', 'place', {'place_id': '123123'}, message=message_data)))
    assert res.durations['authenticate'] == 1
    assert len(res.durations['actions']) == 1
