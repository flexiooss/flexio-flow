from pathlib import Path
from typing import Optional

from Schemes.Schemes import Schemes


class Options:
    auto_stash: bool = False
    close_issue: bool = True
    create: bool = False
    default: bool = False
    debug: bool = False
    filename: Optional[str] = None
    from_schemes: Optional[Schemes] = None
    keep_branch: bool = False
    major: bool = False
    message: Optional[str] = None
    no_cli: bool = False
    read: bool = False
    repository_checkout_spec: Optional[str] = None
    repository_id: Optional[str] = None
    repository_name: Optional[str] = None
    scheme: Optional[Schemes] = None
    scheme_dir: Optional[Path] = None
    to_schemes: Optional[Schemes] = None
    version_dir: Optional[Path] = None
    version: Optional[str] = None
