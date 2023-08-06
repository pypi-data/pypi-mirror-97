# pyse

### 一、介绍
将sengine导出给python

### 二、支持平台

#### 1.windows (x86 x64 amd64)
#### 2.ubuntu2004 (x64 amd64 aarch64)及以上相内核相同内核发行版本

### 三、使用方法

#### 安装
```bash
pip install l0n0lnet
```

#### 实现一个echo server (方法一)
```python
from l0n0lnet.tcp *
from l0n0lnet import *

@on_session_connected("test")
def on_connect(session_id):
    print("链接", session_id)

@on_session_read("test")
def on_read(session_id, data, size):
    print(session_id, data, size)
    # close_tcp_by_name("test")
    send_message(session_id, data)
    call_after(1000, lambda: close_tcp(session_id))

@on_session_disconnected("test")
def on_close(session_id):
    print("断开", session_id)

create_tcp_server_v4("test", '127.0.0.1', 1234)

run()
```

#### 实现一个echo server (方法二)
```python
from l0n0lnet.tcp import base_server
from l0n0lnet import run
class test_server(base_server):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    def on_session_connected(self, session_id):
        print("链接", session_id)

    def on_session_disconnected(self, session_id):
        print("断开", session_id)

    def on_session_read(self, session_id, data, size):
        self.send_msg(session_id, data)
        print(session_id, data, size)

test_server('127.0.0.1', 1234)
run()
```
#### 实现一个echo client (方法一)
```python
def on_connected( id):
    print("连接成功", id)
    self.send_msg(b'hello!')
    self.close()

def on_connect_failed( id):
    print("连接失败", id)

def on_disconnected( id):
    print("断开连接", id)

def on_read(id, data, size):
    print(id, data, size)

connect_to_v4("test", '127.0.0.1', 1234)
set_cb("test", "on_connected", on_connected)
set_cb("test", "on_connect_failed", on_connect_failed)
set_cb("test", "on_disconnected", on_disconnected)
set_cb("test", "on_read", on_read)
run()
```
#### 实现一个echo client (方法二)
```python
from l0n0lnet import run
from l0n0lnet.tcp import base_client

class testclient(base_client):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    def on_connected(self, id):
        print("连接成功", id)
        self.send_msg(b'hello!')
        self.close()

    def on_connect_failed(self, id):
        print("连接失败", id)

    def on_disconnected(self, id):
        print("断开连接", id)

    def on_read(self, id, data, size):
        print(id, data, size)

testclient('127.0.0.1', 1234)
run()
```

