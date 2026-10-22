from groq import Groq
import os
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

while (use_app):
    talk = input("Talk with agent / Stop talking with Agent: enter C")

    if (talk == 'C'):
        break

    agent_response = agent_brain.brain_sensor_entrypoint(talk)
    print(agent_response)