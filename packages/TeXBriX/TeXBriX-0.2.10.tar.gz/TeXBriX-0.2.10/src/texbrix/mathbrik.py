from texbrix.texbrik import Texbrik, InputError
from pathlib import Path
import re

class Mathbrik(Texbrik):

    MATHCONTENT   = re.compile(
        r'\\begin{(?P<type>\w+?)}(?P<cnt>[\w\W]*?)\\end{(?P=type)}')
    MATH_PACKAGES = set(['amsmath', 'abssymb', 'amsthm'])

    def __init__(self, absolute_path, prerequisites,
                 packages, mathcontent):

        self.mathcontent = [m.groupdict() for m in mathcontent]
        content = '\n'.join(
            [f'\\begin{{{m["type"]}}}'
             f'\n{m["cnt"]}'
             f'\n\\end{{{m["type"]}}}'
             for m in self.mathcontent])

        Texbrik.__init__(
            self=self,
            absolute_path=absolute_path,
            prerequisites=prerequisites,
            packages=packages,
            content=content)

    @classmethod
    def brikFromDoc(cls, absolute_path: Path):
        try:
            s = Texbrik.brik_document_content(absolute_path)
        except InputError as e:
            raise InputError(str(absolute_path),
                             'Failed finding Brikfile {p}'.format(
                                 p=str(absolute_path))) from e
        m = cls.MATHCONTENT.finditer(s)
        if not m:
            raise InputError(str(absolute_path),
                             'No math content in {p}'.format(
                                 p=str(absolute_path)))
        return cls(
            absolute_path=absolute_path,
            prerequisites=cls.PREREQS.findall(s),
            packages     =cls.PKGS.findall(s),
            mathcontent  =m)