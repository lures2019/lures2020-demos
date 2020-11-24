import requests
url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn=1&rn=30&httpsStatus=1&reqId=bd2b24f0-acb9-11ea-8d86-192dfd7bb331".format(input("请输入你想要的歌手:"))
headers={
       "Cookie":"__guid=112476674.2155037822307764500.1591598972738.781; _ga=GA1.2.1179338892.1591598974; _gid=GA1.2.878961713.1591951076; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1591598974,1591604364,1591951076; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1591951631; kw_token=6704SO8UJNS; monitor_count=8",
       "Host": "www.kuwo.cn",
       "Referer":"http://www.kuwo.cn/search/list?key=%E8%96%9B%E4%B9%8B%E8%B0%A6",
       "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}
response = requests.get(url=url,headers=headers)

print(response)