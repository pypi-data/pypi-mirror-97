from l0n0lnet import se, add_quit_func, is_ipv6
from ctypes import *
import logging

se.create_udp_endpoint_v4.restype = c_uint32
se.create_udp_endpoint_v4.argtypes = [c_char_p, c_uint16, c_size_t]

se.create_udp_endpoint_v6.restype = c_uint32
se.create_udp_endpoint_v6.argtypes = [c_char_p, c_uint16, c_size_t]

se.set_udp_on_read.restype = None

se.send_udp_msg_v4.restype = c_bool
se.send_udp_msg_v4.argtypes = [
    c_uint32, c_char_p, c_uint16, c_char_p, c_size_t]

se.send_udp_msg_v6.restype = c_bool
se.send_udp_msg_v6.argtypes = [
    c_uint32, c_char_p, c_uint16, c_char_p, c_size_t]

_udps = {}  # id:name映射关系
_name_udps = {}  # name : {id, 回调函数名：回调函数}


@CFUNCTYPE(None, c_uint32, c_uint16, c_char_p, c_uint16, c_char_p, c_size_t)
def _on_udp_read(curid, tiptype, tip, tport, data, size):
    """
    给c++库的回调函数，用于调用python回调(内部函数，不要调用)

    @curid:int:udpid\n
    @tiptype:int:目标的ip类型(4 ipv4| 6 ipv6)\n
    @tip:bytes:目标的ip地址\n
    @tport:int:目标的端口\n
    @data:bytes:目标发送过来的数据\n
    @size:int:目标发送过来的数据的大小\n
    """
    data = data[:size]
    name = _udps.get(curid)
    if not name:
        return
    udpdata = _name_udps.get(name)
    if not udpdata:
        return
    func = udpdata.get("on_read")
    if not func:
        return
    func(tip, tport, data, size)


def get_id_by_name(name: str):
    """
    根据udp的名称获取udp的id(很少用到)

    @name:str:udp的名称\n
    @return:int:udp的ID\n

    例如

    ```python
    @as_udp("test", b'127.0.0.1', 30003， 1024)
    def test1_on_read(tip, tport, data, size):
        print(data)
    id = get_id_by_name("test")
    ```
    """
    udpdata = _name_udps.get(name)
    if not udpdata:
        return
    return udpdata.get("id")


def create_udp(name: str, ip: bytes, port: int, buffer_size: int = 4 * 1024):
    """
    创建udp对象

    @name:str:udp对象的名称\n
    @ip:bytes:要绑定的ip地址\n
    @port:int:要绑定的端口号\n
    @buffer_size:int:udp对象读取缓冲区大小，如果读取的数据超过该大小，会引发错误\n

    例如
    ```python
    create_udp("test2", b'127.0.0.1', 30002)
    send_udp_msg("test2", b'127.0.0.1', 30003, b'123')
    ```
    """
    if is_ipv6(ip):
        id = se.create_udp_endpoint_v6(ip, port, buffer_size)
    else:
        id = se.create_udp_endpoint_v4(ip, port, buffer_size)

    _udps[id] = name
    _name_udps[name] = _name_udps.get(name) or {}
    _name_udps[name]["id"] = id
    se.set_udp_on_read(id, _on_udp_read)


def close_udp(name: str):
    """
    关闭udp对象

    @name:str:udp对象的名称

    例如
    ```python
    create_udp("test2", b'127.0.0.1', 30002)
    close_udp("test2")
    ```
    """
    udpdata = _name_udps.get(name)
    if not udpdata:
        return
    id = udpdata.get("id")
    if not id:
        return

    se.close_udp(id)

    if _udps.get(id):
        del _udps[id]

    del _name_udps[name]


def set_udp_on_read(name: str, cb):
    """
    设置udp对象的读取回调函数

    @name:str:udp对象的名称
    @cb:function:回调函数
        @@tip:bytes:目标的ip地址\n
        @@tport:int:目标的端口\n
        @@data:bytes:目标发送过来的数据\n
        @@size:int:目标发送过来的数据的大小\n

    例如：
    ```python
    def test_on_read(tip, tport, data, size):
        print(data)
    create_udp("test2", b'127.0.0.1', 30002)
    set_udp_on_read("test2", test_on_read)
    ```
    """
    _name_udps[name] = _name_udps.get(name) or {}
    _name_udps[name]["on_read"] = cb


def send_udp_msg(name: str, tip, tport, data):
    """
    发送udp数据包

    @name:str:udp对象的名称
    @tip:bytes:目标ip地址
    @tport:int:目标端口
    @data:bytes:要发送的数据
    @return:bool:发送结果

    例如：
    ```python
    create_udp("test2", b'127.0.0.1', 30002)
    send_udp_msg("test2", b'127.0.0.1', 30003, b'123')
    ```
    """
    id = get_id_by_name(name)
    if not id:
        return
    if is_ipv6(tip):
        return se.send_udp_msg_v6(id, tip, tport, data, len(data))
    return se.send_udp_msg_v4(id, tip, tport, data, len(data))


def as_udp(name: str, ip: bytes, port: int, buffer_size: int = 4 * 1024):
    """
    将一个函数作为读取回调并初始化一个udp对象

    @ip:bytes:要绑定的ip地址\n
    @port:int:要绑定的端口\n
    @buffer_size:int:接收消息缓冲区大小。当消息大于buffer_size时会出现错误\n

    例如
    ```python
    @as_udp("test", b'127.0.0.1', 30003， 1024)
    def test1_on_read(tip, tport, data, size):
        print(data)
    ```
    """
    create_udp(name, ip, port, buffer_size)

    def wraper(func):
        set_udp_on_read(name, func)
        return func

    return wraper


class base_udp:
    """
    初始化udp对象

    @ip:bytes:要绑定的ip地址\n
    @port:int:要绑定的端口\n
    @buffer_size:int:接收消息缓冲区大小。当消息大于buffer_size时会出现错误\n

    例如：
    ```python
    class testudp1(base_udp):
        def __init__(self):
            super().__init__(b'127.0.0.1', 20001)

        def on_read(self, tip: bytes, tport: int, data: bytes, size: int):
            print(tip, tport, data, size)
            self.send_to(tip, tport, b'adsfasdf')
    ```
    """
    max_id = 0

    def __init__(self, ip: bytes, port: int, buffer_size: int = 4 * 1024):
        """
        初始化udp对象

        @ip:bytes:要绑定的ip地址\n
        @port:int:要绑定的端口\n
        @buffer_size:int:接收消息缓冲区大小。当消息大于buffer_size时会出现错误\n
        """
        base_udp.max_id = base_udp.max_id + 1
        self.name = f"{self.__class__.__name__}_{base_udp.max_id}"
        create_udp(self.name, ip, port, buffer_size)
        set_udp_on_read(self.name, self.on_read)

    def on_read(self, tip: bytes, tport: int, data: bytes, size: int):
        """
        读取数据回调(不要主动调用)

        @tip:bytes:目标ip地址\n
        @tport:int:目标端口号\n
        @data:bytes:目标发送过来的数据\n
        @size:int:data的大小\n
        """
        pass

    def send_to(self, tip: bytes, tport: int, data: bytes):
        """
        向目标发送数据

        @tip:btyes:目标的ip地址\n
        @tport:int:目标的端口号\n
        @data:bytes:要发送的数据\n
        @return:bool:发送的结果\n
        """
        return send_udp_msg(self.name, tip, tport, data)

    def close(self):
        """
        关闭udp
        """
        close_udp(self.name)


def _on_quit():
    """
    用于关闭所有udp的回调函数（不可主动调用）
    """
    udp_names = []
    for name in _name_udps.keys():
        udp_names.append(name)

    for name in udp_names:
        close_udp(name)

    _name_udps.clear()
    _udps.clear()


add_quit_func(_on_quit)
