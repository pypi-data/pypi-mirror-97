from ctypes import *
from l0n0lnet.buildcpp import try_create_lib, get_lib_path

_delay_funcs = {}   # 延时函数容器 id : function
_max_delay_id = 0   # 延时函数最大ID
_close_funcs = []   # 程序退出时会顺序执行列表中所有函数


def call_after(timeout: int, fn, repeat: int = 0):
    """
    延时调用

    @timeout:int: timeout毫秒后调用fn函数\n
    @fn: function: 无参数，无返回值的函数\n
    @repeat: int: repeat毫秒后重复执行该函数\n

    例如：
    ```
    def test_timer():
        print("123")

    # 每秒打印一次 '123'
    call_after(1000, test_timer, 1000)

    ```
    """
    global _max_delay_id
    _max_delay_id = _max_delay_id + 1

    _delay_funcs[_max_delay_id] = {
        "cb": fn,
        "repeat": repeat
    }

    se.call_after(timeout, _delay_cb, _max_delay_id, repeat)


def is_ipv6(ip: bytes):
    """
    判断某个ip地址是否时ipv6地址
    """
    return ip.find(b":") != -1


def add_quit_func(func):
    """
    向退出函数列表加入函数

    程序接收到sigint 或者所有运行的 tcp, udp, 延时函数都退出后会顺序执行close_funcs列表中所有的函数。\n
    本函数可以将自定义的退出函数加入到close_funcs列表中
    """
    _close_funcs.append(func)


def run():
    """
    用来启动程序，会卡线程
    """
    se.run()


def run_nowait():
    """
    用来启动程序，不卡线程
    """
    se.run_nowait()


@CFUNCTYPE(None, c_uint64)
def _delay_cb(id):
    """
    给c++的延时回调。用于调用python函数。（不要主动调用）
    """
    data = _delay_funcs.get(id)
    if not data:
        return

    data['cb']()

    if data['repeat'] == 0:
        del _delay_funcs[id]


@CFUNCTYPE(None)
def _on_quit():
    """
    给c++的退出回调（不要主动调用该函数)
    """
    for func in _close_funcs:
        func()


def _load_cpp_lib():
    # 构建库
    try_create_lib()

    # 加载库
    se = cdll.LoadLibrary(get_lib_path())

    # 初始化库
    se.init()

    # 初始化一些函数元数据
    se.call_after.restype = c_bool
    se.quit.restype = None

    se.set_on_quit(_on_quit)

    return se


se = _load_cpp_lib()
