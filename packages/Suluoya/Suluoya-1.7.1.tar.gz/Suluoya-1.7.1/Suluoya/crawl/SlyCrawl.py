import re
import pandas as pd
import requests


class SlyCrawl(object):
    def __init__(self, url='',
                 headers={},
                 params={},
                 cookies={},
                 timeout=5):

        response = requests.get(
            url, headers=headers, params=params, cookies=cookies, timeout=timeout)
        response.encoding = response.apparent_encoding
        self.response = response
        self.url = response.url
        self.headers = response.headers
        self.params = response.data
        self.cookies = response.cookies
        self.html = response.text

    @property
    def useragent(self):
        from fake_useragent import UserAgent
        return UserAgent()

    @property
    def selector(self):
        import parsel
        return parsel.Selector(self.response.text)

    @property
    def Json(self):
        import json
        return json.loads(self.response.text)

    @property
    def soup(self):
        from bs4 import BeautifulSoup
        return BeautifulSoup(self.response.text, 'html.parser')

    def get_text(self, useragent='', accurate=True):
        from goose3 import Goose
        from goose3.text import StopWordsChinese
        try:
            if accurate == True:
                g = Goose({'stopwords_class': StopWordsChinese,
                           'browser_user_agent': useragent
                           })
            else:
                g = Goose({'browser_user_agent': useragent
                           })
            article = g.extract(url=self.url)
            dic = {
                'title': article.title,  # 标题
                'text': article.cleaned_text,  # 正文
                'description': article.meta_description,  # 摘要
                'keywords': article.meta_keywords,  # 关键词
                'tags': article.tags,  # 标签
                'image': article.top_image,  # 主要图片
                'infomation': article.infos,  # 包含所有信息的 dict
                'raw_html': article.raw_html  # 原始 HTML 文本
            }
            return dic
        except Exception as e:
            print(e)

    @property
    def news(self):
        from newspaper import Article
        news = Article(self.url, language='zh')
        news.download()
        news.parse()
        dicts = {}
        dicts['text'] = news.text
        dicts['title'] = news.title
        dicts['html'] = news.html
        dicts['author'] = news.authors
        dicts['image'] = news.top_image
        dicts['movies'] = news.movies
        dicts['keywords'] = news.keywords
        dicts['summary'] = news.summary
        return dicts

    @property
    def links(self):
        links = re.findall('"((http|ftp)s?://.*?)"', self.html)
        links = [i[0] for i in links]
        return links

    @property
    def tables(self):
        df = pd.read_html(self.url)
        return df


def GetProxy(number=1):
    proxies = []
    for i in range(number):
        url = 'http://118.24.52.95/get/'
        json_data = requests.get(url=url).json()
        proxy = json_data['proxy']
        proxies.append({
            "http": "http://" + proxy,
            "https": "https://" + proxy,
        })
    return proxies


class SlyDownload(object):
    def __init__(self, url=''):
        self.url = url

    def download_big_file(self):
        a = re.findall('/(.*)/', self.url)[0]
        b = re.findall(f'{a}/(.*)', self.url)[0]
        res = requests.get(self.url, stream=True)
        from tqdm import tqdm
        with open(r'{}'.format(b), 'wb') as f:
            for chunk in tqdm(res.iter_content(chunk_size=1024)):
                if chunk:
                    f.write(chunk)

    def download(self):
        import wget
        import ssl
        ssl._creat_default_https_context = ssl._create_unverified_context
        wget.download(self.url)

    download_music(self, path='d:\\'):
    import urllib.parse as parse
    from urllib.request import urlretrieve
    import urllib.request
    import json
    w = parse.urlencode({'w': input('请输入歌名:')})
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=63229658163010696&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&%s&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0' % (
        w)
    content = requests.get(url=url)
    str_1 = content.text
    dict_1 = json.loads(str_1)
    song_list = dict_1['data']['song']['list']
    str_3 = '''https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey5559460738919986&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"1825194589","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"1825194589","songmid":["%s"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}'''
    url_list = []
    music_name = []
    for i in range(len(song_list)):
        music_name.append(song_list[i]['name'] +
                          '-'+song_list[i]['singer'][0]['name'])
        print('{}.{}-{}'.format(i+1,
                                song_list[i]['name'], song_list[i]['singer'][0]['name']))
        url_list.append(str_3 % (song_list[i]['mid']))
    id = int(input('请输入你想下载的音乐序号:'))
    content_json = requests.get(url=url_list[id-1])
    dict_2 = json.loads(content_json.text)
    url_ip = dict_2['req']['data']['freeflowsip'][1]
    purl = dict_2['req_0']['data']['midurlinfo'][0]['purl']
    downlad = url_ip+purl
    try:
        print('开始下载...')
        urlretrieve(url=downlad, filename=r'{}{}.mp3'.format(
            path, music_name[id-1]))
        print('{}{}.mp3下载完成!'.format(path, music_name[id-1]))
    except Exception as e:
        print('没有{}的版权'.format(music_name[id-1]))

    def download_video(self):
        import os
        os.system(f'you-get {self.url}')
    
