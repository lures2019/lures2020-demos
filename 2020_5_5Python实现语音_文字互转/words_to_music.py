"""
    1、实现Python读取文字并下载mp3音乐
        思路：
            1）利用百度语音合成：http://ai.baidu.com/tech/speech/tts
            2)查看百度语音的技术文档：https://ai.baidu.com/ai-doc/SPEECH/zk4nlz99s
"""
from aip import AipSpeech

APP_ID = "19731628"
API_KEY = "FYUiMyT6gMe6bHYOCI9W0V8O"
SECRET_KEY = "nZnFUAiFFOlGVVSabC9ju39DZI2AjqDl"

client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)
with open("text.txt","r",encoding="utf-8") as fp:
    text = fp.readlines()
str = ""
for word in text:
    if len(word) != 1:
        str += word
    else:
        pass
    # 删除换行的影响
result = client.synthesis(str,'zh',1,
                          {
                                'pit':5,
                                'vol':9,
                                'per':4,
                                'spd':4
                          })
# 识别正确则返回语音二进制，错误则返回dict，参照下面错误码
if not isinstance(result,dict):
    with open("text.mp3","wb") as f:
        f.write(result)