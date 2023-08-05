# Suluoya

### This is a package written by Suluoya not just for fun!

## pip error

```python
pip3 install --ignore-installed olefile

pip3 install --ignore-installed llvmlite

pip3 install --ignore-installed filelock
```

------

## Upgrade Suluoya

```python
import Suluoya as sly
sly.upgrade()
```

## Welcome

```python
import Suluoya as sly
sly.welcome()
```

### (1)If you wanna get text from your clipboard...

```python
import Suluoya as sly
sly.get_clipboard(show=True)
a = sly.get_clipboard()
print(a)
```

### (2)If you wanna get content from a file...

Currently support 'doc','docx','ppt','pptx','txt'

```python
import Suluoya as sly
content = sly.get_content(file=r'c:\lalala\1.docx')
print(content)
```

### (3) make a QRcode

fill in an url or some strings in content

fill in the name of the png in name

```python
import Suluoya as sly
sly.QRcode(content='', name='')
```

## 2. Import

If you wanna auto import some packages...

use"import Suluoya.Import as SI" instead of "import pandas as pd,import numpy as np"...

```python
#pass
import pandas as pd
import numpy as np
...
df = pd.Dataframe()
#now
import Suluoya.Import as SI
df = pd.Dataframe() # directly
SI.check() # just to check your import by using SI,can be omitted
# ps. go and see a file named "auto_imports.py"!
```

## 3. Crawl

```python
from Suluoya.crawl import SlyCrawl as sc
sc=sc(url='',headers={},params={},cookies={},timeout=5)
print(sc.url)
print(sc.response)
print(sc.html)
print(sc.headers)
print(sc.params)
print(sc.cookies)
'''generate a fake useragent'''
print(sc.useragent)
'''parsel.css'''
print(sc.selector)
'''BeautifulSoup'''
print(sc.soup)
'''it will return a **dic** which contain title,text,description,keywords,tags,image,infomation and the raw_html'''
print(sc.text)
'''it will return a dictionary which contain text,title,html,author,image,movies,keywords and summary.'''
print(sc.news)
'''url links'''
print(sc.links)
'''pandas.read_html'''
print(sc.tables)
```

### get proxies

```python
from Suluoya.crawl import GetProxy as gp
proxies=gp(number=1)
print(proxies)
```

## 4. Download

```python
from Suluoya.crawl import SlyDownload as sd
sd=sd(url='')
```

### (1)download music

```python
sd.download_music(path='d:\\')
```

### (2)download video

```python
sd.download_video()
```

### (3)download anything you want with an URL

```python
sd.download()
```

### (4)download a big file

```python
sd.download_big_file()
```

## 5. Text

### (1)initialize

```python
from Suluoya.text import SlyText as st
st=st('Suluoya','苏洛雅')
```

### (2)translate

```python
st=st('苏洛雅')
translate=st.translate
print(translate)
```

### (3)gender guess

name should be a Chinese name!

```python
st=st('苏洛雅')
gender=st.gender
print(gender)
```

### (4)text compare

accurate=True --> accurate match mode

accurate=False --> fuzzy match mode

```python
st=st('Suluoya','suluoya')
text_compare=st.compare(accurate=True)
print(text_compare)
```

### (5)sentiment

language='C'-->Chinese

language='E'-->English

To download the necessary data,simply run "python -m textblob.download_corpora" before using it,if something goes wrong,then click https://zhuanlan.zhihu.com/p/272181552, https://www.cnblogs.com/liweikuan/p/14052001.html or https://mp.weixin.qq.com/s?__biz=MzI1NzczMDIwNw==&mid=2247483777&idx=1&sn=cd985f3f7fe0472df9560de94753d86d&chksm=ea13b271dd643b67a591485d249ca9f64aaa380db3ff16c462c0d2def5ccce114e3c938b955e&token=445308227&lang=zh_CN#rd

```python
st=st('hello','sad')
sentiment=st.sentiment(language='E')
print(sentiment)
```

### (6)draw a heart

```python
st=st('Suluoya','苏洛雅')
st.heart
```

### (7)voice synthesis

```python
st=st('Suluoya','苏洛雅')
st.voice
```



## 6. Stock

### (1)initialize

```python
from Suluoya.stock import SlyStock as sk
sk=sk(names=['隆基股份','贵州茅台'],
     start_date='2020-12-01', 
     end_date='2020-12-31',
     frequency="w", #d→day,w→week，m→month
     holiday=False, #holiday → True
     holiday_name='国庆节', #'国庆节'，'春节'...
     before=-21,after=21,
     no_risk_rate=0.45/5200)#无风险利率
print(
    sk.start_date,
    sk.end_date,
	sk.frequency,
    sk.names,
    sk.combinations,
    sk.information,
    sk.codes,
    sk.stock_pair,
    sk.data，
    sk.holiday_name
)
```

### (2)date and holiday information

```python
from Suluoya.stock import GetDate
#initialize     if end == 'None',end=time.strftime("%Y%m%d", time.localtime())
gd=GetDate(start='20000101',end=None)
print(,gd.start,gd.end,gd.date)
print(gd.holiday)
print(gd.day)
print(gd.week)
print(gd.month)
print(gd.year)
print(gd.weekofyear)
print(gd.dayofyear)
print(gd.Date)#conclude all above
```

### (3)stock data

reference: http://baostock.com/baostock/index.php/Python_API%E6%96%87%E6%A1%A3

```python
#1.股票数据
from Suluoya.stock import GetStock
gk = GetStock(names=['隆基股份','贵州茅台'], 
                  start_date='2020-12-01', 
                  end_date='2020-12-31',
                  frequency='w'     
                  )
combination=gk.comnine # return a dataframe
stockpair=gk.stock_pair
stockdata=gk.stock_data # return codes, stock pair, stock data
gk.quit() #Please don't forget it!

#2.节日股票数据
from Suluoya.stock import GetHolidayStock
ghs=GetHolidayStock(names=['隆基股份','贵州茅台'], 
                  start_date='2020-12-01', 
                  end_date='2020-12-31',
                  frequency='w',     
                  holiday='国庆节',
                   before=-21,
                   after=21)
combination=ghs.comnine # return a dataframe
HolidayDateNearby=ghs.HolidayDateNearby # return a dataframe
HolidayNearbyData=ghs.HolidayNearbyData # return codes, stock pair, stock data

#3.季频股票能力数据
from Suluoya.stock import StockAbility
sa=StockAbility(names=None,
                 start_year=2018, start_quater=1,
                 end_year=2019, end_quater=4)
print(sa.Range) # time range
print(sa.stock_pair) # codes and names
print(sa.profit) # 盈利能力
print(sa.operation) # 营运能力
print(sa.growth) # 成长能力
print(sa.balance) # 偿债能力
print(sa.cash_flow) # 现金流量
print(sa.dupont_data) # 杜邦指数
print(sa.AllAbility) # 以上所有
sa.save_ability()
sa.quit() # Please don't forget it!

#4.行业分类及成分股
from Suluoya.stock import ConstituentStock
cs=ConstituentStock()
print(cs.StockIndustry(names=['贵州茅台','五粮液'])) # 行业分类
print(cs.sz50) # 上证50成分股
print(cs.hs300) # 沪深300成分股
print(cs.zz500) # 中证500成分股
cs.quit() # Please don't forget it!
```

### (4)calculate sharp ratio

```python
#dic_sharp contains weights,risk,rate of return and sharp ratio
#eg. weights=[0.1,0.2,0.3,0.4],stock_list=['隆基股份','五粮液','贵州茅台','宁德时代']
#The stock_list should be in the names!
#no_risk_rate means “无风险收益率”
from Suluoya.stock import SlyStock as sk
dic_sharp = sk.sharp(weights=[], stock_list=[], no_risk_rate=0.45/5200)
print(dic_sharp)
sk.quit() # Please don't forget it!
```

### (5)Markowit

```python
from Suluoya.stock import SlyStock as sk
sk=sk(names=['隆基股份','贵州茅台'],
     start_date='2020-12-01', 
     end_date='2020-12-31',
     frequency="w"
     )
#if stock_list = [], stock_list = names
#accurate:True→gradient descent，False→500 random weights
markowit=sk.Markowit(stock_list=[],
                     accurate=True, 
                     number=500, 
                     no_risk_rate=0.45/5200)
print(markowit)

sk.quit() # Please don't forget it!
```

### (6)investment portfolio

```python
from Suluoya.stock import SlyStock as sk
sk=sk(names=['隆基股份','贵州茅台'],
     start_date='2020-12-01', 
     end_date='2020-12-31',
     frequency="w"
     )
# accurate=False
result = sk.portfolio(accurate=False, number=500, no_risk_rate=0.45/5200)
print(result)
# accurate=True
print(sk.save_result())

sk.quit() # Please don't forget it!
```

### (7)choose good stocks

```python
# get data from "http://fund.eastmoney.com/data/rankhandler.aspx"
from Suluoya.stock import GetGoodStock as gs
df=gs.GetGoodStock(page=5)
print(df)
```

## 7.DataFrame

### (1)initialize

```python
from Suluoya.dataframe import SlyDataFrame as sdf
import pandas as pd
df = pd.read_csv('https://sakai.unc.edu/access/content/group/3d1eb92e-7848-4f55-90c3-7c72a54e7e43/public/data/bycatch.csv')
sdf=sdf(df)
print(sdf.df)
```

### (2)report

```python
sdf.report
#This will make a html,just look for and open it!
```

### (3)gui

```python
sdf.gui
#pandasgui
```

### (4)sweetviz

```python
sdf.sweetviz
#This will also make a html,just look for and open it!
```

