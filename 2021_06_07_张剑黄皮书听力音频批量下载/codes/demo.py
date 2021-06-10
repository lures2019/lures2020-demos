import requests
import parsel
import os


url = 'https://appd8hbomsz1993.pc.xiaoe-tech.com/api/xe.goods.relation.get/1.0.0?app_id=appD8HBomSz1993'
# 加上请求头
headers1 = {
    'Cookie': 'XIAOEID=1f3ad86e3e51d4bc4080f4324a75a336; channel=homepage; cookie_channel=homepage; anonymous_user_key=dV9hbm9ueW1vdXNfNjBiYzFmMTAwNTEwMl9mNWJ3dWRtVUk2; dataUpJssdkCookie={"wxver":"","net":"","sid":""}; sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%22179ded96494221-00e5f11d191025-3e604809-1049088-179ded964951bf%22%7D; sajssdk_2015_new_user_appd8hbomsz1993_pc_xiaoe-tech_com=1; sa_jssdk_2015_appd8hbomsz1993_pc_xiaoe-tech_com=%7B%22distinct_id%22%3A%22179ded96494221-00e5f11d191025-3e604809-1049088-179ded964951bf%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%7D; pc_user_key=1526e696c47a6cde6ad5d8dc776faebc; xenbyfpfUnhLsdkZbX=0; userInfo={"app_id":"appD8HBomSz1993","user_id":"u_60bc1be14e1a5_DKIdjM1Ik2","wx_avatar":"http://wechatavator-1252524126.file.myqcloud.com/appD8HBomSz1993/image/compress/u_60bc1be14e1a5_DKIdjM1Ik2.png","wx_gender":1,"birth":null,"address":null,"job":null,"company":null,"wx_account":"","universal_union_id":"oTHW5v-u_8NFlzAy-s6OAJNgvQn8","can_modify_phone":true,"phone":null,"pc_user_key":"1526e696c47a6cde6ad5d8dc776faebc","permission_visit":0,"permission_comment":0,"permission_buy":0,"pwd_isset":false,"channels":[{"type":"wechat","active":1},{"type":"qq","active":0}],"area_code":"86"}; app_id="appD8HBomSz1993"; cookie_session_id=faCVav0oY8wJwvZ0m52ajDvrO1UAyqx2',
    'Host': 'appd8hbomsz1993.pc.xiaoe-tech.com',
    'Origin': 'https://appd8hbomsz1993.pc.xiaoe-tech.com',
    'Referer': 'https://appd8hbomsz1993.pc.xiaoe-tech.com/detail/p_5bd9081956b23_onzgZyss/6'
}
data = {
    'goods_id': "p_5bd9081956b23_onzgZyss",
    'goods_type': '6',
    'page_size': '20'
}
response = requests.post(url,json=data,headers=headers1)
response.encoding = response.apparent_encoding
sources = response.json()['data']['goods_list']
path = 'audios'
# 不存在此目录则创建一个
if not os.path.exists(path):
    os.mkdir(path)
for source in sources:
    id = source['resource_id']
    title = source['title']
    url_new = 'https://appd8hbomsz1993.pc.xiaoe-tech.com/api/xe.goods.detail.get/2.0.0?app_id=appD8HBomSz1993'
    data_new = {
        'from_id': "p_5bd9081956b23_onzgZyss",
        'goods_id': id,
        'goods_type': '3',
        'type': "6"
    }
    headers_new = {
        'Host': 'appd8hbomsz1993.pc.xiaoe-tech.com',
        'Origin': 'https://appd8hbomsz1993.pc.xiaoe-tech.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Referer': 'https://appd8hbomsz1993.pc.xiaoe-tech.com/detail/{}/3?from=p_5bd9081956b23_onzgZyss&type=6'.format(id)
    }
    response_new = requests.post(url_new,json=data_new,headers=headers_new)
    response_new.encoding = response_new.apparent_encoding
    print(response_new.json())
