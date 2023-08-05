# coding=UTF-8
import os,shutil
from reduce import file_tools

''' 增量图片前置压缩任务，这部分逻辑仅仅是将一个 SH 和 一个 py 脚本,，真正的压缩逻辑在 /inject/PY_PRE_COMMIT '''

def _inject_work_git_hooks(path, content_sh, content_py='',minrate = 0.2):
    git_path = os.path.join(path,'.git/hooks')
    file_tools.check_make_dirs(git_path)
    pre_sh_path = os.path.join(git_path,'pre-commit')
    pre_py_path = os.path.join(git_path,'pre_commit.py')
    # 获取 pre_py_path 的绝对路径，将其插入 SH 脚本第一行
    pre_py_abs_path = os.path.abspath(pre_py_path)
    # print('pre_py_path:' + pre_py_abs_path)
    str_head_line = 'prepypath='+pre_py_abs_path+'\n'
    file_tools.create_file(pre_sh_path,content_sh,headline=str_head_line)
    # 让 SH 文本变为 unix 可执行文件
    cmd = "chmod +x " + pre_sh_path
    os.system(cmd)
    file_tools.create_file(pre_py_path,content_py,headlines=['# coding=UTF-8\n','MIN_REDUCE_R = {minrate}\n'.format(minrate = minrate)])

# 将脚本注入进工程的 ./git/hooks/目录
def fun_pre_commit(work_path,min_rate):
    main_py_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(main_py_dir, 'inject/HOOK_PRE_COMMIT'), 'r', encoding='utf-8') as content_sh:
        #读取 SH 脚本内容
        with open(os.path.join(main_py_dir, 'inject/PY_PRE_COMMIT'), 'r', encoding='utf-8') as content_py:
            _inject_work_git_hooks(work_path, content_sh = content_sh, content_py = content_py, minrate = min_rate)
    pngquant = os.path.join(main_py_dir, 'inject/pngquant')
    dst_path = os.path.join(work_path, '.git/hooks/pngquant')
    shutil.copy(src = pngquant,dst = dst_path)