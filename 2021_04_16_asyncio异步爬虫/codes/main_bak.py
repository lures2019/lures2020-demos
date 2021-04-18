import os
import requests
# 并发任务
import asyncio
import time
# 完成网络请求并发任务
import aiohttp, aiofiles

_session = None
n = 0
total = 500

async def get_session():
    global _session
    if not _session:
        _session = aiohttp.ClientSession()
    return _session

# python3.5以后被async修饰的函数都支持异步编程，会创建一个协程对象
async def get_content(link):
    # 相当于requests.get()
    link = 'https://www.baidu.com'
    session = await get_session()
    # print('s  is:', session)

    # async with aiohttp.ClientSession() as session:
    # await 创建一个协程对象
    response = await session.get(link)
    # print('return')
    # read()相当于requests.get('XXX').text()或者content()
    content = await response.content.read()
    # print('got img')

    return content


# 下载函数
async def downloader(img):
    content = await get_content(img)
    # with open(path + '/' + str(img[0]) + '.html',mode='wb') as f:
    #     f.write(content)

    async with aiofiles.open(path + '/' + str(img) + '.html',mode='wb') as f:
        await f.write(content)

    global n
    n += 1
    if n == total:
        # exit(0)
        print('already done')
    print("下载成功：{}".format(img[0]))



# 执行函数
def run():
    start = time.time()
    base_url = 'https://www.zcool.com.cn/work/content/show?p=2&objectId=6455837'
    response = requests.get(base_url)
    image_list = response.json()['data']['allImageList']
    # 创建协程对象
    loop = asyncio.get_event_loop()
    # 指定协程运行的任务
    tasks = [asyncio.ensure_future(downloader((i,image))) for i,image in enumerate(range(total))]
    loop.run_until_complete(asyncio.wait(tasks))
    end = time.time()
    print("共运行了{}秒".format(end - start))




if __name__ == "__main__":
    path = "aio_htmls"
    if not os.path.exists(path):
        # 不存在此目录则创建一个
        os.mkdir(path)
    run()
