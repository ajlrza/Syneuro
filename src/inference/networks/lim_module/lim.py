import transport
import numpy as np
from groq import Groq
from enum import Enum
from datetime import datetime
import subprocess, json, asyncio
from src.inference.networks.networks_classes import SensoryOutput

def get_emotional_state(valence: float, arousal: float) -> tuple[np.complex128, np.complex128]:
    """
    Translates continuous VAD metrics into 3D quantum probability amplitudes.
    Valence (-1.0 to 1.0) drives the polar angle (Theta).
    Arousal (-1.0 to 1.0) drives the azimuthal phase (Phi).
    """
    theta = np.interp(valence, [-1.0, 1.0], [np.pi, 0])      
    phi = np.interp(arousal, [-1.0, 1.0], [0, 2 * np.pi])    

    amp_0 = np.cos(theta / 2)
    
    amp_1 = np.exp(1j * phi) * np.sin(theta / 2)

    return amp_0, amp_1

class QuantumEmotion:
     emotional_state: float = 0.0
     affective_state: np.ndarray = np.array([0.0, 0.0, 0.0])
     stimulus_states: np.ndarray = np.array([0.0, 0.0, 0.0]) 
     stimulus_dict: dict = {}

     bloch_dt = np.dtype(
          [('x', 'f4'), ('y', 'f4'), ('z', 'f4')]
     )
     bloch_vector = np.array(
          [(0.0, 0.0, 0.0)], dtype=bloch_dt
     )
     state_vector: np.ndarray

     def __init__(self):
        self.state_vector = np.array([[1.0 + 0.j], [0.0 + 0.j]], dtype=np.complex128)

     def map_vad_to_angles(self, stimulus: np.ndarray):
        valence, arousal, dominance = stimulus

        theta = np.interp(valence, [-1, 1], [np.pi, 0])
        phi = np.interp(arousal, [-1, 1], [0, 2 * np.pi])
        r = np.interp(dominance, [-1, 1], [0, 1])

        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)

        self.bloch_vector['x'] = x
        self.bloch_vector['y'] = y
        self.bloch_vector['z'] = z

        return self.bloch_vector['x'], self.bloch_vector['y'], self.bloch_vector['z']
     
     def compute_emotion_state(self, theta: float, phi: float, r: float):
        
        amp_0 = np.cos(theta / 2)
        amp_1 = np.exp(1j * phi) * np.sin(theta / 2)
        
        self.state_vector = r * np.array([[amp_0], [amp_1]], dtype=np.complex128)
        return self.state_vector
     
     def compute_emotion_transition(self, stimulus_vad: np.ndarray):
        theta, phi, r = self.map_vad_to_angles(stimulus_vad)
        
        U = np.array([
            [np.cos(theta/2), -np.exp(-1j*phi) * np.sin(theta/2)],
            [np.exp(1j*phi) * np.sin(theta/2), np.cos(theta/2)]
        ], dtype=np.complex128)
        
        self.state_vector = np.dot(U, self.state_vector)
        self.affective_state = self.state_vector
        pass

class LIMNetwork:
     '''
     Responsible for  Deeply involved in the emotional center of the brain; 
     it regulates mood, emotional responses, motivation, and memory formation.
     '''
     client: Groq
     sensor: SensoryOutput
     emotion: QuantumEmotion
     emotion_matrix: dict 
     cen: any

     def __init__(self, app_output: dict, api_key: str):

          from .network_imports import network_builder # Deferred import

          self.client = Groq(api_key=api_key)
          self.sensor = SensoryOutput()
          self.emotion = QuantumEmotion()

          cen_class = network_builder("CEN")
          self.cen = cen_class(agent_output=app_output)

          self.emotion_matrix = {
               "x": {
                    "positive": {"name": "Surprise", "value": 0.0, "min": 0.0, "max": 1.0},
                    "negative": {"name": "Fear", "value": 0.0, "min": 0.0, "max": 1.0}
               },
               "y": {
                    "positive": {"name": "Zeal", "value": 0.0, "min": 0.0, "max": 1.0}, 
                    "negative": {"name": "Calm", "value": 0.0, "min": 0.0, "max": 1.0}, 
                    "mixed_negative": {"name": "Angry", "value": 0.0, "min": 0.0, "max": 1.0} 
               },
               "z": {
                    "positive": {"name": "Happy", "value": 0.0, "min": 0.0, "max": 1.0},
                    "moderate_negative": {"name": "Sad", "value": 0.0, "min": 0.0, "max": 1.0},
                    "extreme_negative": {"name": "Depressed", "value": 0.0, "min": 0.0, "max": 1.0}
               }
          }

          self.amygdala(app_output)

     def update_emotion_matrix(self):
        x_val = self.emotion.bloch_vector['x'][0]
        y_val = self.emotion.bloch_vector['y'][0]
        z_val = self.emotion.bloch_vector['z'][0]

        if x_val > 0 and x_val < 1:
             self.emotion_matrix["x"]["positive"]["value"] = float(x_val)
             self.emotion_matrix["x"]["negative"]["value"] = 0.0
        else:
             self.emotion_matrix["x"]["negative"]["value"] = float(x_val)
             self.emotion_matrix["x"]["positive"]["value"] = 0.0

        if y_val > 0 and y_val < 1:
             self.emotion_matrix["y"]["positive"]["value"] = float(y_val)
             self.emotion_matrix["y"]["negative"]["value"] = 0.0
        else:
            self.emotion_matrix["y"]["positive"]["value"] = 0.0
            self.emotion_matrix["y"]["negative"]["value"] = float(y_val) if y_val > -0.5 else 0.0
            self.emotion_matrix["y"]["mixed_negative"]["value"] = float(y_val) if y_val <= -0.5 else 0.0

        if z_val > 0 and y_val < 1:
            self.emotion_matrix["z"]["positive"]["value"] = float(z_val)
            self.emotion_matrix["z"]["moderate_negative"]["value"] = 0.0
            self.emotion_matrix["z"]["extreme_negative"]["value"] = 0.0
        else:
            self.emotion_matrix["z"]["positive"]["value"] = 0.0
            self.emotion_matrix["z"]["moderate_negative"]["value"] = float(z_val) if z_val > -0.6 else 0.0
            self.emotion_matrix["z"]["extreme_negative"]["value"] = float(z_val) if z_val <= -0.6 else 0.0

        return self.emotion_matrix


     def thalamus(self, sensory_data: dict):

          def check_attention(saved_state_vector, last_timestamp, decay_rate):
               from .network_imports import network_builder
               attention_decay = self.cen.attention_check(saved_state_vector, timestamp, decay_rate)
               if (attention_decay):
                    return attention_decay
               else:
                    return False

          for timestamp, sensor_data in sensory_data.items():
               match type(sensor_data).__name__:

                    # ASYNCIO FOR DATA FLOW, NETWORKING, AND COMMUNICATION
                    # MULTIPROCESSING MODULE FOR MATRIX, MATH, AND OPTMIZE, ANYTHING IN NUMPY, NN

                    case "str":
                         self.sensor.Text = sensory_data
                         self.amygdala(self.sensor.Text)
                         attentionGate = check_attention(self.emotion.state_vector, timestamp, 2.0) # test self.decayrate
                         asyncio.create_task(self.cen.push_attention(attentionGate, sensor_data))
                    case "bytearray":
                         # sensoryOutput is a class because the brain will also check it, be used in other areas
                         self.sensor.Audio = sensor_data
                         self.amygdala(self.sensor.Audio) 
                         attentionGate = check_attention(self.emotion.state_vector, timestamp, 3.0) # test self.decayrate
                         asyncio.create_task(self.cen.push_attention(attentionGate, sensor_data))
                    case "ndarray":
                         self.sensor.Video = sensor_data
                         self.amygdala(self.sensor.Video)
                         attentionGate = check_attention(self.emotion.state_vector, timestamp, 4.0) # test self.decayrate
                         asyncio.create_task(self.cen.push_attention(attentionGate, sensor_data))
    
     def amygdala(self, app_output: object):
          amygdala_work = set()

          get_vad = self.extract_affective_state(app_output)
          compute_emotion = self.emotion.map_vad_to_angles(get_vad)
          print(compute_emotion)

          if (self.sensor.Text == None or self.sensor.Audio == None or self.sensor.Video == None):

               if (self.emotion.emotional_state <= 0 and (self.emotion.affective_state != 0.0).all()):
                    transition_the_emotion = asyncio.create_task(
                         self.emotion.compute_emotion_transition(self.emotion.affective_state)
                    )
                    amygdala_work.add(transition_the_emotion)

               elif (self.emotion.emotional_state >= 0.0 and self.emotion.affective_state[0] != 0.0 and
                     self.emotion.affective_state[1] != 0.0):
                    transition_the_emotion = asyncio.create_task(
                         self.emotion.compute_emotion_transition(self.emotion.affective_state)
                    )
                    amygdala_work.add(transition_the_emotion)

          bloch_vector = self.emotion.bloch_vector[0]

          asyncio.run(self.form_memories())

          if (bloch_vector['x'] + bloch_vector['y'] + bloch_vector['z']) != 0:
               self.update_emotion_matrix()
                    
          return self.emotion_matrix

     async def pass_memory(self, memories):
          return memories

     async def form_memories(self):

          check_stimulus_states = self.emotion.stimulus_states
          stimulus_labels = ["Valence", "Arousal", "Dominance"]
          stimulus_dict = {stimulus_labels[i]: val for i, val in enumerate(check_stimulus_states)}

          pass_memory = asyncio.create_task(self.pass_memory([self.cen.get_working_memory() ** stimulus for stimulus, state in
          stimulus_dict.items() if state > self.emotion.emotional_state]))

          await pass_memory
          print(pass_memory)

          # retrieve result from that asyncio and put to memory.memory_holder

          memory_path = r"C:\Users\MSTR Xen\Documents\SYNEURO\services\python_inference\transport\memory.py"

          result = subprocess.run(["python", memory_path], capture_output=True, text=True, universal_newlines=True)          

          print(transport.memory.memory_holder)

     def extract_affective_state(self, app_output: dict) -> np.ndarray:
   
          system_prompt = """
          You are a sensory feature extractor. Analyze the data and output ONLY valid JSON.
          Format exactly like this: {"valence": float, "arousal": float, "dominance": float}
          Values must be between -1.0 and 1.0.
          """

          response = self.client.chat.completions.create(
               model="llama-3.1-8b-instant",
               messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": ""}
               ],
               response_format={"type": "json_object"}, 
               temperature=0.1 
          )
          
          payload = json.loads(response.choices[0].message.content)
          stimulus = np.array([payload["valence"], payload["arousal"], payload["dominance"]])
          
          return stimulus