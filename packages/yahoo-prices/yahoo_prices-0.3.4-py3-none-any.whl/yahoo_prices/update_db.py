import time
import pandas as pd
from tqdm import tqdm
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from yahoo_prices.Prices_table import Prices, create_table
from yahoo_prices.utils import get_ticker, download_market
import logging

log_format = '%(levelname)s: %(module)s:%(lineno)d - %(message)s'
logging.basicConfig(level=logging.info, format=log_format)



def prepare_data(df: pd.DataFrame, engine):

    db_data = pd.read_sql_query("Select * from Prices", engine)
    db_data['Date'] = pd.to_datetime(db_data['Date'])
    db_data = db_data.drop('id', axis=1)
    df['Date'] = pd.to_datetime(df['Date'])
    if len(db_data) > 0:
        db_data = db_data.set_index(['Ticker', 'Date'])
        df = df.set_index(['Ticker', 'Date'])
        df_in = df.loc[~df.index.isin(db_data.index)]
        df_in = df_in.reset_index()
        
    else:

        df_in = df.drop_duplicates(subset=['Ticker', 'Date'], keep='first').copy()

    return df_in

def update_db(df_in: pd.DataFrame, session):
	"""
	Insert Yahoo dataframe into SQLAlchemy DB
	df: pandas dataframe
	Ticker    Date       High    Low       Open  Close      Volume   AdjClose
0   AAME  2020-01-02  29.299999  28.65  28.980000  29.09   6451100.0  28.982893
1   AAME  2020-01-03  28.290001  27.34  28.270000  27.65  14008900.0  27.548195
2   AAME  2020-01-06  27.490000  27.08  27.190001  27.32   6105800.0  27.219410
	"""
	
	if len(df_in) > 0:
		for value in tqdm(df_in.values):
			session.add(Prices(Ticker=value[0], Date=value[1], High=value[2], Low=value[3], 
						 Open=value[4], Close=value[5], Volume=value[6], AdjClose=value[7]))
			
		logging.info("Committing Changes..")
		try:
			session.commit()
		except exc.IntegrityError as e:
		    session.rollback()
		    logging.info(e)
		    session.close()
	else:
		logging.info("Nothing to commit")
	session.close()


def main(market, start_date, end_date):
	engine = create_table()
	Session = sessionmaker(bind=engine)
	session = Session()
	
	logging.info(f"Downloading Market: {market}")
	data = download_market(market, start_date, end_date)
	data = data.reset_index()
	data = data.rename(columns={'level_0': 'Ticker', 'Adj Close': 'AdjClose'})
	data = data[['Ticker', 'Date', 'High', 'Low', 'Open', 'Close', 'Volume', 'AdjClose']]
	logging.info("Preparing Data")
	df_in = prepare_data(data, engine)
	logging.info("Updating Database")

	update_db(df_in, session)


if __name__ == '__main__':
	start = time.perf_counter()
	main()	
	logging.info('====Done=====')
	end = time.perf_counter()
	logging.info(end-start)