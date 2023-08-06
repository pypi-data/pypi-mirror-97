from cryptomodel.cryptostore_symbol_value import total_symbol_value


class BalanceCalculator:

    def __init__(self, transactions, symbol_rates, exchange_rates, preferred_currency, upper_bound_symbol_rates_date,
                 upper_bound_transaction_date):
        self.transactions = transactions
        self.symbol_rates = symbol_rates
        self.exchange_rates = exchange_rates
        self.preferred_currency = preferred_currency
        self.upper_bound_symbol_rates_date = upper_bound_symbol_rates_date
        self.upper_bound_transaction_date = upper_bound_transaction_date

    def compute(self, user_id, date):
        tsv = total_symbol_value(user_id=user_id, date_time_calculated=date,
                                 preferred_currency=self.preferred_currency,
                                 symbol_prices=self.symbol_rates,
                                 exchange_rates=self.exchange_rates,
                                 upper_bound_symbol_rates_date=self.upper_bound_symbol_rates_date,
                                 upper_bound_transaction_date=self.upper_bound_transaction_date)
        return tsv.create(self.transactions)

