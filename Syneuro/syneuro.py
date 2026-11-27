import numpy as np
from dataclasses import dataclass
from groq import Groq
import orjson, asyncio

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

class Quantum:
     emotional_state: float 
     affective_state: np.ndarray 
     stimulus_states: np.ndarray
     bloch_dt: np.dtype 
     bloch_vector: np.ndarray 
     state_vector: np.ndarray
     stimulus_dict: dict[str, any]

     __slots__ = [
          'emotional_state', 
          'affective_state', 
          'stimulus_states', 
          'stimulus_dict',
          'bloch_dt',
          'bloch_vector',
          'state_vector'
          ]

     def __init__(self) -> None:

        self.emotional_state: float = 0.0
        self.affective_state: np.ndarray = np.array([[1.0 + 0.j], [0.0 + 0.j]], dtype=np.complex128)
        self.stimulus_states: np.ndarray = np.array([[1.0 + 0.j], [0.0 + 0.j]], dtype=np.complex128)
        self.state_vector: np.ndarray = np.array([[1.0 + 0.j], [0.0 + 0.j]], dtype=np.complex128)
        self.stimulus_dict: dict[str, any] = {}
        self.bloch_dt = np.dtype([('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
        self.bloch_vector = np.array([(0.0, 0.0, 0.0)], dtype=self.bloch_dt)

     def map_vad_to_angles(self, vad: np.ndarray) -> None:

        valence, arousal, dominance = vad

        theta = np.interp(valence, [-1, 1], [np.pi, 0])
        phi = np.interp(arousal, [-1, 1], [0, 2 * np.pi])
        lam = np.interp(dominance, [-1, 1], [0, 2 * np.pi]) 

        self.bloch_vector['x'] = np.sin(theta) * np.cos(phi)
        self.bloch_vector['y'] = np.sin(theta) * np.sin(phi)
        self.bloch_vector['z'] = np.cos(theta)
     
     def compute_emotion_state(self, theta: float, phi: float, r: float)  -> np.ndarray:
        
        amp_0 = np.cos(theta / 2)
        amp_1 = np.exp(1j * phi) * np.sin(theta / 2)
        
        self.state_vector = r * np.array([[amp_0], [amp_1]], dtype=np.complex128)
        return self.state_vector
     
     def compute_emotion_transition(self, vad: np.ndarray) -> None:

        x, y, z = self.map_vad_to_angles(vad)
        
        U = np.array([
          [np.cos(x/ 2), -np.exp(1j * z) * np.sin(x / 2)],
          [np.exp(1j * y) * np.sin(x / 2), np.exp(1j * (y + z)) * np.cos(x / 2)]
        ], dtype=np.complex128)
        
        self.state_vector = np.dot(U, self.state_vector)
        self.affective_state = self.state_vector
        self.emotional_state = x + y + z

class Emotion:
     '''
     Responsible for  the emotional center of the brain; 
     it regulates mood, emotional responses, motivation, and memory formation.
     '''
     judge: Groq 
     emotion: Quantum
     emotion_matrix: dict[str, dict[str, dict[str, str | float]]]

     __slots__ = ['judge', 'emotion', 'emotion_matrix']

     def __init__(self, groq_api_key: str):

          self.judge = Groq(api_key=groq_api_key)

          self.emotion = Quantum()

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

     def update_emotion_matrix(self) -> None:

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

     def process(self, text_str: str, oai_compatible_model: str) -> dict[str, any] | dict[str, dict[str, dict[str, str | float]]]:
          vad = self.extract_affective_state(text_str, oai_compatible_model)

          if not (isinstance(vad, np.ndarray)):
               return self.emotion_matrix

          self.emotion.map_vad_to_angles(vad)

          if (self.emotion.emotional_state <= 0.0 and (self.emotion.affective_state != 0.0 + 0.j).all()): 

               self.emotion.compute_emotion_transition(vad)

          elif (self.emotion.emotional_state >= 0.0 and self.emotion.affective_state[0] != 0.0 + 0.j and
               self.emotion.affective_state[1] != 0.0 + 0.j):

               self.emotion.compute_emotion_transition(vad)

          self.update_emotion_matrix()
                    
          return self.emotion_matrix

     def extract_affective_state(self, text_str: str, oai_compatible_model: str) -> np.ndarray | None:
   
          system_prompt = """
          You are a sensory feature extractor. Analyze the data and output ONLY valid JSON.
          Format exactly like this: {"valence": float, "arousal": float, "dominance": float}
          Values must be between -1.0 and 1.0.
          """

          response = self.judge.chat.completions.create(
               model=oai_compatible_model,
               messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text_str}
               ],
               response_format={
                    "type": "json_schema",
                    "json_schema": {
                         "name": "emotions",
                         "strict": True,
                         "schema": {
                              "type": "object",
                              "properties": {
                                   "valence": {"type": "number"},
                                   "arousal": {"type": "number"},
                                   "dominance": {"type": "number"}
                              },
                              "required": ["valence", "arousal", "dominance"],
                              "additionalProperties": False,
                         }
                    }
               }, 
               temperature=0.1 
          )
          payload: dict[str, any] = orjson.loads(response.choices[0].message.content)

          if (
               "valence" not in payload.keys() or
               "arousal" not in payload.keys() or
               "dominance" not in payload.keys()
               ):
               return None

          vad = np.array([payload["valence"], payload["arousal"], payload["dominance"]])
          
          return vad
