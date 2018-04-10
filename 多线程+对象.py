#!/usr/bin/python
import requests,random,time,os,threading,winsound

from bs4 import BeautifulSoup
from urllib.request import urlretrieve

#header ：USER_AGENT
Header=[
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.17 Safari/537.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'
        ]

#多进程
class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, urls,name,n):
        threading.Thread.__init__(self)
        self.urls = urls
        self.name = name
        self.n =n
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        # 获得锁，成功获得锁定后返回True
        # 可选的timeout参数不填时将一直阻塞直到获得锁定
        # 否则超时后将返回False
        #threadLock = threading.Lock()
        #threadLock.acquire()
        #以下为运行的函数
        down_wanted_url(self.urls,self.name,self.n)
        # 释放锁
        #threadLock.release()

#下载文件 到d:\pics
#urls=下载的网址，name=下载文件名，n=多个文件时以n+1开始
def down_wanted_url(urls,name,n=0):
    for url in urls:
        # 使用request和withopen下载图片
        r = requests.get(url, headers={'User-Agent': '{}'.format(Header[random.randint(0, 9)])})
        img = name + str(n) + '.jpg'
        try:
            with open(img, 'wb') as f:
                f.write(r.content)
        except FileNotFoundError as e:
            print(e)
    #     urlretrieve(url,name +'%d.jpg'%n)
        print('正在下载第{}张'.format(n))
        n+=1


#通过beautifulsoup分析得到相应的urls
#得到下一级网址
def get_next_urls(url):
    #得到下级页面的网址
    try:
        r = requests.get(url,headers={ 'User-Agent':'{}'.format(Header[random.randint(0,9)])})
        r.encoding='utf-8'#********
        #r.encoding = 'gb2312'
    except requests.RequestException as e:
        print(e)
    #将返回的源码通过beautifulsoup解析
    soup=BeautifulSoup(r.text,'lxml')
    #items=soup.find_all('li',attrs={'href':True})#使用find_all搜索到对应的标签*************************
    items = soup.find_all('a',target="_blank")  # 使用find_all搜索到对应的标签*************************
    html_part_next=[]#图片所需的网址
    urls=[]#下级网址
    for i in items:
        #html_part_one.append( i.a['title'] ) #利用子节点得到图片名称*****************
        html_part_next.append(list(i.strings)[0])  #利用字符串得到图片名称************************
        urls.append(''+i['href'])#得到下级网址#****************
    #print(html_part_next)
    return (html_part_next,urls)      #返回图片名称和下级网址

#得到图片网址
def get_img_urls(url):
    #(img_name,urls)=get_next_urls(url)
    #得到图片的网址
    try:
        r = requests.get(url,headers={ 'User-Agent':'{}'.format(Header[random.randint(0,9)])})
        r.encoding='utf-8'#**********
    except requests.RequestException as e:
        print(e)
    #将返回的源码通过beautifulsoup解析
    soup=BeautifulSoup(r.text,'lxml')
    items=soup.find_all('img',src=True)#使用find_all搜索到对应的标签****************
    #print(items)
    urls = []  # 图片网址
    for i in items:
        urls.append(i['src'])  # 得到下级网址
    #print(urls)
    return urls  # 返回图片名称和下级网址

#主函数
def main():
    time_path = time.strftime('%Y-%m-%d', time.strptime(time.ctime()))
    time_path='D:\pics\\' + time_path+'web2'
    try:
        os.mkdir(time_path)##
    except OSError:
        pass
    os.chdir(time_path)##
    (img_name, urls) = get_next_urls('  ')#**************
    n=0
    #urls=[""]
    for url_1 in urls:
        url_2=get_img_urls(url_1)
        #print(url_2)
        #down_wanted_url(url_2,img_name[n])
        thread=myThread(url_2,img_name[n],0)
        thread.start()
        n+=1

if __name__ == '__main__':
    main()
