## Syneuro

Future work: Adapt syneuro to a VLA pipeline for AI gf companions

<img width="1672" height="941" alt="image" src="https://github.com/user-attachments/assets/dba4ca5a-4a0d-402f-bde2-b791cd949df7" />


## Example

```python
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
```