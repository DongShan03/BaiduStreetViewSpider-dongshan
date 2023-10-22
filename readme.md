# 百度街景爬虫

　　该项目用于根据指定的wgs84经纬度坐标获取对应位置的百度地图的街景图像。

## 环境依赖

　　该脚本在python3环境下运行，需要导入re、os、json、requests、time、glob、csv、traceback这几种库，其中除了requests库是第三方库以外，其余均是python内置模块，无需额外安装。

　　关于requests库，版本为2.26.0，安装方式为：

``` python
  pip install requests
```
## 使用方法
    Spider.py用于爬取百度街景图
    segment.py用于图像语义分割