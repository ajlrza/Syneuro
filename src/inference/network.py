from dataclasses import dataclass
from typing import Literal
from .networks import CENNetwork, LIMNetwork, SALNetwork

@dataclass
class modules(slots=True):
    CEN: CENNetwork
    LIM: LIMNetwork
    SAL: SALNetwork

@dataclass
class output(slots=True):
    sensory: dict[str, str]
    modalities: list[Literal['TextSensor', 'AudioSensor', 'VideoSensor']]
    request_activation: list[Literal['CEN', 'LIM']]
    active_modules: modules

def network_builder(network: str):

    networks = {"CEN": CENNetwork, "LIM": LIMNetwork, "SAL": SALNetwork}
    return networks[network]