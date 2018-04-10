import requests
import random,types
import bs4,os,re
import time
from bs4 import BeautifulSoup
import threading
#header ：USER_AGENT
Header=[
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        ]

#header={ 'User-Agent':'{}'.format(Header[random.randint(0,9)])}

# class myThread(threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter

#     def run(self):
#         print("开始线程：" + self.name)
#         #print_time(self.name, self.counter, 5)
#others way
thread_Lock=threading.BoundedSemaphore(value=10)

#获取字典中的objkey对应的值，适用于字典嵌套
#dict:字典
#objkey:目标key
#default:找不到时返回的默认值
def dict_get(dict, objkey, default):
    tmp = dict
    for k,v in tmp.items():
        if k == objkey:
            return v
        else:
            if type(v) is types.DictType:
                ret = dict_get(v, objkey, default)
                if ret is not default:
                    return ret
    return default

# dget(data, 'a.b.c') # 1
def dget(dictionary, cmd, default=None):
    cmd_list = cmd.split('.')
    tmp = dict(dictionary)
    for c in cmd_list:
        try:
            val = tmp.get(c, None)
        except AttributeError:
            return default
        if val!= None:
            tmp = val
        else:
            return default
    return tmp

def get_html(url):
    try:
        r = requests.get(url,headers={ 'User-Agent':'{}'.format(Header[random.randint(0,9)])})
        r.encoding='utf-8'
    except requests.RequestException as e:
        print(e)
    return r.text
html_doc ='''


'''

name_data = []
def get_first_wanted_url(html):
    soup=BeautifulSoup(html, "lxml")
    first_data=str(soup.find_all('div',attrs={'class':"zhuti_w_list"}))
    second_suop=BeautifulSoup(first_data,'lxml')
    #应该有两种方法↑↓
    second_data=list(second_suop.find_all('strong'))
    first_urls=[]
    for i in second_data:
        first_urls.append(i.a.get('href'))
        name_data.append(i.a.string)
    return first_urls

def get_img_urls(first_urls):
    r=get_html(first_urls)
    soup=BeautifulSoup(r,'lxml')
    page_data=str(soup.find_all('ul',attrs={'class':'pagelist'}))
    page_data_soup=BeautifulSoup(page_data,'lxml')
    num=2
    if(page_data_soup.a==None):
        num=1
    img_urls=[]
    while (num>0):
        num-=1
        first_data = str(soup.find_all('div', attrs={'class': "content_nr"}))
        second_soup=BeautifulSoup(first_data,'lxml')
        #tag_img=list(second_soup.find_all('img',attrs={'class':'BDE_Image'}))
        #tag_img=tag_img.append(list(second_soup.find_all('img',attrs={'style':True})))
        tag_img=list(second_soup.find_all('img',attrs={'style':True}))
        #print(tag_img)
        for i in tag_img:
            img_urls.append(i.get('src'))
        if(num>0):
            first_urls=first_urls.replace('.html', '_2.html')
            r=get_html(first_urls)
            soup = BeautifulSoup(r, 'lxml')

    return img_urls

def download(url,name,n=0):
    r = requests.get(url)
    img =name + str(n) + '.jpg'
    try:
        with open(img, 'wb') as f:
            f.write(r.content)
    except FileNotFoundError as e:
        print(e)
    thread_Lock.release()



def down_wanted_url(urls,name):
    x=0
    for url in urls:
        x+=1
        thread_Lock.acquire()
        t=threading.Thread(target=download,args=(url,name,x))
        t.start()
        print('正在下载第{}张'.format(x))
    





def main(url,mode=0):
    if(mode==0):
        #if(os.path.exists('d:/picture')==False):
            #os.mkdir('d:/picture')
        #os.chdir('d:/picture')
        time_path=time.strftime('%Y-%m-%d', time.strptime(time.ctime()))
        try:
            os.mkdir('D:\pics\\' + time_path)
        except OSError:
            pass
        os.chdir('D:\pics\\' + time_path)
        n=0
        #html=get_html('http://moe.005.tv/moeimg/list_2_5.html')
        html = get_html(url)
        first_urls=get_first_wanted_url(html)#1
        for i,name in enumerate(name_data):
            urls=get_img_urls(first_urls[i])
            n+=1
            try:
                down_wanted_url(urls,name)
                print(n)
            except ConnectionError as e:
                print(e)
    else:
        pass

if __name__ == '__main__':
    main(url='http://moe.005.tv/moeimg/tb/list_3_1.html')