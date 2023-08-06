from pathlib import Path
from string import Template
import re
from importlib import resources


class Texbrik:
    PREREQS = re.compile(r'\\prerequisite{(?P<relativepath>[/_\w]+?)}')
    BRIKINSERTS = re.compile(r'\\brikinsert{(?P<relativepath>[/_\w]+?)}')
    PKGS = re.compile(r'\\include{(\w+?)}')
    BRIKCONTENT = re.compile(r'\\begin{content}([\w\W]*?)\\end{content}')

    def __init__(self, absolute_path: Path,
                 prerequisites, packages, content):
        """

        Args:
            absolute_path (Path): [description]
            prerequisites ([str]): relative paths to prerequisite briks
            packages ([str]): latex import packages
            content (str): content of brik

        Raises:
            InputError: if imports of prerequisites etc. fail
        """
        if not absolute_path.is_absolute():
            raise InputError(
                str(absolute_path),
                '{path} is not an absolute path'.format(
                    path=str(absolute_path)))
        self.path          = absolute_path
        self.packages      = set(packages)
        self.content       = content
        try:
            self.prerequisites = [self._relative_pathstring_to_path(p) for p in prerequisites]
        except InputError as e:
            raise InputError(str(self.path),
                             'Failed to process prerequisites.') from e
        self.brikinserts   = dict()
        self.expanded      = False
        self.ignore        = set() #set of absolute paths

    def __eq__(self, other) -> bool:
        return self.path == other.path \
            if isinstance(other, Texbrik) else False

    def expand(self, ignore: set = set()):
        """recursively adds all imports from brikinsert, usepackage and brikcontent
        to content, ignoring everything mentioned in igore (except when
        explicitely inserted via brikinsert)

        Args:
            ignore (set, optional): Briks to ignore in prerequisite.
            Defaults to set().

        Raises:
            InputError: If there is something wrong with a prerequisite or
                brikinsert
        """

        self.ignore |= ignore
        if self.expanded:
            return
        try:
            self.brikinserts = dict([
                (b, brikFromDoc(
                    self._relative_pathstring_to_path(b)))
                for b in __class__.BRIKINSERTS.findall(self.content)
            ])
        except InputError as e:
            raise InputError(str(self.path),
                             'Failed to process prerequisites.') from e
        self.content = __class__.BRIKINSERTS.sub(
            self._process_brikinsert_occurrence, self.content)
        # since the error for _relative_pathstring_to_path has not been thrown for b[0], it will not make any problems here

        s = ""
        for p in self.prerequisites:
            if p in self.ignore:
                continue
            b = brikFromDoc(p)
            b.expand(ignore=self.ignore)
            self.ignore |= b.ignore
            self.ignore.add(p)
            self.packages |= b.packages
            s += b.content

        self.content = s \
            + "\n%From TeXBriK [{path}]\n".format(
                path=str(self.path)) \
            + self.content \
            + "\n%End of TeXBriK [{path}]\n".format(
                path=str(self.path))
        self.expanded = True

    def _process_brikinsert_occurrence(self, match_object):
        p = match_object[1]
        b = self.brikinserts[p]
        b.expand(ignore=self.ignore)
        self.packages |= b.packages
        self.ignore |= b.ignore
        self.ignore.add(self._relative_pathstring_to_path(p))
        return b.content

    def _relative_pathstring_to_path(
            self, relative_pathstring: str) -> Path:
        p = self.path.parent.joinpath(relative_pathstring)
        b = p.with_suffix('.brik').exists()
        m = p.with_suffix('.mbrik').exists()
        if b and m:
            raise InputError(str(self.path),
                             'Both .mbrik and .brik file exists for {n}'.format(
                                 n=str(p)))
        if b:
            return p.with_suffix('.brik')
        if m:
            return p.with_suffix('.mbrik')
        raise InputError(str(self.path),
                         'No brikfile {n} exists in {p}'.format(
                             n=p.stem, p=str(p.parent)))

    def expanded_content(self) -> str:
        self.expand()
        return self.content

    #TODO default template not found - look at how data is packaged with setuptools
    def make_TeX_file(
            self,
            template: Path = False) -> str:
        """Generates LaTeX File from this TeXBriK

        Args:
            template (Path, optional): File to insert content to.
            Defaults to
                Path(__file__).resolve().parent.joinpath( 'data/default_template').

        Returns:
            str: LaTeX document's content
        """
        if not template:
            with resources.path(__package__, 'default_template.dat') as p:
                template = p

        self.expand()
        t = Template(template.read_text())
        packages = '\n'.join([
            '\\usepackage{{{}}}'.format(i) for i in self.packages])
        return t.substitute(
            packages=packages,
            content=self.content
        )

    @classmethod
    def brikFromDoc(cls, absolute_path: Path):
        """parses .brik document to create a TeXBriK object

        Args:
            absolute_path (Path): Location of the .brik document

        Raises:
            InputError: If there is a problem with the path location
            or document

        Returns:
            Texbrik: generated TeXBriK object
        """

        try:
            s = __class__.brik_document_content(absolute_path)
        except InputError as e:
            raise InputError(str(absolute_path),
                             'Failed finding Brikfile {p}'.format(
                                 p=str(absolute_path))) from e

        c = __class__.BRIKCONTENT.findall(s)
        if len(c) != 1:
            raise InputError(str(absolute_path), 'none or too many content blocks')

        return cls(
            absolute_path=absolute_path,
            prerequisites=__class__.PREREQS.findall(s),
            packages     =__class__.PKGS.findall(s),
            content      =c[0]
        )

    @staticmethod
    def brik_document_content(absolute_path: Path) -> str:
        if not absolute_path.is_absolute():
            raise InputError(
                str(absolute_path),
                '{path} is not an absuolte path'.format(path=str(absolute_path)))

        if not (absolute_path.is_file() and absolute_path.suffix.endswith('brik')):
            raise InputError(
                str(absolute_path),
                '{brik} is not a TeXBriK'.format(brik=str(absolute_path)))
        return absolute_path.read_text()

def brikFromDoc(absolute_path: Path) -> Texbrik:
    if absolute_path.suffix == '.brik':
        return Texbrik.brikFromDoc(absolute_path)
    if absolute_path.suffix == '.mbrik':
        from texbrix.mathbrik import Mathbrik
        return Mathbrik.brikFromDoc(absolute_path)
    raise InputError(str(absolute_path),
                     'Document {d} not found'.format(
                         d=str(absolute_path)))


class InputError(Exception):
    """Exception raised for errors on the input.

    Attributes:
    expression: input expression in which the error occured
    message: explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

