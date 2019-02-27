this is a file to introduce the useage of handle

### 更新啦

现在的获取与处理页面的接口如下：
```python
 # 第一步当然是把函数导入啦
 from scrapy.requests.g_handle import GUrlHandle
 # 然后实例化
 session = GUrlHandle(content_handle='')
 
 # 获取并处理单个页面，hooks接受的是处理页面源码的函数，会返回给函数页面源码
 req = session.get_content(url='', hooks='')
 
 # 获取多个页面并进行处理，urls接受一个url的列表
 # 处理页面的函数是在session开始实例化时便赋值
 session.get_contents(urls=[])
 
```
