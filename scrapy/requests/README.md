this is a file to introduce the useage of handle

### if you have little urls, you can use by this way

```python
  from scrapy.requests.request_handle import get_content
  for url in urls:
    content = get_content(url)
    handle(content)
  
```
NOTICE: 这是堵塞式的

### if you have many urls(成百上千，反正就是有点多), 这是异步获取的，所以比较快
```python
  from scrapy.requests.handle_request import AsyncGet
  
  asyncget = AsyncGet(urls) # 注意，要是列表一类的可以直接迭代出url的
  contents = asyncget.get_content  # 这个被我设置成属性了，可以直接获取
  for content in contents:
    handle(content)
```
如果有bug的话，告诉我
