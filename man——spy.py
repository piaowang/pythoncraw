# -*- coding: UTF-8 -*-
import requests ##导入requests
from bs4 import BeautifulSoup ##导入bs4中的BeautifulSoup
import os
def next_page():
    all_a = Soup.find('li', class_='next-page').find_all('a') ##意思是先查找 class为 all 的div标签，然后查找所有的<a>标签。
    n= 0
    for i in all_a:
        href = i['href']  # 取出a标签的href 属性
        n+=1
        html_a = 'http://xpjw.club/iurenwang/2017/1207/'+ href
        html = requests.get(html_a, headers=headers)  ##上面说过了
        html_Soup = BeautifulSoup(html.text, 'lxml')  ##上面说过了

        print n

def print_picture():
    img = Soup.find('article', class_='article-content').find_all('img')  ##这三行上面都说过啦不解释了哦
    for i in img:
        img_url = i['src']

        name = img_url[-9:-4]  ##取URL 倒数第四至第九位 做图片的名字
        img = requests.get(img_url, headers=headers)
        f = open(name + '.jpg', 'ab')  ##写入多媒体文件必须要 b 这个参数！！必须要！！
        f.write(img.content)  ##多媒体文件要是用conctent哦！
        f.close()

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）

for i in range(20):
    first_url = 'http://xpjw.club/2017/1130/4268.html'
    start_html = requests.get(first_url,headers=headers)  ##使用requests中的get方法来获取all_url(就是：http://www.mzitu.com/all这个地址)的内容 headers为上面设置的请求头、请务必参考requests官方文档解释
    Soup = BeautifulSoup(start_html.text, 'lxml')  ##使用BeautifulSoup来解析我们获取到的网页（‘lxml’是指定的解析器 具体请参考官方文档哦）
    print_picture()

    if i != 0 and i !=1:
        all_url = 'http://xpjw.club/2017/1130/4268'+'_'+str(i)+".html"
        print all_url
        start_html = requests.get(all_url,  headers=headers)  ##使用requests中的get方法来获取all_url(就是：http://www.mzitu.com/all这个地址)的内容 headers为上面设置的请求头、请务必参考requests官方文档解释
        Soup = BeautifulSoup(start_html.text, 'lxml') ##使用BeautifulSoup来解析我们获取到的网页（‘lxml’是指定的解析器 具体请参考官方文档哦）
        print_picture()



