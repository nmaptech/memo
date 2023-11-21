import os
import zipfile

"""
ZIP压缩包处理
zipfile 内置库
"""


# 递归删除目录
def delete_folder(folder_path: str):
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
    try:
        os.rmdir(folder_path)
    except PermissionError as e:
        raise (e, "no access")


# 打包文件夹为zip压缩文件
def zip_folder(to_zip_f: str):
    # 检查
    if not os.path.exists(to_zip_f):  # check file exist
        raise FileExistsError(f"folder not exist: {to_zip_f}")
    if not os.access(to_zip_f, os.R_OK):  # check file access
        raise PermissionError(f"folder no read access: {to_zip_f}")
    if not os.access(to_zip_f, os.W_OK):  # check file access
        raise PermissionError(f"folder no write access: {to_zip_f}")

    # 取默认压缩文件名
    *_, zip_file_name = to_zip_f.split(os.sep)
    zip_file_name = f"{zip_file_name}.zip"

    # 执行压缩
    with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
        for root, dirs, files in os.walk(to_zip_f):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path)

    return os.path.abspath(zip_file_name)


# 解压缩zip包
def unzip_file(zip_path: str, unzip_path=None):
    """
    解压zip文件

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
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # 校验压缩包是否损坏 不能覆盖所有损坏情况
            # res = zip_ref.testzip()
            # if res:
            #     raise IOError(f"{zip_path} file is broken")

            for file_info in zip_ref.infolist():
                file_info.filename = file_info.filename.encode('cp437').decode('gbk')  # 修复中文乱码
                zip_ref.extract(file_info, unzip_full_path)
    except zipfile.BadZipFile as e:  # 文件损坏可能报错
        print(f"bad zip file: {zip_path} {e}")
    except OSError as e:  # 文件损坏可能报错
        print(f"os error: {e}")
        return ''

    return os.path.abspath(unzip_full_path)


if __name__ == '__main__':
    # zip_file_path = "xxx.zip"
    # print(unzip_file(zip_file_path))

    to_zip_folder = r"xxx"
    print(zip_folder(to_zip_folder))
