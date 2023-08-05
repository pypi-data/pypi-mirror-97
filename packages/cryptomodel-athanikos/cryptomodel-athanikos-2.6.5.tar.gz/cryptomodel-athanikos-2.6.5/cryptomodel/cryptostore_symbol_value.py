from calculator.CurrencyConverter import CurrencyConverter
from cryptomodel.order_types import ORDER_TYPES
from cryptomodel.transaction_types import TRANSACTION_TYPES

"""
A structure that holds all transactions per symbol 
computes the total value based on exchange and symbol rates 
contains a dict of user_grouped_symbol_value
user_grouped_symbol_value contains a list of user_symbol_value
also holds the passed in transactions that may be marked as invalid (symbol does not exist)
"""


class total_symbol_value(object):

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['exchange_rates']
        del state['symbol_prices']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __init__(self, user_id, date_time_calculated, preferred_currency, symbol_prices, exchange_rates,
                 upper_bound_symbol_rates_date, upper_bound_transaction_date):
        self.symbol_prices = symbol_prices
        self.exchange_rates = exchange_rates
        self.user_id = user_id
        self.converted_currency = preferred_currency
        self.converted_value = 0
        self.date_time_calculated = date_time_calculated
        self.upper_bound_symbol_rates_date = upper_bound_symbol_rates_date
        self.upper_bound_transaction_date = upper_bound_transaction_date
        self.user_grouped_symbol_values = {}
        self.transactions = []
        self.transaction_value = 0
        self.roi = 0

    def create(self, transactions):
        for trans in transactions:
            self.compute_transaction_value(trans)
        return self

    def compute_transaction_value(self, transaction):
        self.transactions.append(transaction)
        if not transaction.validate_symbol(self.symbol_prices):
            return

        if transaction.type == TRANSACTION_TYPES.TRADE.name:
            computed_usv = user_symbol_value(user_id=self.user_id, transaction=transaction,
                                             present_price=self.symbol_prices[transaction.symbol].price,
                                             currency=self.converted_currency, exchange_rates=self.exchange_rates,
                                             date_time_calculated=self.date_time_calculated,
                                             converted_currency=self.converted_currency)
            ugsv = self.contains_symbol(transaction)
            ugsv = self.create_user_group_symbol_value_or_increment(computed_usv, transaction, ugsv)

            self.converted_value += computed_usv.converted_value if transaction.order_type == ORDER_TYPES.BUY.name else -computed_usv.converted_value
            self.transaction_value += transaction.value if transaction.order_type == ORDER_TYPES.BUY.name else -transaction.value

            self.roi = (self.converted_value - self.transaction_value) / self.transaction_value
            ugsv.user_symbol_values.append(computed_usv)

    def create_user_group_symbol_value_or_increment(self, computed_usv, transaction, ugsv):

        if ugsv is not None:
            ugsv.volume += computed_usv.user_transaction.volume if transaction.order_type == ORDER_TYPES.BUY.name else -computed_usv.user_transaction.volume
            ugsv.converted_value += computed_usv.value if transaction.order_type == ORDER_TYPES.BUY.name else - computed_usv.value
            ugsv.converted_currency = self.converted_currency
            ugsv.value_bought += transaction.value if transaction.order_type == ORDER_TYPES.BUY.name else -transaction.value
            ugsv.roi = (ugsv.converted_value - ugsv.value_bought) / ugsv.value_bought

        else:
            ugsv = user_grouped_symbol_value(user_id=self.user_id,
                                             volume=transaction.volume,
                                             price=self.symbol_prices[transaction.symbol].price,
                                             currency=self.converted_currency,
                                             date_time_calculated=self.date_time_calculated,
                                             symbol=transaction.symbol,
                                             converted_value = computed_usv.value  if transaction.order_type == ORDER_TYPES.BUY.name else - computed_usv.value,
                                             value_bought=transaction.value if transaction.order_type == ORDER_TYPES.BUY.name else -transaction.value
                                             )
        self.user_grouped_symbol_values[transaction.symbol] = ugsv
        return ugsv

    def contains_symbol(self, transaction):
        if self.user_grouped_symbol_values is None:
            return None

        if not transaction.symbol in self.user_grouped_symbol_values.keys():
            return None

        return self.user_grouped_symbol_values[transaction.symbol]


class user_grouped_symbol_value:
    def __init__(self, user_id, symbol, volume, price, currency, date_time_calculated, value_bought, converted_value):
        self.symbol = symbol
        self.volume = volume
        self.date_time_calculated = date_time_calculated
        self.user_id = user_id
        self.currency = currency
        self.price = price
        self.converted_currency = ""
        self.converted_value = converted_value
        self.user_symbol_values = []
        self.value_bought = value_bought
        self.roi = (self.converted_value - self.value_bought) / self.value_bought


class user_symbol_value:
    def __init__(self, user_id, transaction, present_price,
                 currency, date_time_calculated, converted_currency, exchange_rates):
        self.user_transaction = transaction
        self.present_price = present_price
        self.currency = currency
        self.date_time_calculated = date_time_calculated
        self.value = self.present_price * self.user_transaction.volume
        self.user_id = user_id
        self.converted_currency = converted_currency
        self.exchange_rates = exchange_rates
        cc = CurrencyConverter(exchange_rates)
        self.converted_value = cc.convert_value(self.value, self.currency, self.converted_currency)
        self.roi = (self.value - self.user_transaction.value) / self.user_transaction.value
