from datetime import datetime

import jsonpickle

from cryptomodel.computed_notification import computed_notification
from cryptomodel.event_store import event_store, EVENT_TYPES, event_data
from cryptomodel.operations import OPERATIONS

DATE_FORMAT = '%Y-%m-%d'


def test_dynamic():
    cn = computed_notification()
    dt = datetime.now()
    cn.computed_date = dt
    es = event_store()
    es.key = 1
    ed = event_data()
    ed.type = EVENT_TYPES.COMPUTED_NOTIFICATION
    ed.data = jsonpickle.encode(cn)
    es.event_data = ed

    out = es.get_data_str_to_obj()
    assert (out.computed_date.year == dt.year)
    assert (out.computed_date.month == dt.month)
    assert (out.computed_date.day == dt.day)


def test_create():
    cn = computed_notification()
    cn.user_id = 1
    cn.computed_date = datetime.now()
    cn.result = "{a:1}"
    cn.check_every = "00:00"
    cn.is_active = False

    ed = event_data()
    ed.type = EVENT_TYPES.COMPUTED_NOTIFICATION
    ed.data =cn

    et = event_store.create(key=1, event_type=EVENT_TYPES.USER_NOTIFICATION, data=cn,operation=OPERATIONS.ADDED )
    cn2 = et.get_data_str_to_obj()

    assert (cn.computed_date.year == cn2.computed_date.year)
    assert (cn.check_every == cn2.check_every)


