import requests
import re,time

import subprocess

# video_url = "https://www.iqiyi.com/v_19rsmpr66o.html"  # 千与千寻

video_url = input("请输入要下载VIP视频的播放链接：")
movie_name = input("请输入视频名称：")
print("按下 'q' 回车终止下载任务")

response = requests.get(" https://jx.618g.com/?url=" + video_url)

ret = re.search(r'url=(.*.m3u8)', response.text)

if ret:
    url = ret.group(1)
    execute_command = "ffmpeg -i "+ url+ " -vcodec copy -acodec copy {}.mp4".format(movie_name)

    print(execute_command)
    # 命令执行后的结果输出到屏幕
    subprocess.call(execute_command, shell=True)

else:
    print("解析错误，2秒后退出！")
    time.sleep(2)

