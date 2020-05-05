"""
    2、实现Python将mp3语音转化为文字
        思路：
            细节操作：https://blog.csdn.net/kaikai136412162/article/details/90813588
            技术文档：https://cloud.baidu.com/doc/SPEECH/s/tk4o0bm3v
            Python3安装pyAudio：https://blog.csdn.net/a506681571/article/details/85201279
"""
# 支持的格式：pcm/wav/amr
# 目前系统支持的语音时长上限为60s，请不要超过这个长度，否则会返回错误。
from aip import AipSpeech

APP_ID = "19731628"
API_KEY = "FYUiMyT6gMe6bHYOCI9W0V8O"
SECRET_KEY = "nZnFUAiFFOlGVVSabC9ju39DZI2AjqDl"
client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return (fp.read())

# 识别本地文件
text = client.asr(get_file_content('text.pcm'), 'pcm', 16000, {
    'dev_pid': 1537
})
print(text)