from typing import List

from FlexioFlow.Options import Options
from FlexioFlow.options.Option import Option
from FlexioFlow.options.Create import Create
from FlexioFlow.options.Debug import Debug
from FlexioFlow.options.Default import Default
from FlexioFlow.options.FileName import FileName
from FlexioFlow.options.From import From
from FlexioFlow.options.Help import Help
from FlexioFlow.options.KeepBranch import KeepBranch
from FlexioFlow.options.Major import Major
from FlexioFlow.options.Message import Message
from FlexioFlow.options.NoCli import NoCli
from FlexioFlow.options.Read import Read
from FlexioFlow.options.RepositoryCheckoutSpec import RepositoryCheckoutSpec
from FlexioFlow.options.RepositoryId import RepositoryId
from FlexioFlow.options.RepositoryName import RepositoryName
from FlexioFlow.options.Scheme import Scheme
from FlexioFlow.options.SchemeDir import SchemeDir
from FlexioFlow.options.To import To
from FlexioFlow.options.Version import Version
from FlexioFlow.options.VersionDir import VersionDir


class Resolver:
    options: List[Option] = [Create, Debug, Default, FileName, From, Help, KeepBranch, Major, Message, NoCli, Read,
                             RepositoryCheckoutSpec, RepositoryId, RepositoryName, Scheme, SchemeDir, To, Version,
                             VersionDir]

    def resolve(self, opt: str, arg: str, options: Options):
        o: Option
        for o in self.options:
            o.process(opt=opt, arg=arg, options=options)

    def short_name_options(self) -> str:
        ret: str = ''
        for o in self.options:
            if o.SHORT_NAME is not None:
                ret += o.SHORT_NAME
                if (o.HAS_VALUE == True):
                    ret += ':'
        return ret

    def name_options(self) -> List[str]:
        ret: List[str] = []
        for o in self.options:
            v: str = o.NAME
            if (o.HAS_VALUE == True):
                v += '='
            ret.append(v)
        return ret
