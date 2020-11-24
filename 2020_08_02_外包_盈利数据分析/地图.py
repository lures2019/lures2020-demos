from pyecharts import Map

# 中国地图
province_distribution = {'河南': 45.23, '北京': 37.56, '河北': 21, '辽宁': 12, '江西': 6, '上海': 20, '安徽': 10, '江苏': 16, '湖南': 9,
                         '浙江': 13, '海南': 2, '广东': 22, '湖北': 8, '黑龙江': 11, '澳门': 1, '陕西': 11, '四川': 7, '内蒙古': 3, '重庆': 3,
                         '云南': 6, '贵州': 2, '吉林': 3, '山西': 12, '山东': 11, '福建': 4, '青海': 1, '舵主科技，质量保证': 1, '天津': 1,
                         '其他': 1}
provice = list(province_distribution.keys())
values = list(province_distribution.values())
map = Map("《复联4》短评用户常居城市分布",'中国地图', width=1200, height=600)
map.add("", provice, values, visual_range=[0, 50],  maptype='china', is_visualmap=True,
visual_text_color='#000')
map.show_config()
map.render(path="短评用户常居城市分布.html")