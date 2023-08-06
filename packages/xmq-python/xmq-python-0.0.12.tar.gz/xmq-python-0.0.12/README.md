## Message Queue Client for Python

### 生成安装包
参考 https://packaging.python.org/tutorials/packaging-projects/

- 升级安装必要工具

```python
python3 -m pip install --upgrade build
python3 -m pip install --user --upgrade twine
```

- 生成安装包

```python
python3 -m build
```

- 上传安装包

```python
python3 -m twine upload --repository-url https://<私有镜像地址> dist/*
```

默认上传到 https://pypi.org

```python
python3 -m twine upload  dist/*
```

### 使用安装包

- install

```python
pip3 install xmq-python
```

- 发送消息

```python
from xmq_python.producer import Producer
producer = Producer(mq_type='AMQO', host='', port=0, access_key='', access_secret='', timeout=None, max_message_size=None, username='', password='', virtual_host='', instance_id='')
producer.start()
producer.Publish('order','demand',{"id":123, "name": "neil"})
producer.stop()

```

- 接收消息

```python

from xmq_python.consumer import Consumer
import time
def callback(message):
    print("Got message: ", message)
    return True
consumer = Consumer(mq_type='AMQO', consumer_group_name='', host='', port=0, access_key='', access_secret='', timeout=None, max_message_size='', username='', password='', virtual_host='', instance_id='')
consumer.Register("order","demand",callback)
consumer.start()
time.sleep(100)
consumer.stop()
```
