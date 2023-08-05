# coding=UTF-8
import os
import xml.etree.ElementTree as ET

# 从xml文件 {xml_file_name} 中删除，指定列表{del_list}条目

# 使用解析器保留注释
class TreeBuilderWithComments(ET.TreeBuilder):
    def comment(self, data):
        # data 为备注内容
        self.start(ET.Comment, {})
        self.data(data)
        self.end(ET.Comment)


def mixXmlFile(xml_file_name, del_list, item_name='dimen'):
    """
    del target res items in the xml file
    """

    if not del_list:
        return

    tree = ET.parse(xml_file_name, parser=ET.XMLParser(target=TreeBuilderWithComments()))
    root = tree.getroot()

    # 这边新建一个list，而不是直接在 原来的列表中删除。因为有的资源在 value、value-xxhdpi 中可能存在多份
    clearList = list(del_list)
    hasRemoved = False

    for movie in root.findall(item_name):
        # print(movie.attrib['name'])
        # print(movie.text)
        for target_del in clearList:
            if target_del == movie.attrib['name']:
                print('del {0}:{1}'.format(item_name, target_del))
                root.remove(movie)
                clearList.remove(target_del)
                hasRemoved = True
                break

    if hasRemoved:
        tree.write(file_or_filename=xml_file_name, encoding='utf-8', xml_declaration='utf-8',
                   method='xml')


# Test code
# demo_list = ['hdt', 'delme', 'remove', 'testTwo']
# mixXmlFile(xml_file_name='dimens.xml', del_list=demo_list)
# print(demo_list)
