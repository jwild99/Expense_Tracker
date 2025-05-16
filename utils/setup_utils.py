import datetime
from const import time_const

def init() -> None:
    """ Initializes current data and makes sure there is a csv file created for the current year.
    Also gets the current budgets from info.json """

    time_const.cur_month = datetime.datetime.now().month
    time_const.cur_day = datetime.datetime.now().day
    time_const.cur_year = datetime.datetime.now().year




