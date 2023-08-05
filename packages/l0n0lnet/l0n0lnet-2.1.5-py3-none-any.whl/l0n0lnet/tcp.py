from l0n0lnet import se, add_quit_func, is_ipv6
from ctypes import *
import logging

# 初始化库
se.create_server_v4.restype = c_uint32
se.create_server_v4.argtypes = [c_char_p, c_int32, c_int32]

se.create_server_v6.restype = c_uint32
se.create_server_v6.argtypes = [c_char_p, c_int32, c_int32]

se.connect_to_v4.restype = c_uint32
se.connect_to_v4.argtypes = [c_char_p, c_int32]

se.close_tcp.restype = None
se.close_tcp.argtypes = [c_int32]

se.send_message.restype = c_bool
se.send_message.argtypes = [c_uint32, c_char_p, c_size_t]


_tcps = {}      # id:name映射关系
_name_tcp = {}  # name : {id, 回调函数名：回调函数}


def _get_callback(target_id: int, cb_name: str):
    """
    获取某个tcp的回调

    @target_id:int:目标tcp的id\n
    @cb_name:str:要获取的回调名称\n
    @return:function:回调函数\n
    """
    name = _tcps.get(target_id)
    if name is None:
        return
    name_data = _name_tcp.get(name)
    if name_data is None:
        return
    return name_data.get(cb_name)


@CFUNCTYPE(None, c_uint32, c_uint32, c_char_p, c_size_t)
def _on_session_read(session_id: int, server_id: int, data: bytes, size: int):
    """
    给c++服务器回调的sesion read回调函数(不要主动调用)

    @session:int:会话ID\n
    @server_id:int:会话对应的服务器ID\n
    @data:bytes:客户端会话传递过来的数据\n
    @size:int:数据的大小\n
    """
    func = _get_callback(server_id, "on_session_read")
    if func is None:
        return
    data = data[:size]
    func(session_id, data, size)


@CFUNCTYPE(None, c_uint32, c_uint32)
def _on_session_connected(session_id, server_id):
    """
    给c++服务器回调函数：会话连接 回调函数(不要主动调用)

    @session:int:会话ID\n
    @server_id:int:会话对应的服务器ID\n
    """
    se.regist_on_read_size(session_id, 0, _on_session_read)
    func = _get_callback(server_id, "on_session_connected")
    if func is None:
        return
    func(session_id)


@CFUNCTYPE(None, c_uint32, c_uint32)
def _on_session_disconnected(session_id, server_id):
    """
    给c++服务器回调函数：会话断开连接 回调函数(不要主动调用)

    @session:int:会话ID\n
    @server_id:int:会话对应的服务器ID\n
    """
    func = _get_callback(server_id, "on_session_disconnected")
    if func is None:
        return
    func(session_id)


@CFUNCTYPE(None, c_uint32, c_uint32)
def _on_client_connected(client_id, server_id):
    """
    给c++客户端回调函数：连接服务器成功 回调函数(不要主动调用)

    @session:int:客户端ID\n
    @server_id:int: 固定值1 暂时没用\n
    """
    func = _get_callback(client_id, "on_connected")
    if func is None:
        return
    func()


@CFUNCTYPE(None, c_uint32, c_uint32)
def _on_client_disconnected(client_id, server_id):
    """
    给c++客户端回调函数：与服务器连接断开 回调函数(不要主动调用)

    函数并不一定会执行。比如当前tcp对象是最后一个被关闭的对象。被关闭后主循环也关闭了，所以就不执行了。\n
    如果想要在程序退出时执行某函数请调用add_quit_func将需要执行的函数加入到退出列表

    @session:int:客户端ID\n
    @server_id:int: 固定值1 暂时没用\n
    """
    func = _get_callback(client_id, "on_disconnected")
    if func is None:
        return
    func()


@CFUNCTYPE(None, c_uint32, c_uint32)
def _on_client_connect_failed(client_id, server_id):
    """
    给c++客户端回调函数：连接服务器失败 回调函数(不要主动调用)

    @session:int:客户端ID\n
    @server_id:int: 固定值1 暂时没用\n
    """
    func = _get_callback(client_id, "on_connect_failed")
    if func is None:
        return
    func()


@CFUNCTYPE(None, c_uint32, c_uint32, c_char_p, c_size_t)
def _on_client_read(client_id, server_id, data, size):
    """
    给c++客户端回调函数：获取到服务器发来的数据 回调函数(不要主动调用)

    @session:int:客户端ID\n
    @server_id:int: 固定值1 暂时没用\n
    """
    func = _get_callback(client_id, "on_read")
    if func is None:
        return
    data = data[:size]
    func(data, size)


def send_message(id: int, data: bytes) -> bool:
    """
    向目标ID发送数据

    @id:int:目标ID\n
    @data:bytes:数据\n

    例如
    ```python
    from l0n0lnet.tcp import *
    from l0n0lnet import *

    def on_session_connected(session_id):
        print(session_id)

    def on_session_disconnected(session_id):
        print(session_id)

    def on_session_read(session_id, data, size):
        print(data)
        # 在这里^v^
        send_message(session_id, data)
        close_tcp(session_id)

    id = create_tcp_server("test", b"127.0.0.1", 1234, 1024)

    set_cb("test", "on_session_connected", on_session_connected)
    set_cb("test", "on_session_disconnected", on_session_disconnected)
    set_cb("test", "on_session_read", on_session_read)

    run()
    ```
    """
    return se.send_message(id, data, len(data))


def close_tcp(id: int):
    """
    用来关闭tcp。如服务器，客户端，session。

    @id:int:tcp对象的ID\n

    例如
    ```python
    from l0n0lnet.tcp import *
    from l0n0lnet import *

    def on_session_connected(session_id):
        print(session_id)

    def on_session_disconnected(session_id):
        print(session_id)

    def on_session_read(session_id, data, size):
        print(data)
        send_message(session_id, data)
        # 在这里^v^
        close_tcp(session_id)

    id = create_tcp_server("test", b"127.0.0.1", 1234, 1024)

    set_cb("test", "on_session_connected", on_session_connected)
    set_cb("test", "on_session_disconnected", on_session_disconnected)
    set_cb("test", "on_session_read", on_session_read)

    run()
    ```
    """
    # 关闭tcp
    se.close_tcp(id)

    # 获取名称
    name = _tcps.get(id)
    if not name:
        return

    # 删除名称缓存
    if _name_tcp.get(name):
        del _name_tcp[name]

    # 删除数据
    del _tcps[id]


def create_tcp_server(server_name: str, ip: bytes, port: int, backlog: int = 1024):
    """
    创建tcp服务器

    @server_name:str:服务器名称\n
    @ip:str:服务器IP地址\n
    @port:int:服务器端口号\n
    @backlog:int:backlog\n
    @return:int:服务器ID号。0 表示创建失败\n

    例如
    ```python
    from l0n0lnet.tcp import *
    from l0n0lnet import *

    def on_session_connected(session_id):
        print(session_id)

    def on_session_disconnected(session_id):
        print(session_id)

    def on_session_read(session_id, data, size):
        print(data)
        send_message(session_id, data)
        close_tcp(session_id)

    id = create_tcp_server("test", b"127.0.0.1", 1234, 1024)

    set_cb("test", "on_session_connected", on_session_connected)
    set_cb("test", "on_session_disconnected", on_session_disconnected)
    set_cb("test", "on_session_read", on_session_read)

    run()
    ```
    """
    # 创建服务器
    if is_ipv6(ip):
        id = se.create_server_v4(ip, port, backlog)
    else:
        id = se.create_server_v6(ip, port, backlog)

    # 验证创建结果
    if id == 0:
        return id

    # 注册基本回调
    se.regist_on_session_connected(id, _on_session_connected)
    se.regist_on_session_disconnected(id, _on_session_disconnected)

    # 缓存数据
    if not _name_tcp.get(server_name):
        _name_tcp[server_name] = {"id": id}
    else:
        _name_tcp[server_name]['id'] = id

    _tcps[id] = server_name

    # 返回ID
    return id


def connect_to(client_name: str, ip: bytes, port: int):
    """
    创建连接到目标的客户端

    @client_name:str:客户端名称\n
    @ip:bytes:服务器ip地址\n
    @port:int:服务器端口号\n
    @return:int:客户端id\n

    例如
    ```python
    from l0n0lnet.tcp import *
    from l0n0lnet import *

    client_id = connect_to("test", b"127.0.0.1", 1234)

    def on_connected():
        print("on_connected")
        send_message(client_id, b'Hello.')

    def on_connect_failed():
        print("on_connect_failed")

    def on_disconnected():
        print("on_disconnected")

    def on_read(data, size):
        print(data)
        close_tcp(client_id)

    set_cb("test", "on_connected", on_connected)
    set_cb("test", "on_connect_failed", on_connect_failed)
    set_cb("test", "on_disconnected", on_disconnected)
    set_cb("test", "on_read", on_read)

    run()
    ```
    """
    # 连接目标
    if is_ipv6(ip):
        id = se.connect_to_v4(ip, port)
    else:
        id = se.connect_to_v6(ip, port)

    # 验证创建结果
    if id == 0:
        return id

    # 注册基本回调
    se.regist_on_connected(id, _on_client_connected)
    se.regist_on_disconnected(id, _on_client_disconnected)
    se.regist_on_connect_failed(id, _on_client_connect_failed)
    se.regist_on_read_size(id, 0, _on_client_read)

    # 缓存数据
    if not _name_tcp.get(client_name):
        _name_tcp[client_name] = {"id": id}
    else:
        _name_tcp[client_name]['id'] = id

    _tcps[id] = client_name

    # 返回ID
    return id


def close_tcp_by_name(name: str):
    """
    通过名称关闭tcp对象

    @name:str:tcp对象的名称\n
    """
    namedata = _name_tcp.get(name)
    if not namedata:
        return
    id = namedata.get("id")
    if not id:
        return
    close_tcp(id)


def set_cb(tcp_name: str, cb_name: str, cb_fn):
    """
    设置回调

    @tcp_name:str:tcp对象的名称\n
    @cb_name:str:回调函数的名称(例如 on_session_read)\n
    @cb_fn:function:回调函数\n
    """
    if not _name_tcp.get(tcp_name):
        _name_tcp[tcp_name] = {cb_name: cb_fn}
    else:
        _name_tcp[tcp_name][cb_name] = cb_fn


def handler_session_connected(server_name: str):
    """
    用来修饰服务器on_session_read回调的装饰器

    @server_name:str:服务器的名称\n

    例如
    ```python
    from l0n0lnet.tcp import *
    from l0n0lnet import *

    @handler_session_connected("test")
    def on_session_connected(session_id):
        print(session_id)

    @handler_session_disconnected("test")
    def on_session_disconnected(session_id):
        print(session_id)

    @handler_session_read("test")
    def on_session_read(session_id, data, size):
        print(data)
        send_message(session_id, data)
        close_tcp(session_id)

    id = create_tcp_server("test", b"127.0.0.1", 1234, 1024)

    run()
    ```
    """
    def wraper(func):
        set_cb(server_name, "on_session_connected", func)
        return func
    return wraper


def handler_session_disconnected(server_name: str):
    """
    用来修饰服务器on_session_disconnected回调的装饰器

    @server_name:str:服务器的名称\n

    例如
    ```python
    from l0n0lnet.tcp import *
    from l0n0lnet import *

    @handler_session_connected("test")
    def on_session_connected(session_id):
        print(session_id)

    @handler_session_disconnected("test")
    def on_session_disconnected(session_id):
        print(session_id)

    @handler_session_read("test")
    def on_session_read(session_id, data, size):
        print(data)
        send_message(session_id, data)
        close_tcp(session_id)

    id = create_tcp_server("test", b"127.0.0.1", 1234, 1024)

    run()
    ```
    """
    def wraper(func):
        set_cb(server_name, "on_session_disconnected", func)
        return func
    return wraper


def handler_session_read(server_name: str):
    """
    用来修饰服务器on_session_read回调的装饰器

    @server_name:str:服务器的名称\n

    例如
    ```python
    from l0n0lnet.tcp import *
    from l0n0lnet import *

    @handler_session_connected("test")
    def on_session_connected(session_id):
        print(session_id)

    @handler_session_disconnected("test")
    def on_session_disconnected(session_id):
        print(session_id)

    @handler_session_read("test")
    def on_session_read(session_id, data, size):
        print(data)
        send_message(session_id, data)
        close_tcp(session_id)

    id = create_tcp_server("test", b"127.0.0.1", 1234, 1024)

    run()
    ```
    """
    def wraper(func):
        set_cb(server_name, "on_session_read", func)
        return func
    return wraper


def _on_quit():
    """
    程序退出时要执行的函数（比如收到sigint信号后, 不要主动调用）

    用于关闭所有的tcp对象
    """
    tcpids = []
    for tcp_data in _name_tcp.values():
        id = tcp_data.get("id")
        if id:
            tcpids.append(id)

    for id in tcpids:
        close_tcp(id)

    _tcps.clear()
    _name_tcp.clear()


add_quit_func(_on_quit)


class base_server:
    """
    基础tcp服务器类（用于继承)

    @ip:bytes:服务要绑定的IP地址\n
    @port:int:服务要监听的端口\n

    例如：
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


    server = test_server(b'127.0.0.1', 1234)

    run()
    ```
    """
    max_id = 0

    def __init__(self, ip: bytes, port: int):
        base_server.max_id = base_server.max_id + 1
        self.name = f"{self.__class__.__name__}_{base_server.max_id}"
        create_tcp_server(self.name, ip, port)
        set_cb(self.name, "on_session_connected", self.on_session_connected)
        set_cb(self.name, "on_session_disconnected", self.on_session_disconnected)
        set_cb(self.name, "on_session_read", self.on_session_read)

    def __del__(self):
        self.close()

    def close(self):
        close_tcp_by_name(self.name)

    def send_msg(self, id, data):
        send_message(id, data)

    def on_session_connected(self, session_id):
        pass

    def on_session_disconnected(self, session_id):
        """
        函数并不一定会执行。比如当前tcp对象是最后一个被关闭的对象。被关闭后主循环也关闭了，所以就不执行了。\n
        如果想要在程序退出时执行某函数请调用add_quit_func将需要执行的函数加入到退出列表
        """
        pass

    def on_session_read(self, session_id, data, size):
        pass


class base_client:
    """
    基础tcp客户端（用于继承）

    @ip:bytes:要链接服务器的IP地址\n
    @port:int:要链接服务器的端口\n

    例如：
    ```python
    from l0n0lnet import run
    from l0n0lnet.tcp import base_client

    class testclient(base_client):
        def __init__(self, ip, port):
            super().__init__(ip, port)

        def on_connected(self):
            print("连接成功")
            self.send_msg(b'hello!')
            self.close()

        def on_connect_failed(self):
            print("连接失败")

        def on_disconnected(self):
            print("断开连接")

        def on_read(self, data, size):
            print(id, data, size)


    client = testclient(b'127.0.0.1', 1234)

    run()
    ```
    """
    max_id = 0

    def __init__(self, ip, port):
        base_client.max_id = base_client.max_id + 1
        self.name = f"{self.__class__.__name__}_{base_client.max_id}"
        self.id = connect_to(self.name, ip, port)
        set_cb(self.name, "on_connected", self.on_connected)
        set_cb(self.name, "on_connect_failed", self.on_connect_failed)
        set_cb(self.name, "on_disconnected", self.on_disconnected)
        set_cb(self.name, "on_read", self.on_read)

    def __del__(self):
        self.close()

    def close(self):
        close_tcp_by_name(self.name)

    def send_msg(self, data):
        send_message(self.id, data)

    def on_connected(self):
        pass

    def on_connect_failed(self):
        pass

    def on_disconnected(self):
        """
        函数并不一定会执行。比如当前tcp对象是最后一个被关闭的对象。被关闭后主循环也关闭了，所以就不执行了。\n
        如果想要在程序退出时执行某函数请调用add_quit_func将需要执行的函数加入到退出列表
        """
        pass

    def on_read(self, data, size):
        pass
