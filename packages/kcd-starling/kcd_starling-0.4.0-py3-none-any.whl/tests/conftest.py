from datetime import datetime, timedelta

import pytest

from starling.types import MessageData


@pytest.fixture()
def message_data():
    return MessageData(
        message={'contents': 'test'},
        visibility_timeout_at=datetime.strftime(datetime.now() + timedelta(minutes=10),
                                                '%Y%m%d%H%M%S'))
