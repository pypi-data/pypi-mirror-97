from datetime import datetime

import jsonpickle

from build.lib.cryptomodel.cryptostore_symbol_value import user_grouped_symbol_value, user_symbol_value
from cryptomodel.computed_notification import computed_notification
from cryptomodel.cryptostore import user_notification, user_transaction
from cryptomodel.cryptostore_symbol_value import total_symbol_value

DATE_FORMAT = '%Y-%m-%d'


def test_dynamic():

    cn = computed_notification()
    cn.notification_type = "BALANCE"
    cn.set_result(value=create_balance(), computed_date=datetime.now())
    out = cn.get_result()
    out2 = jsonpickle.decode(out)
    assert (out2.user_id == 1)


def create_balance():
    tsv = total_symbol_value(user_id=1, date_time_calculated=datetime.now(),
                             preferred_currency="EUR", symbol_prices=[], exchange_rates=[],
                             upper_bound_transaction_date=datetime.now(), upper_bound_symbol_rates_date=datetime.now()
                             )
    tsv.user_id = 1
    tsv.converted_value = 1
    tsv.transaction_value = 1

    t = user_transaction()
    t.user_id = 1
    t.value = 1
    t.volume = 1
    t.source = "kraken"
    t.symbol = "OXT"
    t.date = datetime.now()
    t.is_valid = True

    usv = user_symbol_value(user_id=1, converted_currency="EUR", present_price=1, transaction=t,
                            date_time_calculated=datetime.now(), exchange_rates=[], currency="EUR")

    usgv = user_grouped_symbol_value(user_id=1, symbol="OXT", volume=1, price=2, currency="EUR",
                                     date_time_calculated=datetime.now(),
                                     value_bought=1, converted_value=1)

    usgv.user_symbol_values.append(usv)

    usgv.value_bought = 1
    usgv.roi = .10

    tsv.user_grouped_symbol_values['OXT'] = usgv
    return tsv
