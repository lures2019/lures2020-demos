#### 前言

发现听网课的时候多个`pdf`看起来并不是很方便，加上日常生活需要使用多个`pdf`合并成一个`pdf`方便传送和阅读，于是用`python`制作一款个人小工具！



#### 打包

```
pypdf2所在路径：D:\Anaconda\Anaconda3\Lib\site-packages\PyPDF2
不使用依赖项打包：
pyinstaller -F -p D:\Anaconda\Anaconda3\Lib\site-packages -i "logo.ico" demo.py
去掉exe运行初的黑屏：
pyinstaller -F -w -p D:\Anaconda\Anaconda3\Lib\site-packages -i "logo.ico" demo.py
```

![](./images/合并pdf使用.gif)