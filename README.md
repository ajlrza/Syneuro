## Syneuro

---

<img width="1376" height="768" alt="image" src="https://github.com/user-attachments/assets/eeb6db94-58a9-4584-87ec-4093eac0de11" />

---

# Syneuro: Dev Workflow Guide

Syneuro is a lightweight emotion layer you can add on top of your AI chatbot applications.
It uses LLM-as-judge mechanism, where the LLM itself reasons around the emotions, though, it is Groq-based.
A Groq API key is needed, unless the code is modified to take any other API keys and endpoints.

This guide outlines developer workflow

## Prerequisites

Before using Syneuro, ensure your environment meets the following requirements at [requirements.txt](https://github.com/ajlrza/Syneuro/requirements.txt)
If prerequisites are not yet installed or are outdated, follow the steps below

## Installation

You can install the `Syneuro` package directly from the Git repository using pip.

```bash
pip install git+https://github.com/ajlrza/Syneuro.git
```

```bash
pip install -r requirements.txt
```

# Syneuro Example Usage 
```python
import os
from Syneuro import syneuro

text = "This is a text sample."
emotion = syneuro.Emotion(os.environ.get("API_KEY"))
processed_emotion = emotion.process(text_str=text, oai_compatible_model="llama-3.3-70b-versatile")
```
> [!NOTE]
> **Syneuro Usage:** Syneuro offers the emotion class and can be used wherever, as long as the text strings go through the ```.process()``` method along with the Groq-compatible model names.

# Sample Emotion Output
```python
{
  "x": {
    "positive": {
      "name": "Surprise",
      "value": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "negative": {
      "name": "Fear",
      "value": -0.4755282552719116,
      "min": 0.0,
      "max": 1.0
    }
  },
  "y": {
    "positive": {
      "name": "Zeal",
      "value": 0.34549150466918945,
      "min": 0.0,
      "max": 1.0
    },
    "negative": {
      "name": "Calm",
      "value": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "mixed_negative": {
      "name": "Angry",
      "value": 0.0,
      "min": 0.0,
      "max": 1.0
    }
  },
  "z": {
    "positive": {
      "name": "Happy",
      "value": 0.8090169906616211,
      "min": 0.0,
      "max": 1.0
    },
    "moderate_negative": {
      "name": "Sad",
      "value": 0.0,
      "min": 0.0,
      "max": 1.0
    },
    "extreme_negative": {
      "name": "Depressed",
      "value": 0.0,
      "min": 0.0,
      "max": 1.0
    }
  }
}
```

