# coding=UTF-8
import os,sys
from reduce import file_tools as FT
from pip._internal import main as pip_cmd

PNGQUANT_FILE = 'inject/pngquant'
PNGQUANT_EXT_END = '_new.png'
WEBP_END = '.webp'
CHUNK_TYPE_R_TIMES = 'cTMs'
UN_CHECK_TIMES = 88
log_enable = True

# 当前.py文件寻址

now_dir = os.path.dirname(os.path.abspath(__file__))

# 将 pngquant 文件路径改一下；
pngquant_path = os.path.join(now_dir, PNGQUANT_FILE)

def _need_check_max_times(times):
    return not times == UN_CHECK_TIMES

def _import_png_or_load():
    try:
        import png
    except ImportError:
        print('pypng 模块不存在，开始下载')
        pip_cmd(['install','--upgrade', 'pypng'])

def _read_compress_times(png_path):
    _import_png_or_load()
    import png
    reader = png.Reader(filename=png_path)
    chunks = reader.chunks()
    times = 0
    for chunk_item in chunks:
        if CHUNK_TYPE_R_TIMES == FT.bytes_to_str(chunk_item[0]):
            times = FT.bytes_to_int(chunk_item[1])
            break
    return times

# 将压缩次数写入 png
def _write_compress_times(png_path, dst_png, times = 0):
    _import_png_or_load()
    import png
    reader = png.Reader(filename=png_path)
    chunks = reader.chunks()
    chunk_list = list(chunks)
    #第一个chunk是固定的IHDR，我们把tEXt放在第2个chunk
    inserted = False
    for item in chunk_list:
        if FT.bytes_to_str(item[0]) == CHUNK_TYPE_R_TIMES:
            index = chunk_list.index(item)
            new_item = list(item)
            new_item[1] = FT.int_to_bytes(times)
            chunk_list.remove(item)
            chunk_list.insert(index, tuple(new_item))
            inserted = True
    if not inserted:
        chunk_item = tuple([FT.str_to_bytes(CHUNK_TYPE_R_TIMES), FT.int_to_bytes(times)])
        # 第一个chunk是固定的 IHDR，我们把cTMs放在第2个 chunk
        chunk_list.insert(1, chunk_item)
    with open(dst_png, 'wb') as dst_file:
        png.write_chunks(dst_file, chunk_list)
    return times


# 返回 0 表示压缩成功
def _cmd_pngquant(png_path, ext_end = PNGQUANT_EXT_END):
    # print("_cmd_pngquant:"+pngquant_path)
    # -f 覆盖已存在的文件
    cmd = "{pngquant} --quality=80-99 -f --ext={0} --speed=3 {1}".format(
        ext_end, png_path, pngquant=pngquant_path)
    return os.system(cmd)

# 检查新图片的大小，若达到预期替换，返回 True ；若不替换 返回 False
def _check_size_replace(origin_pic, new_pic, min_reduce = 0.2, replace_enable = False,log_tag =''):
    if not FT.files_all_exists(origin_pic,new_pic):
        return
    size_origin = FT.fileSizeBytes(origin_pic)
    size_new = FT.fileSizeBytes(new_pic)
    if size_origin * ( 1 - min_reduce ) > size_new :
        # 达到压缩阈值,删除原始文件，重命临时文件使其变为正式文件
        if replace_enable:
            FT.del_file(origin_pic)
            FT.rename_file(new_pic, origin_pic)
        print('{tag} compressed :{f} {s0} -> {s1}'.format(tag = log_tag, f=os.path.split(origin_pic)[1],s0 = size_origin,s1 = size_new))
        return True
    else:
        # 未达阈值，删除临时文件
        # print('quant pass:' + origin_pic)
        FT.del_file(new_pic)
        return False


# 
def _quant_and_check(origin_png, min_reduce = 0.2, max_times = UN_CHECK_TIMES):
    # 检车压缩次数，决定是否继续压缩
    if _need_check_max_times(max_times):
        # 检查压缩次数
        origin_compressed_times = _read_compress_times(origin_png)
        if origin_compressed_times >= max_times:
            print('压缩次数上限:'+FT.get_simple_name(origin_png))
            return
    result = _cmd_pngquant(origin_png)
    if result == 0:
        # 转换成功
        new_png_path = FT.cutFileSuffix(origin_png) + PNGQUANT_EXT_END
        compressed = _check_size_replace(origin_pic = origin_png,new_pic = new_png_path,
            min_reduce = min_reduce, replace_enable=False, log_tag = 'pngquant')
        if compressed:
            origin_compressed_times = _read_compress_times(origin_png)
            # 将压缩次数写入 png 文件，覆盖原图，删除临时的新图
            _write_compress_times(new_png_path, dst_png = origin_png, times = origin_compressed_times+1)
            FT.del_file(new_png_path)
    else:
        print('quant failed: '+ origin_png )


# cwebp [options] -q quality input.png -o output.webp
def _webp_and_check(origin_png, min_reduce = 0.2):
    if origin_png.endswith('.9.png'):
        return
    new_webp_path = FT.cutFileSuffix(origin_png) + WEBP_END
    cmd = "cwebp {pic} -q {quality} -o {new} -quiet".format(pic = origin_png,quality = 80, new = new_webp_path,)
    os.system(cmd)
    succ = _check_size_replace(origin_pic = origin_png,new_pic = new_webp_path,
        min_reduce = min_reduce, replace_enable = False,log_tag = 'webp')
    if succ:
        FT.del_file(origin_png)
        # TODO webp add git
        #os.system('git add ' + new_webp_path)

def _scan_path_and_compression(path, **kwargs):
    webp_enable = kwargs.get('webp_enable',False)
    png_enable = kwargs.get('png_enable',False)
    max_times = kwargs.get('max_times',UN_CHECK_TIMES)
    min_reduce = kwargs.get('min_reduce',0.2)
    print('scan config:')
    print(kwargs)
    png_list = FT.scan_files(path, postfix='.png')
    for origin_png in png_list:
        if png_enable:
            _quant_and_check(origin_png,min_reduce = min_reduce,max_times = max_times)
        if webp_enable:
            _webp_and_check(origin_png,min_reduce = min_reduce)

def fun_scan(**kwargs):
    dirs = kwargs.get('dirs')
    if dirs:
        for path in dirs:
            _scan_path_and_compression(path,**kwargs)
    

