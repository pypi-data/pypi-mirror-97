import os
import sys
from pathlib import Path
from functools import reduce


class ModuleImportFinder(object):
    def __init__(self, mod_name):
        self.find_next_line = False
        self.parent_module = None
        self.modules = []
        self.mod_name = mod_name

    def find_modules(self, code):
        """
        从源代码中查找所有import关键字以获取所有模块
        :param code: python 源码
        :return:
        """
        code = code.splitlines()
        for item in code:
            # pass all comment and blank line.
            if not item or item[0] == '#':
                continue
            if self.find_next_line is True:
                self.find_modules_next_line(item, self.parent_module)
            item_import_head = item[:7]
            item_import_tail = item[7:]
            item_from_head = item[:5]
            item_from_tail = item[5:]
            if item_import_head == "import ":
                self.parent_module = None
                if '\\' in item[-1]:
                    self.find_next_line = True
                if ',' in item_import_tail:
                    self.modules += item_import_tail.strip("\\").replace(" ", "").split(",")
                else:
                    self.modules.append(item_import_tail.strip("\\").replace(" ", ""))
            if item_from_head == "from ":
                if '\\' in item[-1]:
                    self.find_next_line = True
                module = item_from_tail.split('import')
                self.parent_module = module[0].strip(" ")
                self.set_absolute_path()
                item_from_tail = module[1]
                if ',' in item_from_tail:
                    modules = item_from_tail.strip("\\").replace(" ", "").split(",")
                    self.modules += map(lambda item: self.parent_module + "." + item, modules)
                else:
                    self.modules.append(self.parent_module + "." + item_from_tail.strip("\\").replace(" ", ""))

    def find_modules_next_line(self, code, module=None):
        """
        :param code:
        :param module: 父模块
        :return:
        """
        if '\\' not in code[-1]:
            self.find_next_line = False
        code = code.strip("\\").replace(" ", "")
        if ',' in code:
            # 切割所有的类、函数、模块
            modules = code.replace(" ", "").split(",")
            if module:
                modules = map(lambda x: module + "." + x, modules)
            self.modules += modules
        else:
            if module:
                code = module + "." + code
            self.modules.append(code)

    def set_absolute_path(self):
        """递归的将相对路径转换为绝对路径."""
        parent_module_tail = self.parent_module.strip(".")
        length = len(self.parent_module) - len(parent_module_tail)
        if length == 0:
            return
        abs_mod_list = self.mod_name.split(".")
        head = abs_mod_list[:-length]
        if not head:
            sys.exit('异常退出：项目结构错误，请检查项目结构')
        self.parent_module = reduce(lambda x, y: x + '.' + y, head) + "." + parent_module_tail


class FileCallGenerator(object):
    def __init__(self, filenames):
        self.file_path = filenames

    def get_module_name(self, filename):
        """
        获取某一文件的模块名
        :param filename:
        :return:
        """

        init_path = os.path.join(os.path.dirname(filename), '__init__.py')
        mod_name = os.path.basename(filename).replace('.py', '')

        if not os.path.exists(init_path):
            return mod_name

        if not os.path.dirname(filename):
            return mod_name

        return self.get_module_name(os.path.dirname(filename)) + '.' + mod_name

    def get_module_list(self):
        """
        获取所有的模块名
        :return:
        """
        self.module_list = []

        # 循环所有的 .py 文件，依次获取其自身的模块名
        for filename in self.file_path:
            mod_name = self.get_module_name(filename)
            self.module_list.append(mod_name)
        return self.module_list

    def find_files(self, mod_name):
        """
        接收一个模块名，递归的返回文件名
        :param mod_name:
        :return:
        """
        if mod_name in self.module_list:
            return mod_name
        elif "." in mod_name:
            mod_name_list = mod_name.split(".")
            mod_name = reduce(lambda x, y: x + '.' + y, mod_name_list[:-1])
            return self.find_files(mod_name)
        else:
            return False

    def generate_call_rel(self):
        """
        生成调用关系
        :return:
        """
        self.call_rel = {}
        for filename in self.file_path:
            mod_name = self.get_module_name(filename)
            with open(filename, "rt", encoding="utf-8") as f:
                content = f.read()
            finder = ModuleImportFinder(mod_name)
            finder.find_modules(content)
            found = set()
            for item in finder.modules:
                res = self.find_files(item)
                if res is False:
                    continue
                else:
                    found.add(res)
            self.call_rel[mod_name] = list(found)
        return self.call_rel

    def finish(self):
        """
        输出最终node、edge的关系
        :return:
        """
        nodes = self.get_module_list()
        edges = []
        for src, dsts in self.generate_call_rel().items():
            if not dsts:
                continue
            for dst in dsts:
                edges.append((src,dst))
        return nodes,edges


# if __name__ == '__main__':
#
#     path_base = '/mnt/ubuntu/opt/projects/cosmosdb'
#     # only find python file
#     path_list = list(Path(path_base).rglob("*.py"))
#     filenames = [i.as_posix() for i in path_list]
#
#     file_an = FileCallGenerator(filenames)
#
#     # 生成文件间的调用关系
#     from pyvis.network import Network
#
#     net = Network(heading='XDetection-Module', width="1300px", height="100%",directed=True)
#     net.show_buttons(filter_=['physics'])
#     # 创建节点
#     net.add_nodes(file_an.get_module_list())
#     # 创建边
#     for src, dsts in file_an.generate_call_rel().items():
#         if not dsts:
#             continue
#         for dst in dsts:
#             net.add_edge(src, dst)
#     net.show('XDetection-module.html')
