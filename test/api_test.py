import os, sys, numpy, Groq, typing
from datetime import datetime, timezone
from Syneuro import syneuro

def emotion_attr_helper(emotion_dict: dict[str, any] | dict[str, dict[str, dict[str, str | float]]]) -> bool:

    if ("prev" in list(emotion_dict.keys()) and "new" in list(emotion_dict.keys())):

        for coord in ["x", "y", "z"]:
            
            for polarity in ["positive", "negative"]:

                assert(
                    emotion_dict["prev"][coord][polarity]["name"] != 
                    emotion_dict["new"][coord][polarity]["name"])
                assert(
                    emotion_dict["prev"][coord][polarity]["value"] != 
                    emotion_dict["new"][coord][polarity]["value"])
                assert(
                    emotion_dict["prev"][coord][polarity]["min"] != 
                    emotion_dict["new"][coord][polarity]["min"])
                assert(
                    emotion_dict["prev"][coord][polarity]["max"] != 
                    emotion_dict["new"][coord][polarity]["max"])
        return True

    elif (list(emotion_dict.keys()) == ["x", "y", "z"]):
        for coord in ["x", "y", "z"]:
            
            assert isinstance(emotion_dict[coord], dict)
            assert(len(emotion_dict[coord].keys()) == 2)
            assert(list(emotion_dict[coord].keys()) == ["positive", "negative"])

            for polarity in ["positive", "negative"]:

                assert isinstance(emotion_dict[coord][polarity], dict)
                assert(len(emotion_dict[coord][polarity].keys()) == 4)
                assert(list(emotion_dict[coord][polarity].keys()) == ["name", "value", "min", "max"])
                assert(
                    isinstance(emotion_dict[coord][polarity]["name"], str) and
                    isinstance(emotion_dict[coord][polarity]["value"], float) and
                    isinstance(emotion_dict[coord][polarity]["min"], float) and
                    isinstance(emotion_dict[coord][polarity]["max"], float) 
                )
        return True

    else:
        return False
    
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

    assert(emotion_attr_helper(emotion.emotion_matrix))

def test_emotion_flow(emotion: syneuro.Emotion):

    prev_dict = emotion.emotion_matrix
    output = emotion.emotion("This is a test.", "openai/gpt-oss-120b")
    assert(emotion_attr_helper({"prev": prev_dict, "new": output}))

def test_groq_api(emotion: syneuro.Emotion):

    assert (emotion.extract_affective_state("This is a test.", "openai/gpt-oss-120b") != None)