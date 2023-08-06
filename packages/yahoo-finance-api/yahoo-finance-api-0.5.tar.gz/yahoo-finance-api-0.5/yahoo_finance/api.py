# Std lib
from datetime import datetime
import logging
import re
import time

# Third party libs
import pandas as pd
import requests
from bs4 import BeautifulSoup

#Config
# log_file = f"/logs/finage_etl_{datetime.today().strftime('%Y%m%d')}.log"
#,logging.FileHandler(log_file)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.StreamHandler()])


# ------------------------------------------------------------------------------------------------------------------------

### HELPER ###
def date_to_unixtimestamp(date):
    
    """
    Util to convert date from str to unix timestamp
    
    Args:
        date (str): Provide data in yyyy-mm-dd format

    Returns:
        [int]: Unix timestamp
    """        
    return int(datetime.strptime(date,'%Y-%m-%d').timestamp())

def get_historic_data(ticker,start_date,end_date):

    """
    Function will source historic data for any given stock / timeframe.

    Args:
        ticker (str): Ticker of the stock we need the data for
        start_date (str): Date in yyyy-mm-dd format
        end_date (str): Date in yyyy-mm-dd format

    Returns:
        pd.DataFrame : Dataframe with historic data for given time period.
    """    

    start_date = date_to_unixtimestamp(start_date)
    end_date = date_to_unixtimestamp(end_date)

    url = f'''https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={start_date}&period2={end_date}&interval=1d&events=history&includeAdjustedClose=true'''
    logging.info(url)
    try:
        logging.info("Attempting to source data from Yahoo.")
        data = pd.read_csv(url)
        logging.info(f''' Data Sourced. There are {data.shape[0]} rows and date range is {data['Date'].min()} : {data['Date'].max()} ''')
        data.set_index('Date',inplace=True)
        return data

    except Exception:
        logging.error('Error occuered',exc_info=True)

# ------------------------------------------------------------------------------------------------------------------------

def get_most_active_stocks(default=True):

    """
    Function scrapes data from Yahoo's most active stocks page.

    Args:
        default (bool, optional): By default function will return first 100 rows of Most Active UK Stocks. 
                                  If False then function will scrape all stocks from the page.
                                  Defaults to True. 

    Returns:
        pd.DataFrame : Dataframe with historic data for given time period.
    """
    if not default:
        try:
            r = requests.get('https://uk.finance.yahoo.com/most-active?count=100&offset=0')
            soup = BeautifulSoup(r.text, 'html')
            span = soup.find_all("span", {"class": "Mstart(15px) Fw(500) Fz(s)"})
            number_of_records = re.findall(' (\d*) results',span[0].text)[0]
            logging.info(f"There are total of {number_of_records} records to pull")
            
            off_sets = [x for x in range(0,int(number_of_records)) if x%100==0]

            data = pd.DataFrame()
            for off_set in off_sets:
                logging.info(f"Getting data for off_set {off_set}")
                temp = pd.read_html(f'https://uk.finance.yahoo.com/most-active?count=100&offset={off_set}')[0]
                data = data.append(temp)
                
                logging.info('Sleeping for five seconds')
                time.sleep(5)
            return data

        except Exception:
            logging.error('Error occuered',exc_info=True)
    else:
        data = pd.read_html('https://uk.finance.yahoo.com/most-active?count=100&offset=0')[0]
        return data
    

# ------------------------------------------------------------------------------------------------------------------------

def get_upcoming_earnings_data(date):
    """
    Function scrapes earnings data for given date.

    Args:
        date (str): Date in yyyy-mm-dd format

    Returns:
        pd.DataFrame : Dataframe with historic data for given time period.
    """
    url = f'https://uk.finance.yahoo.com/calendar/earnings?day={date}'

    try:
        logging.info(f'Getting earnings data for {date}')
        data = pd.read_html(url)[0]
        return data

    except ValueError as e:
        logging.info(e)
        return None

# ------------------------------------------------------------------------------------------------------------------------

def get_upcoming_stock_splits_data(date):
    """
    Function scrapes stock splits data for given date.

    Args:
        date (str): Date in yyyy-mm-dd format

    Returns:
        pd.DataFrame : Dataframe with historic data for given time period.
    """
    url = f'https://uk.finance.yahoo.com/calendar/splits?day={date}'

    try:
        logging.info(f'Getting earnings data for {date}')
        data = pd.read_html(url)[0]
        return data

    except ValueError as e:
        logging.info(e)
        return None

# ------------------------------------------------------------------------------------------------------------------------
