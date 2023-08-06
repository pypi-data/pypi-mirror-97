import os


def get_module_name(filename):
    """尝试确定源文件的完成模块名，方法是确定它的目录中是否含有 __init__.py 文件

    :param filename: [description]
    :type filename: [type]
    :return: [description]
    :rtype: [type]
    """

    if os.path.basename(filename) == '__init__.py':
        return get_module_name(os.path.dirname(filename))

    init_path = os.path.join(os.path.dirname(filename), '__init__.py')
    mod_name = os.path.basename(filename).replace('.py', '')

    if not os.path.exists(init_path):
        return mod_name

    if not os.path.dirname(filename):
        return mod_name

    return get_module_name(os.path.dirname(filename)) + '.' + mod_name