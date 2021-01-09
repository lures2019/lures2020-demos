# 下面的代码只是单纯的接口生成的
from twilio.rest import Client
import requests

# 经过分析发现接收到的短信内容都是：message下的body信息，这样我们完全可以通过爬取当天的天气，然后发送天气信息
def get_weather():
    url = 'https://free-api.heweather.net/s6/weather/forecast?location=%E7%A7%A6%E7%9A%87%E5%B2%9B&key=e5142d9cce6c405c8962e05749ab7ce6'
    response = requests.get(url)
    # 当前的天气
    html= response.json()['HeWeather6'][0]['daily_forecast'][0]
    date = html['date']             # 日期
    wind_dir = html['wind_dir']         # 风向
    wind_sc = html['wind_sc']           # 风级
    wind_spd = html['wind_spd']         # 风速

    tmp_max = html['tmp_max']           # 最高气温
    tmp_min = html['tmp_min']           # 最低气温
    cond_txt_d = html['cond_txt_d']     # 白天天气情况
    # 最后拼接这个messgage然后返回信息
    message = "嗨，小主！早上好呀！\n今天是：{}\n秦皇岛的天气：{}\n今天气温：{}℃~{}℃\n今天风向(速/级)：{}/({}km/h、{}级)\n\n新的一天从好心情开始，但也要记得努力哦！（づ￣3￣）づ╭❤～".format(date,cond_txt_d,tmp_min,tmp_max,wind_dir,wind_spd,wind_sc)
    return message


if __name__ == '__main__':
    account_sid = 'AC6a49bdf948639653df71a5440e318470'
    auth_token = '25dd72e0eb6bd97f6d97a642d78d7b2a'
    client = Client(account_sid, auth_token)
    # 上面的是调用的api接口
    text = get_weather()
    message = client.messages.create(
        from_='+12056541226',
        body=text,                 # 调用函数
        to='+8617663712231'
    )
    print(message.sid)