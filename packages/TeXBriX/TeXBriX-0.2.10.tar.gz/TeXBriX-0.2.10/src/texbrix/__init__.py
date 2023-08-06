from . import texbrik
from . import mathbrik
import argparse
from pathlib import Path

__version__ = "0.2.10"
parser = argparse.ArgumentParser(description='create LaTeX file from brix')
parser.add_argument(
    'top_brik',
    metavar='Top Brik',
    type=str,
    help='top .brik document to work with')
parser.add_argument('--template', nargs=1)
parser.add_argument('--version', action='version', version="%(prog)s {v}".format(v=__version__))


def main():
    args = parser.parse_args()
    p = Path(args.top_brik).resolve()
    b = texbrik.brikFromDoc(p)
    if args.template:
        s = b.make_TeX_file(template=Path(args.template[0]).resolve())
    else:
        s = b.make_TeX_file()
    p.with_suffix('.tex').write_text(s)
