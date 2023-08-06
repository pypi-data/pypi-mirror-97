__FileName__    =  'getData.py'
__CreatedDate__ = '2021/03/08 11:21:21'
__Author__      =  'Yizhe Zhang'
__WebSite__     = 'http://ervinzhang.pythonanywhere.com/'

import pandas as pd
import numpy as np
import requests

def getStockByDay(stockCode,day="today",source="126"):
    """
        web: 126
        stockCode: "XXXXXXX"
        day: "today" / "4d"  # 日数据 / 4日数据
    """
    if len(stockCode)<7:
        stockCode = "0"+stockCode

    url = f"http://img1.money.126.net/data/hs/time/{day}/{stockCode}.json"
    r = requests.get(url)
    rst = eval(r.text)
    rst2 = pd.DataFrame(rst["data"])
    # 小时分钟时间、价格、均价、成交量
    rst2.columns = ["time","price","AVG price","Volume"]
    rst2.set_index("time",inplace=True)
    return rst2

def getStockByYear(stockCode,year="2020",adjust="klinederc",source="126"):
    """
        web: 126
        stockCode: "XXXXXXX"
        year: ... / 2018 / 2019 / 2020 / ... # 年份
        adjust: "kline" / "klinederc"  # 不复权 / 复权
    """
    if len(stockCode)<7:
        stockCode = "0"+stockCode

    url = f"http://img1.money.126.net/data/hs/{adjust}/day/history/{year}/{stockCode}.json"
    r = requests.get(url)
    rst = eval(r.text)
    rst2 = pd.DataFrame(rst["data"])
    rst2.columns = ["time","Price1","Price2","Price3","Price4","Volume","Rate"]
    rst2.set_index("time",inplace=True)
    return rst2

def getStockByPeriod(stockCode,period="week",adjust="klinederc",source="126"):
    """
        web: 126
        stockCode: "XXXXXX"
        period: "day" / "week" / "month"  # 年份
        adjust: "kline" / "klinederc"  # 不复权 / 复权
    """
    if len(stockCode)<7:
        stockCode = "0"+stockCode

    # 周期数据
    if source=="126":
        url = f"http://img1.money.126.net/data/hs/{adjust}/{period}/times/{stockCode}.json"
        r = requests.get(url)
        rst = eval(r.text)
        rst2 = pd.DataFrame.from_dict(rst)
        rst2 = rst2[["times","closes"]]
        rst2.set_index("times",inplace=True)
        return rst2

    elif source=="stockstar":
        shanghai = ["60","900","730","700"]
        shenzhen = ["00","200","080","002","300"]
        if stockCode.startswith(shanghai[0]) or stockCode.startswith(shanghai[1]) or stockCode.startswith(shanghai[2]) or stockCode.startswith(shanghai[3]):
            market = 1  # 市场1表示沪
        elif stockCode.startswith(shenzhen[0]) or stockCode.startswith(shenzhen[1]) or stockCode.startswith(shenzhen[2]) or stockCode.startswith(shenzhen[3]):
            market = 2  # 市场2表示深
        
        if period=="day":periodNum=6
        if period=="week":periodNum=7
        if period=="month":periodNum=8

        url = f"http://cq.ssajax.cn/interact/getTradedata.ashx?pic=qlpic_{stockCode}_{market}_{periodNum}"

        r = requests.get(url)
        rst = eval(r.text[31:-1].replace("true","True"))
        rst2 = pd.DataFrame(rst["datas"])
        rst2.columns = ["time","1","2","3","4","5","6","7","8","9"]
        rst2.set_index("time",inplace=True)
        return rst2
    else:
        return "No this source"

def getStockByTwoDate(stockCode,startDate="20210301",endDate="20210308",source="sohu"):
    """
        web: sohu
        stockCode: "XXXXXX"
        startDate:"20210301"
        endDate:"20210308"
    """
    if len(stockCode)>6:
        stockCode = stockCode[1:]

    # 时间段数据
    url = f"http://q.stock.sohu.com/hisHq?code=cn_{stockCode}&start={startDate}&end={endDate}&stat=1&order=D&period=d&callback=historySearchHandler&rt=jsonp"
    r = requests.get(url)
    rst = eval(r.text[22:-3])
    rst2 = pd.DataFrame(rst["hq"])
    rst2.columns = ["time","1","2","3","4","5","6","7","8","9"]
    rst2.set_index("time",inplace=True)
    return rst2