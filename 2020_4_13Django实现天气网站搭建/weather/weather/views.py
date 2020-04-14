import requests
from django.shortcuts import render
# request相当于快递员(链接，城市)



def index(request):
    # 城市(默认是北京)--->得到天气情况
    if request.method == 'POST':
        url = 'http://api.map.baidu.com/telematics/v3/weather?output=json&ak=3p49MVra6urFRGOT9s8UBWr2&location=' + request.POST['city']
    else:
        url = 'http://api.map.baidu.com/telematics/v3/weather?output=json&ak=3p49MVra6urFRGOT9s8UBWr2&location=北京'
    # 获取天气情况
    data = requests.get(url).json()
    weather = data['results'][0]
    city = weather['currentCity']
    weather_data = weather['weather_data']
    print(city,weather_data)

    # 数据整理收集
    context = {
        'city':city,
        'weather_data':weather_data
    }
    return render(request,'index.html',context)

