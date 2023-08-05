# coding=UTF-8
# 扫描删除以下资源进行删除： *- [24.0 B   : res/id/child_view_holder]
# res/id
# res/string
# res/dimen
# res/color
import os
from reduce import util_res_read as utils
from reduce import util_res_xml
import sys
import json

S_DIR_NAME_VALUES = 'values'
S_DIMEN = 'dimen'

# 目标资源类型 tuple，不可修改
TARGET_RES_TYPES = ('id','string','dimen','color')

'''具体类型的条目的标签名称，对应 {TARGET_RES_TYPES}，若没有匹配到，直接取 RES_TYPE'''
TARGET_RES_ITEM_MAP = {'id':'item'}

# 存放待删除的资源,数据类型 字典 {"key":[xx,xx]}
dictRes = {}

for data in TARGET_RES_TYPES :
    dictRes[data] = []
            
def _read_report_file(report_buff):
    for line in report_buff:
        kv = utils.readResKV(line)
        if not kv:
            continue
        if TARGET_RES_TYPES.__contains__(kv[0]) :
            dictRes[kv[0]].append(kv[1])
        elif kv[0].__contains__(S_DIMEN):
            key = utils.cutVauleLeftFirst(kv[0])
            if not key in dictRes:
                dictRes[key] = [kv[1]]
            else :
                dictRes[key].append(kv[1])

# 函数：清理目标 values 文件夹下的 目标 资源；
def _clearTargetResInValueFile(targetRes, values_dir):
    for (key,value) in targetRes.items():
        if key in TARGET_RES_TYPES:
            dirs = os.listdir(values_dir)
            # 拎出 dirs 下文件名中包含 key 关键字的文件名
            x = [i for i in dirs if key in i]
            #print(x)
            if x:
                workFilePath = os.path.join(values_dir, x[0])
                print('workFilePath:' + workFilePath)
                #print(value)
                item_cell_name = TARGET_RES_ITEM_MAP.get(key)
                if not item_cell_name:
                    item_cell_name = key
                util_res_xml.mixXmlFile(xml_file_name = workFilePath, del_list = value, item_name = item_cell_name)

# 清理， values_dirs：value 资源文件下列表
def _clearTargetResDir(values_dirs):
    if values_dirs:
        for values_dir in values_dirs:
            _clearTargetResInValueFile(targetRes = dictRes, values_dir = values_dir)


# textbuff 是无用资源清单 _io.TextIOWrapper ; dir_array 是目标扫描路径
def fun_clear_attr(textbuff,dir):
    if not textbuff:
        print('unused file is null')
        sys.exit(2)
    if not dir:
        print('error: target resource dir is required')
        sys.exit(2)

    _read_report_file(textbuff)
    #print(dictRes)
    value_dir_array = []
    for root, sub_dirs, files in os.walk(dir):
        for child_dir in sub_dirs:
            if 'value' in child_dir and not 'build/intermediates' in root:
                value_dir_array.append(os.path.join(root, child_dir))

    _clearTargetResDir(value_dir_array)



