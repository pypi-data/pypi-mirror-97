import json
import pymongo
import pytest
import mock

from cryptomodel.config import configure_app
from cryptomodel.helpers import get_url


def get_exchange_rates_record():
    with open('sample_records/exchange_rate.json', 'r') as my_file:
        return json.load(my_file)


def get_prices_record():
    with open('sample_records/price.json', 'r') as my_file:
        return json.load(my_file)


def get_prices_2020706_record():
    with open('sample_records/prices_2020706.json', 'r') as my_file:
        return json.load(my_file)


def get_prices20200812039_record():
    with open('sample_records/prices2020-08-01T20:39.json', 'r') as my_file:
        return json.load(my_file)


def get_prices20200801T2139_record():
    with open('sample_records/prices2020-08-01T21:39.json', 'r') as my_file:
        return json.load(my_file)


def get_prices_with_int_date_record():
    with open('sample_records/prices_with_int_date.json', 'r') as my_file:
        return json.load(my_file)



def insert_prices_record():
    config = configure_app()
    client = pymongo.MongoClient(get_url(config))
    db = client[config.DATABASE]
    prices_col = db["prices"]
    prices_col.insert(get_prices_record())


def delete_prices():
    config = configure_app()
    client = pymongo.MongoClient(get_url(config))
    db = client[config.DATABASE]
    prices_col = db["prices"]
    prices_col.delete_many({})


def insert_prices_2020706_record():
    config = configure_app()
    client = pymongo.MongoClient(get_url(config))
    db = client[config.DATABASE]
    prices_col = db["prices"]
    prices_col.insert(get_prices_2020706_record())


def insert_exchange_record():
    config = configure_app()
    client = pymongo.MongoClient(get_url(config))
    db = client[config.DATABASE]
    exchange_rates_col = db["exchange_rates"]
    exchange_rates_col.insert(get_exchange_rates_record())


# refactor file use this only
def insert_prices_record_with_method(method_to_get):
    config = configure_app()
    client = pymongo.MongoClient(get_url(config))
    db = client[config.DATABASE]
    prices_col = db["prices"]
    prices_col.insert(method_to_get())


@pytest.fixture(scope='module')
def mock_log():
    with mock.patch("Logger.logger.log_error"
                    ) as _mock:
        _mock.return_value = True
        yield _mock
