from __future__ import annotations

from Core.ConfigHandler import ConfigHandler


class Read:
    def __init__(self, config_handler: ConfigHandler):
        self.config_handler: ConfigHandler = config_handler

    def __config_handler(self) -> ConfigHandler:
        return self.config_handler

    def __final_message(self) -> Read:
        print(
            """###############################################
Enjoy with Flexio FLow 
###############################################
""")
        return self

    def __ensure_have_config(self) -> Read:
        if self.__config_handler().file_exists():
            self.__config_handler().load_file_config()
            print(
                """###############################################
Flexio Flow Core 
###############################################
at : {path!s}

{config!s}
""".format(
                    path=self.__config_handler().file_path().as_posix(),
                    config=str(self.__config_handler().config.to_dict())
                )
            )

        else:
            raise FileNotFoundError

        return self

    def process(self):
        self.__ensure_have_config()
        self.__final_message()
