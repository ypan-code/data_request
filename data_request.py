# %% [markdown]
# # 一些基于万得接口的基础设施建设
# - 阅读万得接口安装说明并尝试导入万得包
# - 个股时序数据请求
# - 截面股池数据请求

# %%
from WindPy import *
import pandas as pd

# %% [markdown]
# ## 个股时序数据

# %%
def stock_time_sequence(stock, fields, start, end, interval = 'day', PriceAdj = 'QFQ'):
    """
    obtain time sequence data of a SINGLE stock! 

    @param
    ------
        stock: str
            a single stock, not a list
        fields: str or iterable object of str
            fields of interest, for details, check wind api documentation
        start: str
            starting time, e.g., '2020-01-01' or '2020-01-01 9:30:00'
        end: str
            ending time
        interval: str
            either 'day' or 'min'
        PriceAdj: str
            method to adjust price, default 'QFQ'
        
    @return
        df: pd.DataFrame
            the index is time, columns are elements in the parameter "fields"
    """
    try:
        w.start()
    except:
        return "Connection Error! Make sure you log in your Wind account with account name and password instead of qrcode."
    if interval == 'day':
        df = w.wsd(stock, fields, start, end, "PriceAdj=F", usedf = True)[1]
    elif interval == 'min':
        df = w.wsi(stock, fields, start, end, "PriceAdj=F", usedf = True)[1]
    return df

# %% [markdown]
# 以下为示例

# %%
df = stock_time_sequence('000063.SZ', ["open", "close", "low", "high", "volume"], '2021-01-01', '2023-04-07')
df.head()

# %%
def cross_section(stocklist, fields, date):
    try:
        w.start()
    except:
        return "Connection Error! Make sure you log in your Wind account with account name and password instead of qrcode."
    data = pd.DataFrame(None)
    for stock in stocklist: 
        df = w.wsd(stock, fields, date, date, "PriceAdj=F", usedf = True)[1]
        data = pd.concat([data, df])
    return data

# %%
df = cross_section(['000001.SZ', '000002.SZ'], ['open', 'close'], '2020-01-07')
print(df)
df.index


