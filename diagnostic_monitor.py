from datetime import datetime, timedelta

import pandas as pd


class PersonalBanker(object):
    '''
    Usage:
    PersonalBanker.read('f.xls').for_().pbt()
    '''
    def __init__(self, df):
        self.df = df

    @staticmethod
    def read(filename):
        df = pd.read_excel(filename)
        return PersonalBanker(df)

    def for_period(self, start_dt, end_dt):
        return self.df[(self.df['timestamp'] > start_dt) & (self.df['timestamp'] < end_dt)]
    
    def pbt(self):
        raise NotImplementedError()


class Transactions(object):
    '''
    Usage:
    Transactions.read('f.xls').for_poller_to_poller('8-24-22').coin_in()
    Transactions.read('f.xls').for_drop_to_drop().coin_in()
    Transactions.read('f.xls').for_drop_to_poller('8-24-22').coin_in()
    Transactions.read('f.xls').for_poller_to_drop('8-24-22').coin_in()
    Transactions.read('f.xls').for_period(dt1, dt2).coin_in()
    '''
    def __init__(self, df):
        self.df = df

    @staticmethod
    def read(filename):
        df = pd.read_excel(filename)
        return Transactions(df)

    def drops(self):
        return self.df[self.df['trx_id'] == 81]\
                   .sort_values(by='sentinel_dt', ascending=True)

    def for_period(self, start_dt, end_dt):
        return self.df[(self.df['sentinel_dt'] > start_dt) & (self.df['sentinel_dt'] < end_dt)]

    def for_poll_to_poll(self, gaming_day=None):
        # 6am on gaming day to 6am the day after
        if not gaming_day:
            gaming_day = datetime.strftime(datetime.now(), '%m-%d-%y') - timedelta(days=1)
        start_dt = datetime.strptime(gaming_day, '%m-%d-%y') + timedelta(hours=6)
        end_dt = start_dt + timedelta(days=1)
        return Transactions(self.for_period(start_dt, end_dt))

    def for_poll_to_drop(self, gaming_day=None):
        # 6am on gaming day open to time it was last dropped
        raise NotImplementedError()

    def for_drop_to_poll(self, gaming_day=None):
        # last time it was dropped to the 6am gaming day close
        raise NotImplementedError()
    
    def for_drop_to_drop(self, date=None):
        # last time it was dropped to next time it was dropped, prior to date if specified
        start_dt, end_dt = self.drops().iloc[-2:]
        return Transactions(self.for_period(start_dt, end_dt))

    def coin_in(self):
        raise NotImplementedError()
    
    def coin_out(self):
        raise NotImplementedError()

    def bill_in(self):
        raise NotImplementedError()

    def pbt(self):
        raise NotImplementedError()

    def att_pd_pay(self):
        raise NotImplementedError()

    def vouchers(self):
        raise NotImplementedError()
