import os
import platform
import sys
import base64
import shutil
from git.repo import Repo

lib_name = "libse_2_2_1.so"  # c++库的名称
cur_file_path, filename = os.path.split(os.path.abspath(__file__))
cppsrc = "https://gitee.com/l00n00l/l0n0lnet.git"
branch = "cppsrc"


def get_tmp_path():
    if platform.system() == "Windows":
        return os.environ.get("TEMP") + "\\l0n0lnet"
    elif platform.system() == "Linux":
        return "/tmp/l0n0lnet"
    sys.stderr.write(("Current platform not supported.\n"))


def get_lib_path():
    lib_temp_path = get_tmp_path()
    if not lib_temp_path:
        return
    return f"{lib_temp_path}/{lib_name}"


def create_temp_dir():
    lib_temp_path = get_tmp_path()
    if not lib_temp_path:
        return
    if not os.path.exists(lib_temp_path):
        os.mkdir(lib_temp_path)
    return True


# 删除不匹配的缓存
def remove_nouse_libs():
    lib_temp_path = get_tmp_path()
    if not lib_temp_path:
        return
    for d in os.listdir(lib_temp_path):
        target_path = f"{lib_temp_path}/{d}"
        if d != "." and d != ".." and d != lib_name and os.path.isfile(target_path):
            os.remove(target_path)


def try_create_lib():
    if not create_temp_dir():
        return
    remove_nouse_libs()
    if platform.system() == "Windows":
        # 获取二进制库
        if platform.architecture()[0] == "64bit":
            from l0n0lnet.libse_windows_x64 import libse_data
        else:
            from l0n0lnet.libse_windows_x86 import libse_data
        # 将库写入到缓存目录
        lib_full_path = get_lib_path()
        if not os.path.exists(lib_full_path):
            with open(lib_full_path, 'wb') as fp:
                fp.write(base64.decodebytes(libse_data))
    elif platform.system() == "Linux":
        build_linux_lib()


def get_build_src_path():
    lib_temp_path = get_tmp_path()
    if not lib_temp_path:
        return
    return f"{lib_temp_path}/cppsrc"


def clone_cpp_src():
    src_path = get_build_src_path()
    if not src_path:
        return
    if os.path.exists(src_path):
        r = Repo(src_path)
        r.remote().pull()
    else:
        r = Repo()
        r.clone_from(cppsrc, src_path, multi_options=[f'-b {branch}'])


def build_lib():
    src_path = get_build_src_path()
    if not src_path:
        return
    build_path = f"{src_path}/build"
    os.system(f"cmake -S {src_path} -B {build_path}")
    os.system(f"make -C {build_path}")


def copy_lib():
    src_path = get_build_src_path()
    if not src_path:
        return
    lib_path = f"{src_path}/lib/libse.so"
    if not os.path.exists(lib_path):
        sys.stderr.write("Build cpp lib failed.\n")
        return
    shutil.copy(lib_path, get_lib_path())


def build_linux_lib():
    lib_path = get_lib_path()
    if not lib_path:
        return
    if os.path.exists(lib_path):
        return
    clone_cpp_src()
    build_lib()
    copy_lib()
