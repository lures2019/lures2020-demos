### 代码说明：

```
使用requests和Django实现，其中index.html是先前已经写好的网页模板，只需要传入相应的参数就可以展现出来！
1）创建工程
django-admin startproject weather
2）将index.html剪切到weather的子目录，和manage.py在同一级
3）代码部分不详细解释了，不难，命名为views.py,和settings.py在同一目录
4）修改settings.py第57行内容，改为'DIRS': ['.'],
5）修改urls.py,将内容改为下面的形式：
	from django.contrib import admin
    from django.urls import path
    from . import views

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('index/', views.index),        # 画作的名字
    ]
6）运行：python manage.py runserver
7）网页上打开链接：https://127.0.0.1/index
```

