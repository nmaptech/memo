import os
import rarfile

"""
RAR压缩包处理
rarfile 三方库 pip install rarfile -i https://pypi.tuna.tsinghua.edu.cn/simple
支持解压：需要配置环境变量 将winrar的路径加入环境变量 重启pycharm
支持压缩：通过执行windows命令实现 需要给出winrar可执行文件路径
"""


# 递归删除目录
def delete_folder(folder_path):
    """
    folder_path: 要删除的目录名。
    """
    # check folder exist
    if not os.path.exists(folder_path):
        return

    # del items in folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            # del file
            os.remove(item_path)
        else:
            # del folder
            delete_folder(item_path)

    # del empty folder
    os.rmdir(folder_path)


# 打包文件夹为rar压缩包
def folder_to_rar(to_rar_f: str, win_rar_path=r'C:/"Program Files"/WinRAR/WinRAR.exe'):
    """
    to_rar_f: 待压缩的文件或者目录
    win_rar_path: windows上winrar可执行文件位置
    return： 压缩文件全路径
    """
    # 检查
    if not os.path.exists(to_rar_f):  # check file exist
        raise FileExistsError(f"folder not exist: {to_rar_f}")
    if not os.access(to_rar_f, os.R_OK):  # check file access
        raise PermissionError(f"folder no read access: {to_rar_f}")
    if not os.access(to_rar_f, os.W_OK):  # check file access
        raise PermissionError(f"folder no write access: {to_rar_f}")

    # 取默认压缩文件名 执行压缩
    *_, rar_file_name = to_rar_f.split(os.sep)

    rar_file_name = f"{rar_file_name}.rar"

    if os.path.exists(rar_file_name):
        os.remove(rar_file_name)

    # win_rar_path = r'C:/"Program Files"/WinRAR/WinRAR.exe'  # 路径带有空格必须加一层引号
    f_dir = os.path.dirname(os.path.abspath(rar_file_name))
    print(f_dir)
    base_name = os.path.basename(to_rar_f)
    os.chdir(f_dir)  # 切换工作目录 切到目标的父路径
    os.system(rf"{win_rar_path} a {rar_file_name} {base_name}")  # 执行压缩

    return os.path.abspath(rar_file_name)


# 压缩包处理 解压缩zip包 默认解压到同名文件夹 返回解压所在目录和文件列表
def unrar_file(zip_path: str, unzip_path=None):
    """
    解压rar文件

    :param zip_path: 压缩文件路径
    :param unzip_path: 解压位置 默认压缩文件同目录下 同名目录
    :return: 解压后 全路径
    """

    # 检查
    if not os.path.exists(zip_path):  # check file exist
        raise FileExistsError(f"file not exist: {zip_path}")
    if not os.access(zip_path, os.R_OK):  # check file access
        raise PermissionError(f"file no read access: {zip_path}")

    # 压缩文件路径 自适应
    zip_full_path = zip_path
    if not os.path.isabs(zip_path):
        zip_full_path = os.path.abspath(zip_path)
    base_name = os.path.basename(zip_full_path)  # testcase.zip
    pre_path, extension = os.path.splitext(base_name)  # 路径(不包括扩展名) 文件类型

    # 解压路径 自适应
    unzip_full_path = unzip_path
    if not unzip_path:
        unzip_full_path = pre_path
    if os.path.exists(unzip_full_path):
        delete_folder(unzip_full_path)

    # 执行解压
    with rarfile.RarFile(zip_path, 'r') as rar_ref:
        rar_ref.extractall(unzip_full_path)

    return os.path.abspath(unzip_full_path)


if __name__ == '__main__':
    rar_file_path = r"xxx.rar"
    print(unrar_file(rar_file_path))

    # to_rar_folder = r"xxx"
    # print(folder_to_rar(to_rar_folder))
