import time
import pandas as pd
import pandas_datareader as pdr
import concurrent.futures
import logging

log_format = '%(levelname)s: %(module)s:%(lineno)d - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)


def get_ticker(ticker, start_date, end_date):
	try:
		df = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)
		df['Ticker'] = ticker
		return df
	except Exception as e:
		logging.warning(f"{e}: {ticker}")

def download_market(market: str, start_date, end_date):

	if market == 'Nasdaq':
		start = time.perf_counter()
		tickers = pd.read_csv('ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt', 
					  error_bad_lines=False, sep='|').Symbol.tolist()

	logging.info("Found %d tickers on nasdaqtrader.com"%len(tickers))
	with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
		# Start the load operations and mark each future with its URL
		future_to_url = {executor.submit(get_ticker, ticker, start_date, end_date) for ticker in tickers}
		def gen():
			for future in concurrent.futures.as_completed(future_to_url):
				try:
				    data = future.result()
				    if isinstance(data, pd.DataFrame):
				    	yield data
				except Exception as exc:
					logging.warning(exc)

		df = pd.concat(gen())

	df = df.reset_index()
	df = df.rename(columns={'level_0': 'Ticker', 'Adj Close': 'AdjClose'})
	df = df[['Ticker', 'Date', 'High', 'Low', 'Open', 'Close', 'Volume', 'AdjClose']]

	return df