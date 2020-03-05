import requests
import os,time,parsel

def get_url(url):
    headers = {
        'Cookie': 'PHPSESSID=clh0i5li73eti7dfqt25vvi7vh; BAIDU_SSP_lcr=https://cn.bing.com/; __gads=ID=e98268942865f2b2:T=1583324066:S=ALNI_MY2QCXWX-JOEuBdbRqQRj_cQM37SQ; UM_distinctid=170a577f3c619d-036b6839d831fc-376b4502-ff000-170a577f3c8b7; CNZZDATA1260546685=2139540747-1583319607-https%253A%252F%252Fcn.bing.com%252F%7C1583319607',
        'Host': 'www.fabiaoqing.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    select = parsel.Selector(response.text)
    results = select.css('.ui.segment img')
    path = '表情包'
    if not os.path.exists(path):
        os.mkdir(path)
    for result in results:
        image_url = result.xpath('./@data-original').get()
        image_name = result.xpath('./@title').get()
        image_name = str(image_name).replace(":", '').replace('?', '')
        response = requests.get(image_url)
        suffix = image_url.split('.')[-1]
        try:
            with open(path + '/' + image_name + '.' + suffix, mode="wb") as f:
                f.write(response.content)
        except Exception as error:
            print(error)
        print(image_name + '下载完毕！')

if __name__ == '__main__':
    start_time = time.time()
    for i in range(200):
        url = 'https://www.fabiaoqing.com/biaoqing/lists/page/' + str(i) + '.html'
        get_url(url)
        print('*************************第{}页表情包抓取完毕！*************************'.format(str(i+1)),'\n')
        time.sleep(0.5)
    end_time = time.time()
    print('抓取图片总耗时：{}秒'.format(str(end_time-start_time)))
    time.sleep(2)