from ptee.instance import Instance
import argparse
example_str = """
Examples:

1. save to path

   ptee --path=/tmp/log/one.log

2. set backup count

   ptee --path=/tmp/log/one.log --backup=7

3. set file size

   ptee --path=/tmp/log/one.log --max_byte=50m

4. with debug

   ptee --path=/tmp/log/one.log --debug=1
"""

import os
_dir = os.path.dirname(os.path.abspath(__file__))
init_path = os.path.join(_dir, '__init__.py')


def read_version():
    d = {}
    code = open(init_path).read()
    code = compile(code, '<string>', 'exec', dont_inherit=True)
    exec(code, d, d)
    return d['__version__']


parser = argparse.ArgumentParser('ptee',
                                 description='ptee ',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=example_str)
parser.add_argument('--path', dest='path',
                    help='save path', required=True)
parser.add_argument('--backup', dest='backup',
                    default=7, help='backup count')
# parser.add_argument('--encode', dest='encode', default='utf-8')
# parser.add_argument('--line-filter', dest='line_filter', help='regex for line filter')
parser.add_argument("--max_byte", dest="max_byte", default="50m", help="ex 50m, 20k, 5G")
parser.add_argument("--debug", dest="debug", default="0", help="show debug message")
parser.add_argument("--version", action="version", version=read_version())


def main(argv=None):
    if argv is not None:
        convert_args = parser.parse_args(argv)
    else:
        convert_args = parser.parse_args()

    # generated_by_dict_unpack: convert_args
    path, backup, max_byte = convert_args.path, convert_args.backup, convert_args.max_byte
    debug = int(convert_args.debug)
    backup = int(backup)

    ins = Instance(path, backup, max_byte, debug)
    ins.loop()
