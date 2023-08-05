from ejtraderDB import PDict
from ejtraderMT import Metatrader
from datetime import date, timedelta
import time
import pandas as pd
import os

start_time = time.time()
api = Metatrader(localtime=True)


active = ["EURUSD","GBPUSD"]
timeframe = "M1"


try:
    os.makedirs('data')
except OSError:
    pass


start_date = date(2020, 1, 1)
end_date = date(2021, 1, 1)
delta = timedelta(days=30)
delta2 = timedelta(days=30)
count= 0
while start_date <= end_date:
    fromDate = start_date.strftime("%d/%m/%Y")
    toDate = start_date
    toDate +=  delta2
    toDate = toDate.strftime("%d/%m/%Y")
    for symbol in active:
        count += 1 
        df = api.history([symbol],timeframe,fromDate,toDate)
        df.isnull().sum().sum() # there are no nans
        df.fillna(method="ffill", inplace=True)
        df = df.loc[~df.index.duplicated(keep = 'first')]
        df = df.dropna()
        df = df.fillna(method="ffill")
        df = df.dropna()
        if count <=1:
            df.to_csv (f'data/{symbol}.csv',  mode='a', header=True)
        else:
            df.to_csv (f'data/{symbol}.csv',  mode='a', header=False)

        print(f'writing to database... from: {fromDate} to {toDate} symbol: {symbol}')
        start_date += delta
        print('Sleeping 3 sec...')
        time.sleep(3)

         

for symbol in active:
    q = PDict(f"{symbol}",auto_commit=True)
    df = pd.read_csv(f'data/{symbol}.csv')
    q[f"{symbol}"] = df
    # Get directory name
    MODELFILE = f'data/{symbol}.csv'
    try:
        os.remove(MODELFILE)
    except OSError:
        pass

print(("--- %s seconds ---" % (time.time() - start_time)))    



        











