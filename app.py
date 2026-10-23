from groq import Groq
import os
from datetime import datetime, timezone
from src.inference import brain

client = Groq()
use_app = False
use_talk = False

use_or_not = input("Use app? y or n")

if not isinstance(use_or_not, str):
    print("y or n only")
    exit()

if (use_or_not == 'y'):
    use_app = True
elif (use_or_not == 'n'):
    exit()

key = input(os.environ.get("API_KEY"))

agent_brain = brain.Brain(key)
current_time = datetime.now(timezone.utc)

formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

conscious_warmup = agent_brain.activate_conscious_warmup(key)
user_talk = None

while (use_app):
    talk = input("Talk with agent / Stop talking with Agent: enter C")

    if (talk == 'C'):
        break

    app_output = {
        'sensory': {
            f'{formatted_time}': talk
        },
        'modalities': ['Text'],
        'request_activation': ['CEN'],
        'active_modules': []
    }

    if (conscious):

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
        conscious = agent_brain.activate_conscious_warmup(key)

