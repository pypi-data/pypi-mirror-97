from .dict2CSV import dict2CSV
from .reuters import main
from .trading_dates import update_dates
import pandas as pd 

def load_data(filename,count):
    dayscomp, daysfailed = update_dates()
    data, numcompleted, numfailed = main('https://www.reuters.com',count)
    dict2CSV(data, ['text', 'title', 'date'], '{}.csv'.format(filename))
    return numcompleted,numfailed


#This function was run once to create the starting dates file.
# Now, we only update existing file by calling get_dates() in trading_dates.py

def load_trading_days(filename):
    data,completed,failed = get_dates()
    dict2CSV.dictCSV(data,['non_trading','trading'],filename)
    return completed, failed






