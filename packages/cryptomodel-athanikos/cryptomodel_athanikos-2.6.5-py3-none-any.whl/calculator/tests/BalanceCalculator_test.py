from datetime import date, datetime

from mongoengine import Q

from calculator.tests.helpers import insert_prices_record_with_method, get_prices_with_int_date_record
from config import configure_app
from cryptomodel.coinmarket import prices, Coin, EUR, EURQuote, Status
from cryptomodel.fixer import exchange_rates
from cryptomodel.cryptostore import user_transaction
from calculator.BalanceCalculator import BalanceCalculator
from cryptomodel.helpers import do_connect

DATE_FORMAT = '%Y-%m-%d'


def test_one_transaction():
    the_prices = ({"XTZ": EUR(price=1)})

    xtz_trans = user_transaction(user_id=1, volume=31.182, symbol="XTZ", value=176.08408,
                                 price=2.44, date="2020-07-15",
                                 source="kraken",
                                 source_id="",
                                 type="TRADE",
                                 order_type="BUY")

    bc = BalanceCalculator(transactions=[xtz_trans],
                           preferred_currency="EUR", symbol_rates=the_prices, exchange_rates=[],
                           upper_bound_symbol_rates_date="2040-07-15", upper_bound_transaction_date="2040-07-15")

    out = bc.compute(user_id=1, date="2040-07-15")

    assert (out.converted_value == 31.182)


def test_no_symbols_should_not_throw_exception_should_mark_trans_invalid():
    the_prices = {}

    xtz_trans = user_transaction(user_id=1, volume=31.182, symbol="XTZ", value=176.08408,
                                 price=2.44, date="2020-07-15",
                                 source="kraken",
                                 source_id="",
                                 type="TRADE",
                                 order_type="BUY")

    bc = BalanceCalculator(transactions=[xtz_trans],
                           preferred_currency="EUR", symbol_rates=the_prices, exchange_rates=[],
                           upper_bound_symbol_rates_date="2040-07-15", upper_bound_transaction_date="2040-07-15")

    out = bc.compute(user_id=1, date="2040-07-15")
    assert (out.transactions[0].is_valid == False)
    assert (out.converted_value == 0)


def test_none_symbols_should_not_throw_exception_should_mark_trans_invalid():
    the_prices = None

    xtz_trans = user_transaction(user_id=1, volume=31.182, symbol="XTZ", value=176.08408,
                                 price=2.44, date="2020-07-15",
                                 source="kraken",
                                 source_id="",
                                 type="TRADE",
                                 order_type="BUY")

    bc = BalanceCalculator(transactions=[xtz_trans],
                           preferred_currency="EUR", symbol_rates=the_prices, exchange_rates=[],
                           upper_bound_symbol_rates_date="2040-07-15", upper_bound_transaction_date="2040-07-15")

    out = bc.compute(user_id=1, date="2040-07-15")
    assert (out.transactions[0].is_valid == False)
    assert (out.converted_value == 0)


def test_five_distinct_symbols():
    the_prices = {
        "XTZ": EUR(price=2.45),
        "ADA": EUR(price=.11862),
        "TRX": EUR(price=0.0161217),
        "XLM": EUR(price=0.08713060),
        "XRP": EUR(price=0.24919500),
    }

    xtz_trans = user_transaction(user_id=1, volume=31.182, symbol="XTZ", value=76.64,
                                 price=2.44, date="2020-07-15",
                                 source="kraken",
                                 source_id="",
                                 type="TRADE",
                                 order_type="BUY")
    ada_trans = user_transaction(user_id=1, volume=2076.384678, symbol="ADA", value=244.968,
                                 price=.118, date="2020-07-15",
                                 source="kraken",
                                 source_id="",
                                 type="TRADE",
                                 order_type="BUY")
    xlm_trans = user_transaction(user_id=1, volume=1796, symbol="XLM", value=149.068,
                                 price=0.08738980, date="2020-07-15",
                                 source="kraken",
                                 source_id="",
                                 type="TRADE",
                                 order_type="BUY")

    xrp_trans = user_transaction(user_id=1, volume=1010.8, symbol="XRP", value=212.268,
                                 price=.21, date="2020-07-15",
                                 source="kraken",
                                 source_id="",
                                 type="TRADE",
                                 order_type="BUY")

    trx_trans = user_transaction(user_id=1, volume=6420, symbol="TRX", value=103.5174,
                                 price=0.01612420, date="2020-07-15",
                                 source="kraken",
                                 source_id="",
                                 type="TRADE",
                                 order_type="BUY")

    bc = BalanceCalculator(transactions=[xtz_trans, xrp_trans, ada_trans, xlm_trans, trx_trans],
                           preferred_currency="EUR", symbol_rates=the_prices, exchange_rates=[],
                           upper_bound_symbol_rates_date="2040-07-15", upper_bound_transaction_date="2040-07-15")

    out = bc.compute(user_id=1, date="2040-07-15")

    assert (out.converted_value == 2.45 * 31.182
            + .11862 * 2076.384678
            + 0.0161217 * 6420
            + 0.08713060 * 1796
            + 0.24919500 * 1010.8)


def test_roi():
    the_prices = {
        "XTZ": EUR(price=2),
        "ADA": EUR(price=3),

    }

    xtz_trans = user_transaction(user_id=1, volume=30, symbol="XTZ", value=31.182,
                                 price=1, date="2020-07-15",
                                 source="kraken",
                                 source_id="",
                                 type="TRADE",
                                 order_type="BUY")
    ada_trans = user_transaction(user_id=1, volume=20, symbol="ADA", value=40,
                                 price=2, date="2020-07-15",
                                 source="kraken",
                                 source_id="",
                                 type="TRADE",
                                 order_type="BUY")

    bc = BalanceCalculator(transactions=[xtz_trans, ada_trans],
                           preferred_currency="EUR", symbol_rates=the_prices, exchange_rates=[],
                           upper_bound_symbol_rates_date="2040-07-15", upper_bound_transaction_date="2040-07-15")

    out = bc.compute(user_id=1, date="2040-07-15")
    assert (len(out.user_grouped_symbol_values) == 2)
    assert out.user_grouped_symbol_values['ADA'].roi == ((3 * 20) - (40)) / (40)
    assert out.roi == ((2 * 30 + 3 * 20) - (40 + 31.182)) / (40 + 31.182)


def test_volume():
    the_prices = {
        "XTZ": EUR(price=2),
        "ADA": EUR(price=3),

    }

    xtz_trans = user_transaction(user_id=1, volume=30, symbol="XTZ", value=31.182,
                                 price=1, date="2020-07-15",
                                 source="kraken",
                                 source_id="",
                                 type="TRADE",
                                 order_type="BUY")
    ada_trans = user_transaction(user_id=1, volume=20, symbol="XTZ", value=40,
                                 price=2, date="2020-07-15",
                                 source="kraken",
                                 source_id="",
                                 type="TRADE",
                                 order_type="SELL")

    bc = BalanceCalculator(transactions=[xtz_trans, ada_trans],
                           preferred_currency="EUR", symbol_rates=the_prices, exchange_rates=[],
                           upper_bound_symbol_rates_date="2040-07-15", upper_bound_transaction_date="2040-07-15")

    out = bc.compute(user_id=1, date="2040-07-15")
    assert out.user_grouped_symbol_values['XTZ'].volume == 10


def test_roi_with_buy_sell_and_deposit():
    the_prices = {
        "XTZ": EUR(price=2),
        "ADA": EUR(price=3),

    }

    ada_trans_1 = user_transaction(user_id=1, volume=30, symbol="ADA", value=50,
                                   price=2, date="2020-07-15",
                                   source="kraken",
                                   source_id="",
                                   type="TRADE",
                                   order_type="BUY")

    ada_trans_2 = user_transaction(user_id=1, volume=20, symbol="ADA", value=40,
                                   price=2, date="2020-07-15",
                                   source="kraken",
                                   source_id="",
                                   type="TRADE",
                                   order_type="SELL")

    ada_trans_3 = user_transaction(user_id=1, volume=10, symbol="ADA", value=40,
                                   price=2, date="2020-07-15",
                                   source="kraken",
                                   source_id="",
                                   type="TRADE",
                                   order_type="BUY")

    deposit_trans = user_transaction(user_id=1, volume=13, symbol="EUR", value=40,
                                     price=1000, date="2020-07-15",
                                     source="kraken",
                                     source_id="",
                                     type="DEPOSIT",
                                     order_type="NONE")

    bc = BalanceCalculator(transactions=[ada_trans_1, ada_trans_2, ada_trans_3, deposit_trans],
                           preferred_currency="EUR", symbol_rates=the_prices, exchange_rates=[],
                           upper_bound_symbol_rates_date="2040-07-15", upper_bound_transaction_date="2040-07-15")

    out = bc.compute(user_id=1, date="2040-07-15")

    assert (len(out.user_grouped_symbol_values) == 1)

    assert out.user_grouped_symbol_values['ADA'].volume == 20

    assert out.user_grouped_symbol_values['ADA'].roi == (20 * 3 - (50 - 40 + 40)) / (50 - 40 + 40)

    assert out.roi == (20 * 3 - (50 - 40 + 40)) / (50 - 40 + 40)


def test_price_date_type():
    do_connect(configure_app())
    dt_now =int(datetime(year = 2021, month=1, day=1 ).timestamp()) * 1000
    prices.objects.all().delete()
    insert_prices_record_with_method(get_prices_with_int_date_record)
    prc = prices.objects(Q( status__timestamp__lt = dt_now)).order_by(
        '-status__timestamp')[:10]
    assert (len(prc) == 1)

    dt_now = int(datetime(year=2018, month=1, day=1).timestamp()) * 1000 #?
    prc = prices.objects(Q( status__timestamp__lt = dt_now)).order_by(
        '-status__timestamp')[:10]
    assert (len(prc) == 0)