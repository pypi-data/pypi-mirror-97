# coding=UTF-8
# 扫描指定目录下的所有图片资源，尝试进行压缩，达到阈值，进行替换

import os
import json

''' 
扫描出 directory 下所有文件，prefix 文件头匹配，postfix 文件后缀匹配
'''

def scan_files(directory, prefix=None, postfix=None):
    files_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root, special_file))
            else:
                files_list.append(os.path.join(root, special_file))

    return files_list

# 返回文件名称
def get_simple_name(file_path):
    return os.path.split(file_path)[1]

# 文件重命名
def rename_file(old_file,new_file):
    try:
        os.rename(old_file, new_file)
    except Exception as e:
        print(e)
        print('rename file fail\r\n')
    else:
        pass
        #print('rename file success\r\n')

# 删除某个文件
def del_file(path):
    if os.path.exists(path):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(path)
    else:
        print('del_file fialed, no such file:%s'%path)  # 则返回文件不存在

# 检查文件或者路径是否全都存在
def files_all_exists(*args):
    for path in args:
        if os.path.exists(path):
            pass
        else :
            return False
    return True

# 文件大小
def fileSizeBytes(file_path):
    return os.path.getsize(file_path)

# 去除文件路径的后缀
def cutFileSuffix(file_path):
    return os.path.splitext(file_path)[0]

# 新建一个文件，往里写入内容 txt_buff
def create_file(file_path, txt_buff, headline = None,headlines = None):
    if os.path.exists(file_path):
        os.remove(file_path)
    f = open(file_path,"a")
    if headline:
        f.write(headline)
    if headlines:
        f.writelines(headlines)
    f.writelines(txt_buff)
    f.close

# 读取json 配置文件，返回一个 json 字典
def read_json_cfg(cfg_path):
    file = open(cfg_path, "rb")
    fileJson = json.load(file)
    return fileJson

# 若没有该目录，创建该目录，包括其父目录
def check_make_dirs(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# 将内容插入某个文件的头部
def addHead2File(file_name, head_content):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    with open(file_name, 'w') as n:
        n.write(head_content+'\n')
        n.writelines(lines)

def int_to_bytes(number,bytes_size = 1):
    return int(number).to_bytes(length = bytes_size,byteorder='big')

def bytes_to_int(bytess):
    return int().from_bytes(bytess,byteorder='big')

def str_to_bytes(str):
    return bytes(str, encoding = 'utf8')

def bytes_to_str(bytess):
    return str(bytess,'utf-8')