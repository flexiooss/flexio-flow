from FlexioFlow.StateHandler import StateHandler
from Schemes.SchemeFactory import SchemeFactory
from Schemes.Schemes import Schemes


class UpdateSchemeVersion:

    @staticmethod
    def from_state_handler(state_handler: StateHandler) -> StateHandler:
        scheme: Schemes
        for scheme in state_handler.state.schemes:
            SchemeFactory.create(scheme, state_handler).set_version()

            print("""
New version : {0!s}
Level : {1!s}
for scheme : {2!s}
""".format(str(state_handler.state.version), state_handler.state.level.value, scheme.value))
        return state_handler
