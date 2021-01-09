import requests

url = 'www.baidu.com'
response = requests.get(url)
print(response.status_code)

