import datetime
from data import time_const as time

from data import file_paths as paths
from . import budgets as bUtils
from . import file as fUtils

def init() -> None:
    """ Initializes current data and makes sure there is a csv file created for the current year.
    Also gets the current budgets from info.json """

    time.cur_month = datetime.datetime.now().month
    time.cur_day = datetime.datetime.now().day
    time.cur_year = datetime.datetime.now().year

    if not fUtils.exists(paths.BUDGETS):
        bUtils.init_budgets()

    bUtils.get_budgets()

    with open(f"records\\expenses{time.cur_month}-{time.cur_year}.csv", 'a') as file:
        pass









