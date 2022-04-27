#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from dateutil.relativedelta import relativedelta


# In[3]:


#getting crypto tickers from Yahoo. Let's do some webscrapping 
tickers = ['BTC', 'ETH', 'BNB', 'XRP', 'DOT', 'DOGE', 'SHIB', 'LTC', 'UNI', 'LINK', 'MATIC', 'BCH', 'TRX', 'MANA', 'ATOM', 'ETC', 'XTZ', 'XMR', 'GRT', 'EOS', 'SAND', 'AAVE', 'LRC', 'NEO', 'ZEC']
#apparently for some reason Yahoofinance has no ticker as BTC, it only has BTC-USD, so let's add USD to all of the tickers above
good_tickers_list=[]
for x in tickers:
    good_tickers = x+str('-USD')
    good_tickers_list.append(good_tickers)
#now let's create our dataframe
#concatenated_dataframes = pd.concat([dataframe1, dataframe2], axis=1)

#I will create an array to fill it in with the data of Crypto Close Prices
list_of_close=[]

#Here I just put all the arrays of prices I have in one beautiful dataframe
for x in range(len(good_tickers_list)):
    list_of_close.append(yf.Ticker(good_tickers_list[x]).history(period='2y')['Close'])
df=pd.DataFrame(list_of_close, index=tickers).transpose()


#Here I will calculate monthly return base on daily return

#Later on I will resample for weeks and days 
new_df=df.pct_change().resample('M').agg(lambda x:(x+1).prod()-1)
new_df


# In[4]:


#Let's Calculate Returns for the last 11 month

past_11 = (new_df+1).rolling(11).apply(np.prod)-1


# In[5]:


past_11


# In[8]:


#Let's define portfolio formation date
formation = dt.datetime(2021,5,31)
end_measurement = formation - relativedelta(months=1)

ret_12 = past_11.loc[end_measurement]


# In[9]:


ret_12=ret_12.reset_index()
ret_12


# In[10]:


#now let's set quantiles 
ret_12['Qnt']=pd.qcut(ret_12.iloc[:,1],5, labels=False)

winners = ret_12[ret_12.Qnt==4]
losers = ret_12[ret_12.Qnt==0]


# In[12]:


#rename index column to symbols to get only the Tickers
winners.rename(columns={"index": "Symbol"}, inplace=True)
losers.rename(columns={"index": "Symbol"}, inplace=True)


# In[13]:


winnerret = new_df.loc[formation+relativedelta(months=1),df.columns.isin(winners['Symbol'])]
loserret = new_df.loc[formation+relativedelta(months=1),df.columns.isin(losers['Symbol'])]


# In[14]:


momentumprofit = winnerret.mean()-loserret.mean()
momentumprofit


# In[ ]:




