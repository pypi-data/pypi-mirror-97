__all__ = [
    'connect',
    'orchestrate',
]

from pyrasgo.rasgo import Rasgo
from pyrasgo.orchestration import RasgoOrchestration


def connect(api_key):
    return Rasgo(api_key=api_key)

def orchestrate(api_key):
    return RasgoOrchestration(api_key=api_key)