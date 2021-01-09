import requests

url = 'http://www.baidu.com'
response = requests.get(url)
print(response.status_code)

