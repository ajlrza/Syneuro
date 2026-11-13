import os, sys, pytest
from groq import Groq
from datetime import datetime, timezone
from Syneuro import brain

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

def test_init_syneuro_conscious_state():
    
    app_output = None # soon

    key = input(os.environ.get("API_KEY"))

    agent_brain = brain.Brain(key)
    current_time = datetime.now(timezone.utc)

    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    conscious_warmup = agent_brain.activate_conscious_warmup(key)
    user_talk = None

    if (conscious_warmup):

        brain_sense = agent_brain.sense_sensory_data(app_output)
        brain_conscious = agent_brain.activate_conscious_state()
        brain_response = agent_brain.react_to_sensory_data()

        for brain_module, spike in agent_brain.spiked:
            if (not spike):
                continue
            print(f"{brain_module}" + spike)
    else:
        print("Agent's brain consciousness is not warmed up.")
        print("Initializing agent's brain warm-up.")
        conscious_warmup = agent_brain.activate_conscious_warmup(key)