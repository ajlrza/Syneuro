import os, sys
from groq import Groq
from .networks import CENNetwork, LIMNetwork, SALNetwork

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

def network_builder(network: str):

    networks = {"CEN": CENNetwork, "LIM": LIMNetwork, "SAL": SALNetwork}
    return networks[network]

class Brain:
     
    __slots__ = ['active_modules', 'api_key', 'app_output']

    def __init__(self, app_output: object, api_key):
        self.app_output = app_output
        self.api_key = api_key
        self.active_modules = {"CEN": None, "LIM": None, "SAL": None}

    def activate_brain_module(self, brain_module: str):

        if brain_module in self.active_modules.keys():
            return f'{brain_module} is already active.'
        
        try:   
            self.active_modules[brain_module] = network_builder(brain_module)(self.app_output)
        except:
            try:
                self.active_modules[brain_module] = network_builder(brain_module)(self.app_output, self.api_key)
            except:
                self.active_modules[brain_module] = network_builder(brain_module)(self.app_output)
        
    def activate_conscious_state(self, app_output: object, api_key: str):

        if (len(app_output['request_activation']) >= 1):
            for brain_module in app_output['request_activation']:
                self.activate_brain_module(brain_module)

        if (len(app_output['sensory'].keys()) >= 1 and len(self.brain_management.active_modules.keys()) >= 1):

            cen_work = self.brain_management.active_modules['CEN']
            lim_work = self.brain_management.active_modules['LIM']

            cen_active = cen_work(app_output)
            lim = lim_work(app_output, api_key)

            print(lim.emotion_matrix)
        else:
            return ("Syneuro does not process any sensor_data and active brain modules at the moment.")
        
        # There's no need for database ID in this, as it is not an application but a middleware.