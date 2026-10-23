import os, sys
from typing import Literal
from .network import modules, output, network_builder

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

class Brain:
     
    __slots__ = ['active_modules', 'api_key', 'app_output']

    def __init__(self, api_key) -> None:
        self.app_output: output = None
        self.api_key: str = None
        self.active_modules: modules = None
 
    def activate_brain_module(self, brain_module: str) -> None:

        if brain_module in self.active_modules:
            return f'{brain_module} is already active.'
        
        try:   
            setattr(self.active_modules, brain_module, network_builder(brain_module)(self.app_output))
        except:
            try:
                setattr(self.active_modules, brain_module, network_builder(brain_module)(self.app_output)(self.api_key))
            except:
                setattr(self.active_modules, brain_module, network_builder(brain_module)(self.app_output))
        
    def activate_conscious_state(self, app_output: object, api_key: str) -> bool:

        self.app_output = output()

        self.active_modules = map(setattr(self.app_output, _),app_output)

        self.api_key = api_key

        if (len(app_output['request_activation']) >= 1):

            for brain_module in app_output['request_activation']:
                if brain_module in self.active_modules:
                    self.activate_brain_module(brain_module)

            return self.active_modules

        self.activate_brain_module(app_output['request_activation'][0])
        return True

    def react_to_sensory_data(self) -> dict:

        return self.active_modules.LIM(self.app_output)