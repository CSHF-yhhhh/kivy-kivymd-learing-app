# 基于 Kivy/Kivymd 开发的成语学习APP

本项目已成功打包,使用的打包环境请参考[nkiiiid的文章](https://github.com/nkiiiiid/kivy-apk)
buildozer.spec文件请参考/MainApp/buildozer.spec

> 成功打包的APK已上传,可自行下载

## 环境说明

> Kivy==1.11.1
> kivy-deps.glew==0.3.0
> kivy-deps.gstreamer==0.3.1
> kivy-deps.sdl2==0.3.1
> Kivy-Garden==0.1.4
> kivymd==0.104.1
> Django==3.1
> openpyxl==3.0.6

## 本地运行

* server服务端

服务端使用Diango框架,通过json来传输数据

```python
#如果需要部署在服务器上记得在服务器中开放使用的端口
python ./server/manage.py runserver ip:port #eg: python manage.py 0.0.0.0:12345
```

* MainApp/client/client.py

在这个文件夹中设置服务器的地址和端口

* 启动app

在MainApp下,通过以下命令运行

```python
python main.py
```
