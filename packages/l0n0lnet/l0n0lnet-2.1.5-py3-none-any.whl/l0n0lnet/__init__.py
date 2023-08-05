from ctypes import *

import os
import platform
import sys
import base64

cur_file_path, filename = os.path.split(os.path.abspath(__file__))

lib_temp_path = None

if platform.system() == "Windows":
    if platform.architecture()[0] == "64bit":
        from l0n0lnet.libse_windows_x64 import libse_data
    else:
        from l0n0lnet.libse_windows_x86 import libse_data
    lib_temp_path = os.environ.get("TEMP") + "\\l0n0lnet"
elif platform.system() == "Linux":
    if platform.machine() == "x86_64" or platform.machine() == "AMD64":
        from l0n0lnet.libse_linux_x64 import libse_data
    elif platform.machine() == "aarch64":
        from l0n0lnet.libse_linux_armv7 import libse_data
    else:
        sys.stderr.write(("Current platform not supported.\n"))
    lib_temp_path = "/tmp/l0n0lnet"

else:
    sys.stderr.write(("Current platform not supported.\n"))

# 创建缓存目录
lib_name = "libse_2_1_5.so"
lib_full_path = f"{lib_temp_path}/{lib_name}"
if not os.path.exists(lib_temp_path):
    os.mkdir(lib_temp_path)

# 删除不匹配的缓存
for d in os.listdir(lib_temp_path):
    if d != "." and d != ".." and d != lib_name:
        os.remove(f"{lib_temp_path}/{d}")

# 写入库内容
if not os.path.exists(lib_full_path):
    with open(lib_full_path, 'wb') as fp:
        fp.write(base64.decodebytes(libse_data))

# 加载库
se = cdll.LoadLibrary(lib_full_path)

# 初始化库
se.init()

# 初始化一些函数元数据
se.call_after.restype = c_bool
se.quit.restype = None


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


_delay_funcs = {}
_max_delay_id = 0


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


# 程序退出时会顺序执行列表中所有函数
close_funcs = []


def add_quit_func(func):
    """
    向退出函数列表加入函数

    程序接收到sigint 或者所有运行的 tcp, udp, 延时函数都退出后会顺序执行close_funcs列表中所有的函数。\n
    本函数可以将自定义的退出函数加入到close_funcs列表中
    """
    close_funcs.append(func)


@CFUNCTYPE(None)
def _on_quit():
    """
    给c++的退出回调（不要主动调用该函数)
    """
    for func in close_funcs:
        func()


se.set_on_quit(_on_quit)


def is_ipv6(ip: bytes):
    """
    判断某个ip地址是否时ipv6地址
    """
    return ip.find(b":") != -1
