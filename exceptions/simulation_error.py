import json
from typing import Dict, Any

from exceptions.simulation_error_codes import SimulationErrorCode

class SimulationError(Exception):
    def __init__(self, error_code: SimulationErrorCode, context: Dict[str, Any] = None) -> None:
        self._error_code: SimulationErrorCode = error_code
        self._context: Dict[str, Any]|None = context

    def get_message(self) -> str:
        return self._error_code.value[1]

    def get_code(self) -> str:
        return self._error_code.value[0]

    def __str__(self):
        return repr(self)

    def __repr__(self):
        msg = f"[{self.get_code()}]: {self.get_message()}"
        if self._context is not None:
            context_msg = ", ".join([f"{key}={repr(value)}" for key, value in self._context.items()])
            msg += f"\nContext {{{context_msg}}}"

        return msg