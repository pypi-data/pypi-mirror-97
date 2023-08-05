# coding: utf-8
import os
import sys
import argparse
from .m_pre_commit import fun_pre_commit
from .m_clear_attr import fun_clear_attr
from .m_scan_png import fun_scan,UN_CHECK_TIMES

NAME = 'hydg'
ACTION_ATTR = "cleanvalue"
ACTION_SCAN_PNG = "scanpng"
ACTION_PRE_COMMIT = "precommit"

def _scan_pngs(args):
    #print(args)
    # args : (dirs=[], func=<function _scan_pngs at 0x104d5f280>, maxtime=2, minrate=0.2, sub_cmd='scanpng', webp=False, xpng=True)
    fun_scan(dirs = args.dirs, max_times = args.maxtime, min_reduce = args.minrate, 
        webp_enable = args.webp, png_enable = args.xpng)

def _clean_values(args):
    # print(args)
    fun_clear_attr(textbuff = args.report, dir=args.dir)

def _inj_pre(args):
    #print(args.rate)
    #TODO 压缩率透传
    for dir in args.dirs:
        print(dir)
        fun_pre_commit(dir,args.rate)

def main():
    parser = argparse.ArgumentParser(description='youku child pkg slimming tool, more detail go https://www.atatech.org/articles/195338',add_help=False)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'VERSION'), 'r', encoding='utf-8') as version_file:
        version_info = version_file.read().strip()
    argument_group_general = parser.add_argument_group('general options')
    argument_group_general.add_argument('-v', '--version', action='version', version=NAME + version_info)
    argument_group_general.add_argument('-h', '--help', action='help', help='show this help message and exit')

    subparsers = parser.add_subparsers(title='subcommands',description='valid subcommands',help='sub-command help', dest='sub_cmd')
    
    parser_scan = subparsers.add_parser('scanpng')
    parser_scan.add_argument('dirs', metavar='res_dirs', nargs='*', help = "the android module res dirs you want to scan and compres png ")
    parser_scan.add_argument('-mr', '--minrate', type=float, nargs='?', default=0.2, help = "期望的最小压缩率，若达不到则不压缩替换，默认值：0.2")
    parser_scan.add_argument('-mt', '--maxtime', type=int, nargs='?', default = UN_CHECK_TIMES, help = "最大压缩次数，不设置则不检查。如果被反复压缩，图片压缩的次数超过了该值，则压缩不生效")
    parser_scan.add_argument('--webp', action='store_true', help = "开启 webp 转换，默认不使用 webp 转换")
    parser_scan.add_argument('--xpng', action='store_false', help = "关闭 png 压缩，默认使用 png 压缩")
    parser_scan.set_defaults(func=_scan_pngs)

    parser_pre = subparsers.add_parser('precommit')
    parser_pre.add_argument('dirs', metavar='work_dirs', nargs='*', help = "the working dirs you want inject png compression tools before you commit res and codes")
    parser_pre.add_argument('-r', '--rate', type=float, nargs='?', default=0.2, help = "期望的最小压缩率，若达不到则不压缩替换，默认值：0.2")
    parser_pre.set_defaults(func=_inj_pre)

    parser_clean = subparsers.add_parser('cleanvalue')
    parser_clean.add_argument('report', metavar='report_file', type=argparse.FileType('r'), nargs='?',
                        help="the module's unused res list,witch extract from youku franky report。franky 包大小分析工具中将对于模块的无用资源复制出来，拷贝进对应的文件里")
    parser_clean.add_argument('dir', metavar='module_dir', nargs='?', help = "the android module work dir you want scan and remove unused value items")
    parser_clean.set_defaults(func=_clean_values)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()