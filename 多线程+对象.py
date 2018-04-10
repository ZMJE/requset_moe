#!/usr/bin/python
import requests,random,time,os,threading,winsound

from bs4 import BeautifulSoup
from urllib.request import urlretrieve

#header ��USER_AGENT
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

#�����
class myThread (threading.Thread):   #�̳и���threading.Thread
    def __init__(self, urls,name,n):
        threading.Thread.__init__(self)
        self.urls = urls
        self.name = name
        self.n =n
    def run(self):                   #��Ҫִ�еĴ���д��run�������� �߳��ڴ������ֱ������run����
        # ��������ɹ���������󷵻�True
        # ��ѡ��timeout��������ʱ��һֱ����ֱ���������
        # ����ʱ�󽫷���False
        #threadLock = threading.Lock()
        #threadLock.acquire()
        #����Ϊ���еĺ���
        down_wanted_url(self.urls,self.name,self.n)
        # �ͷ���
        #threadLock.release()

#�����ļ� ��d:\pics
#urls=���ص���ַ��name=�����ļ�����n=����ļ�ʱ��n+1��ʼ
def down_wanted_url(urls,name,n=0):
    for url in urls:
        # ʹ��request��withopen����ͼƬ
        r = requests.get(url, headers={'User-Agent': '{}'.format(Header[random.randint(0, 9)])})
        img = name + str(n) + '.jpg'
        try:
            with open(img, 'wb') as f:
                f.write(r.content)
        except FileNotFoundError as e:
            print(e)
    #     urlretrieve(url,name +'%d.jpg'%n)
        print('�������ص�{}��'.format(n))
        n+=1


#ͨ��beautifulsoup�����õ���Ӧ��urls
#�õ���һ����ַ
def get_next_urls(url):
    #�õ��¼�ҳ�����ַ
    try:
        r = requests.get(url,headers={ 'User-Agent':'{}'.format(Header[random.randint(0,9)])})
        r.encoding='utf-8'#********
        #r.encoding = 'gb2312'
    except requests.RequestException as e:
        print(e)
    #�����ص�Դ��ͨ��beautifulsoup����
    soup=BeautifulSoup(r.text,'lxml')
    #items=soup.find_all('li',attrs={'href':True})#ʹ��find_all��������Ӧ�ı�ǩ*************************
    items = soup.find_all('a',target="_blank")  # ʹ��find_all��������Ӧ�ı�ǩ*************************
    html_part_next=[]#ͼƬ�������ַ
    urls=[]#�¼���ַ
    for i in items:
        #html_part_one.append( i.a['title'] ) #�����ӽڵ�õ�ͼƬ����*****************
        html_part_next.append(list(i.strings)[0])  #�����ַ����õ�ͼƬ����************************
        urls.append(''+i['href'])#�õ��¼���ַ#****************
    #print(html_part_next)
    return (html_part_next,urls)      #����ͼƬ���ƺ��¼���ַ

#�õ�ͼƬ��ַ
def get_img_urls(url):
    #(img_name,urls)=get_next_urls(url)
    #�õ�ͼƬ����ַ
    try:
        r = requests.get(url,headers={ 'User-Agent':'{}'.format(Header[random.randint(0,9)])})
        r.encoding='utf-8'#**********
    except requests.RequestException as e:
        print(e)
    #�����ص�Դ��ͨ��beautifulsoup����
    soup=BeautifulSoup(r.text,'lxml')
    items=soup.find_all('img',src=True)#ʹ��find_all��������Ӧ�ı�ǩ****************
    #print(items)
    urls = []  # ͼƬ��ַ
    for i in items:
        urls.append(i['src'])  # �õ��¼���ַ
    #print(urls)
    return urls  # ����ͼƬ���ƺ��¼���ַ

#������
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
