import os, sys, numpy, Groq
from datetime import datetime, timezone
from Syneuro import syneuro

def test_state_helper() -> bool:

    assert isinstance(syneuro.get_emotional_state(0.0, 0.0), tuple) 
    test_one, test_two = syneuro.get_emotional_state(0.0, 0.0)
    assert isinstance(test_one, complex) 
    assert isinstance(test_two, complex) 
    
    return True

def test_quantum_attr(quantum: syneuro.Quantum):

    assert isinstance(quantum.emotional_state, float) 
    assert isinstance(quantum.affective_state, numpy.ndarray) 
    assert isinstance(quantum.stimulus_states, numpy.ndarray) 
    assert isinstance(quantum.bloch_dt, numpy.dtype) 
    assert isinstance(quantum.bloch_vector, numpy.ndarray) 
    assert isinstance(quantum.stimulus_dict, dict)

    return True

def test_emotion_attr(emotion: syneuro.Emotion):

    assert isinstance(emotion.judge, Groq) 
    assert isinstance(emotion.quantum, syneuro.Quantum)
    assert isinstance(emotion.emotion_matrix, dict) 

    assert (len(emotion.emotion_matrix.keys()) == 3)
    assert(list(emotion.emotion_matrix.keys()) == ["x", "y", "z"])

    assert isinstance(emotion.emotion_matrix["x"], dict)
    assert(len(emotion.emotion_matrix["x"].keys()) == 2)
    assert(list(emotion.emotion_matrix["x"].keys()) == ["positive", "negative"])
    assert(len(emotion.emotion_matrix["x"]["positive"].keys() == 4))
    assert(list(emotion.emotion_matrix["x"]["positive"].keys()) == ["name", "value", "min", "max"])

    assert isinstance(emotion.emotion_matrix["x"], dict)
    assert(len(emotion.emotion_matrix["y"].keys()) == 2)
    assert(list(emotion.emotion_matrix["y"].keys()) == ["positive", "negative"])
    assert(len(emotion.emotion_matrix["y"]["positive"].keys() == 4))
    assert(list(emotion.emotion_matrix["y"]["positive"].keys()) == ["name", "value", "min", "max"])

    assert isinstance(emotion.emotion_matrix["z"], dict)
    assert(len(emotion.emotion_matrix["z"].keys()) == 2)
    assert(list(emotion.emotion_matrix["z"].keys()) == ["positive", "negative"])
    assert(len(emotion.emotion_matrix["z"]["positive"].keys() == 4))
    assert(list(emotion.emotion_matrix["z"]["positive"].keys()) == ["name", "value", "min", "max"])