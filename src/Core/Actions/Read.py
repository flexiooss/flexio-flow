from __future__ import annotations

from Core.ConfigHandler import ConfigHandler
from sty import fg, bg


class Read:
    def __init__(self, config_handler: ConfigHandler):
        self.config_handler: ConfigHandler = config_handler

    def __config_handler(self) -> ConfigHandler:
        return self.config_handler

    def __ensure_have_config(self) -> Read:
        if self.__config_handler().file_exists():
            self.__config_handler().load_file_config()
            print(
                """{fg_yellow}###############################################
Flexio Flow 
Core configuration
{path!s}
###############################################

{config!s}{reset_fg}
""".format(
                    path=self.__config_handler().file_path().as_posix(),
                    config=str(self.__config_handler().config.to_dict()),
                    fg_yellow=fg.yellow,
                    reset_fg=fg.rs
                )
            )

        else:
            raise FileNotFoundError

        return self

    def process(self):
        self.__ensure_have_config()
