import os, sys
from datetime import datetime, timezone
from Syneuro import syneuro

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

def test_init_syneuro_conscious_state():
    
    app_output = None # soon

    key = input(os.environ.get("API_KEY"))

    emotions = syneuro.Emotion(key)
    current_time = datetime.now(timezone.utc)

    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    emotions.emotion_attach(app_output)