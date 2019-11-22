import requests
from lxml import etree


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/78.0.3904.87 Safari/537.36'}


def parser(url):
    try:
        raw_url = requests.get(url, headers=headers)
        if raw_url.status_code != 200:
            print('解析出错{},正在重试'.format(raw_url.status_code))
            parser(url)
        return etree.HTML(raw_url.content)
    except requests.exceptions.ConnectionError as e:
        print('Error', e.args)


def get_url(page):
    start_url = f'https://www.xicidaili.com/nn/{page}'
    lists = parser(start_url)
    if lists is not None:
        list_ip = lists.xpath('//table[@id="ip_list"]/tr')
        for real_list in list_ip:
            real_ip = real_list.xpath('./td[2]/text()')
            real_port = real_list.xpath('./td[3]/text()')
            real_http = real_list.xpath('./td[6]/text()')
            pool = ''.join(real_http) + r'://' + ''.join(real_ip) + ':' + ''.join(real_port)
            if pool != '://:':
                if ''.join(real_http) == 'HTTP':
                    save_in_http(pool)
                if ''.join(real_http) == 'HTTPS':
                    save_in_https(pool)


def save_in_http(pool):
    with open('pools_http.txt', 'a') as f:
        f.write(pool + '\n')


def save_in_https(pool):
    with open('pools_https.txt', 'a') as f:
        f.write(pool + '\n')


if __name__ == '__main__':
    for i in range(1, 6):
        get_url(i)
