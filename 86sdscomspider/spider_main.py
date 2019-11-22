import os
import re
import requests
from lxml import etree


start_url = 'http://www.86sds.com/html/artlist/756_810.html'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/78.0.3904.87 Safari/537.36'}


def parser(url):
    raw_html = requests.get(url, headers=headers)
    if raw_html.status_code != 200:
        print('解析出错')
    html = etree.HTML(raw_html.content)
    return html


def get_url(url):
    target = parser(url)
    titles = target.xpath('//li[@class="name"]/a/text()')
    urls = target.xpath('//li[@class="name"]/a/@href')
    for title, url in zip(titles, urls):
        url = 'http://www.86sds.com/' + url
        downloader(url, title)
    turn_page(url)


def turn_page(url):
    page = parser(url)
    turn_bottom = page.xpath('//div[@class="pager"]/a[3]/@href')
    last_bottom = page.xpath('//div[@class="pager"]/a[4]/@href')
    if turn_bottom != last_bottom:
        for turn in turn_bottom:
            new_url = 'http://www.86sds.com' + turn
            get_url(new_url)
    else:
        print('爬取完毕')


def downloader(url, title):
    download_page = parser(url)
    download_links = download_page.xpath('//textarea/text()')
    for download_links_re in download_links:
        re_rule = re.compile(r'(https://.*?.jpg)')
        download_link_res = re_rule.findall(download_links_re)
    try:
        print('开始下载')
        if not os.path.exists('images\\' + title):
            print('创建文件夹' + title)
            os.makedirs('images\\' + title)
        i = 0
        for download_link in download_link_res:
            i += 1
            filename = 'images\\{}\\'.format(title) + str(i) + '.jpg'
            if not os.path.exists(filename):
                print('正在下载第' + str(i) + '张图片，地址：' + download_link)
                r = requests.get(download_link, headers=headers)
                with open(filename, 'wb') as f:
                    f.write(r.content)
    except Exception as Ex:
        print('下载出错{}'.format(Ex))


if __name__ == '__main__':
    get_url(start_url)
