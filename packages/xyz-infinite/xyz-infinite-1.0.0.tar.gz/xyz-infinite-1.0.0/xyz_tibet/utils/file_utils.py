# -*- coding:utf-8 -*-
"""
文件操作utils
"""
import commands
import zipfile

import os
import os.path


def read_file_content_from_file(file_path):
    """
    打印出文件内容
    """
    if not file_path or not os.path.exists(file_path):
        return ''
    result_str = ''
    with open(file_path, 'r') as f:
        while 1:
            line = f.readline()
            result_str += line
            if not line:
                break
    return result_str


def save_uploaded_staff_to_file(memory_file, file_absolute_path):
    """
    将上传上来的文件存储在本地
    """
    try:
        with open(file_absolute_path, 'wb+') as destination:
            for chunk in memory_file.chunks():
                destination.write(chunk)
        return True
    except:
        return False


def replace_file_str(file_path, source_str, target_str):
    """

    """
    if not file_path or not os.path.exists(file_path):
        return ''
    temp_file = '/tmp/this_is_temp_file'
    lines = open(file_path).readlines()  # 打开文件，读入每一行
    fp = open(temp_file, 'w')
    for s in lines:
        fp.write(s.replace(source_str, target_str))
    fp.close()  # 关闭文件
    commands.getoutput("rm -f %s" % file_path)
    commands.getoutput("cp {source_file} {target_file}".format(source_file=temp_file, target_file=file_path))


def read_file_as_memory_file(file_path):
    """

    """
    f = open(file_path, 'r+')
    contents = f.read()
    return contents


def write_file_as_txt(file_path, file_content):
    """

    """
    with open(file_path, 'w') as f:
        f.write(file_content)


def write_file_to_txt_append(file_path, file_content):
    """

    """
    with open(file_path, 'a') as f:
        f.write(file_content)


def write_file_to_txt_append_with_seek(file_path, file_info_list_fo_list):
    """
    适用于多进程写文件
    """
    f = open(file_path, 'a')
    f.seek(0, os.SEEK_END)
    for line in file_info_list_fo_list:
        f.write(line + '\n')


def loop_a_dir(root_dir, sort_by=''):
    """
    遍历一个文件夹,返回该文件夹下面所有的文件名list
    """
    file_name_list = []
    for parent, dir_names, file_names in os.walk(root_dir):
        for filename in file_names:
            file_name_list.append(filename)
    return file_name_list


def zip_dir(dirname, zipfile_name):
    file_list = []
    if os.path.isfile(dirname):
        file_list.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                file_list.append(os.path.join(root, name))
    zf = zipfile.ZipFile(zipfile_name, "w", zipfile.zlib.DEFLATED)
    for tar in file_list:
        arc_name = tar[len(dirname):]
        zf.write(tar, arc_name)
    zf.close()
