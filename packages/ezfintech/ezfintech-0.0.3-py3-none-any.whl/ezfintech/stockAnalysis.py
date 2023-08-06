__FileName__    =  'stockAnalysis.py'
__CreatedDate__ = '2021/03/08 16:20:12'
__Author__      =  'Yizhe Zhang'
__WebSite__     = 'http://ervinzhang.pythonanywhere.com/'

import pandas as pd
import mplfinance as mpl
from datetime import datetime

def plotKLine(data,movingAvg=(3,6,9),plotType="candle",startDate="",endDate=""):
    """
        data: pd.DataFrame with Date(index), Open/High/Low/Close/Volume(Columns)
        movingAvg: (period1,period2,period3...) or period1   # 移动平均时间
        plotType: "candle" / "line" / "renko" / "pnf"
        startDate: "YYYY-MM-DD"
        endDate: "YYYY-MM-DD"
    """
    try:
        if startDate=="":
            startDate = data.index.min()
        if endDate=="":
            endDate = data.index.max()
        if type(startDate) != pd._libs.tslibs.timestamps.Timestamp:
            startDate = datetime.strptime(startDate,'%Y-%m-%d')
        if type(endDate) != pd._libs.tslibs.timestamps.Timestamp:
            endDate = datetime.strptime(endDate,'%Y-%m-%d')
        
        data2 = data[["Open","High","Low","Close","Volume"]][startDate:endDate]
        mpf.plot(data2,type=plotType,mav=movingAvg,volume=True,show_nontrading=True)
    except KeyError:
        print("KeyError: 请检查数据是否包含Date索引+OHLCV五列")
    except ValueError:
        print("ValueError: 请检查开始、结束日期格式是否为YYYY-MM-DD")
    except TypeError:
        print('TypeError: 请检查图表类型是否为"candle" / "line" / "renko" / "pnf"')
        print('TypeError: 请检查移动平均是否为(period1,period2,period3...)或period1')
    except Exception:
        print("Something wrong with stock data")