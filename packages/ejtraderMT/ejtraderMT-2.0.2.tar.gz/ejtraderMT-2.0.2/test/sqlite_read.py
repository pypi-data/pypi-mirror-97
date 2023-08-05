from ejtraderDB import PDict
import pandas as pd
import time

symbol = "GBPUSD"

q = PDict(f"{symbol}",auto_commit=True)

start_time = time.time()
try:
    data = q[f"{symbol}"]

    print(("--- %s seconds ---" % (time.time() - start_time)))   
    




    data.columns=['date','open', 'high', 'low','close','volume','spread']
    data =  data.set_index(['date'])
    print(data)

except KeyError:
    print('Sorry there is no data with this name') 