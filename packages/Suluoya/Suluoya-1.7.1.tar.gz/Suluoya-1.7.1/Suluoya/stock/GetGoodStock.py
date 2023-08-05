import pandas as pd
import requests
import parsel
import requests
import re
import json
from tqdm import tqdm
import concurrent.futures


def GetGoodStock(page=5):
    url = "http://fund.eastmoney.com/data/rankhandler.aspx"
    headers = {
        "Host": "fund.eastmoney.com",
        "Referer": "http://fund.eastmoney.com/data/fundranking.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63"
    }
    urls = []

    def get_urls(page):
        params = {
            "op": "ph",
            "sc": "6yzf",
            "sd": '2021-02-11',
            "ed": '2021-02-11',
            "pi": str(page),
            "dx": "1",
        }
        response = requests.get(url, headers=headers, params=params)
        response.encoding = response.apparent_encoding
        data = re.findall('var rankData = {datas:(.*),allRe', response.text)[0]
        data = eval(data)
        list = ['http://fund.eastmoney.com/' +
                re.findall(r'(\d*),', i)[0]+'.html' for i in data]
        for i in list:
            urls.append(i)
    for i in range(1, page+1):
        get_urls(i)

    def get_stock(url):
        df = pd.read_html(url)
        return df[5][['股票名称', '持仓占比']]

    stocks = []

    def main(url):
        stocks.append(get_stock(url))

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for url in urls:
            print(url)
            executor.submit(main, url)
    stock = pd.concat(stocks)
    stock['持仓占比'] = stock['持仓占比'].map(lambda x: x.replace('%', ''))
    stock = stock.replace('暂无数据',0) 
    stock['持仓占比'] = stock['持仓占比'].astype('float')
    group = stock.groupby('股票名称')
    df1 = group.mean()
    df2 = group.count()
    df1 = df1.rename(columns={'持仓占比': '平均持仓占比'})
    df2 = df2.rename(columns={'持仓占比': '出现次数'})
    df = pd.merge(df1, df2, how='outer', on='股票名称')
    df = df.sort_values(by='出现次数', ascending=False)
    df.to_csv('goodstocks.csv', encoding='utf8')
    return df

