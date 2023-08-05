# coding=UTF-8
import os
S_RES = 'res/'
KUOHAO_R = ']'
BACKUP_TAIL = '.backup'  # 备份原始文件


# 对应格式为：|   *- [54.0 B   : res/dimen-sw720dp-v13/dchild_component_ks_poster_width]
def _readResKVFromLineA(msg):
    starIndex = msg.find(S_RES) + len(S_RES)
    endIndex = msg.find(KUOHAO_R)
    resTypeEndIndex = msg.find('/', starIndex)
    resType = msg[starIndex: resTypeEndIndex]
    resName = msg[resTypeEndIndex+1: endIndex]
    return resType, resName

# 对应格式为：dimen:guide_step_birthday_width -> []
def _readResKVFromLineB(temp_msg):
    msg = temp_msg.replace(' ','')
    resTypeEndIndex = msg.find(':')
    resNameEndIndex = msg.find('->')
    resType = msg[0: resTypeEndIndex]
    resName = msg[resTypeEndIndex+1: resNameEndIndex]
    return resType, resName

# 对应格式为：R.string.download_cancel
def _readResKVFromLineC(temp_msg):
    msg = temp_msg.replace('\n',"")
    indexTypeStart = msg.find('.')+1
    indexTypeEnd = msg.rfind('.')
    resType = msg[indexTypeStart: indexTypeEnd]
    resName = msg[indexTypeEnd+1: len(msg)]
    return resType, resName

# 从 line 中 读取 resType，resName，目前支持两种格式
def readResKV(msg):
    if not msg:
        return
    if msg.startswith('R.'):
        return _readResKVFromLineC(msg)
    elif S_RES in msg:
        # 包含 /res 关键字说明是格式 A
        return _readResKVFromLineA(msg)
    else:
        return _readResKVFromLineB(msg)

# 将资源类型裁剪：dimen-sw720dp-v13 裁剪为 dimen-sw720dp，这样做是为了跟工程目录对应
def cutVauleLeftFirst(resType):
    firstMuliIndex = resType.find('-')
    #print(str(firstMuliIndex))
    if firstMuliIndex:
        tail = resType[firstMuliIndex+1:]
        secondMuliIndex = tail.find('-')
        if secondMuliIndex:
            return resType[:firstMuliIndex + secondMuliIndex + 1]
    return resType






