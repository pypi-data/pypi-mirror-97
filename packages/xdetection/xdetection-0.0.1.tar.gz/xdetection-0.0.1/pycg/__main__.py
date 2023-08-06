import os
from pathlib import Path
from optparse import OptionParser
from pycg.pycg import CallGraphGenerator
from pycg.machinery.modulecall import FileCallGenerator
from pycg.formats.visgraph import VisualGraph


def main():
    usage = """usage: xdetection PATH..."""
    desc = ('Analyse one or more Python source files and generate an'
            'approximate call graph of the modules, classes and functions'
            ' within them.')

    parser = OptionParser(usage=usage,description=desc)

    parser.add_option(
        "--function",
        help="Generate function-based call relationships.",
        action="store_true",
        default=True
    )

    parser.add_option(
        "--module",
        help="Generate module-based calling relationships.",
        action="store_true",
        default=False
    )

    parser.add_option(
        "--format",
        help="Output format.",
        default=None
    )

    option,args = parser.parse_args()

    if len(args) == 0:
        parser.error('Please enter the PATH parameter.')
    path = args[0]

    if not os.path.exists(path):
        parser.error('cannot access {0}: No such file or directory'.format(path))

    if os.path.isdir(path):
        filenames = [i.as_posix() for i in list(Path(path).rglob("*.py"))]
    else:
        filenames = [path]

    if option.module:
        # 生成基于module的调用关系
        nodes, edges = FileCallGenerator(filenames).finish()
    else:
        # 生成基于函数的调用关系
        cg = CallGraphGenerator(filenames,path if os.path.isdir(path) else None)
        cg.analyze()
        nodes, edges = cg.output_internal_nodes_edges()

    visgra = VisualGraph(nodes, edges, True if option.module else False)

    if option.format == 'html':
        visgra.html()
    elif option.format == 'svg':
        visgra.svg()
    elif option.format == 'dot':
        visgra.dot(is_created=True)
    elif option.format == 'jpg':
        visgra.jpg()
    elif option.format == 'pdf':
        visgra.pdf()
    else:
        print({"nodes": visgra.nodes,"edges": visgra.edges})


if __name__ == "__main__":
    main()
