## 📖 Overview

Syneuro is a Neuro-Symbolic Affective-Computing Framework designed to simulate complex emotions via Python
## Architecture

* **`SALNetwork` (Salience):** The core router. It actively monitors incoming telemetry and decides whether the emotion should be in a resting state or active.
* **`CENetwork` (Central Executive):** Handles high-level reasoning, complex problem solving, tool execution, and goal-directed behavior influenced by emotion.
* **`LIMNetwork` (Limbic):** The affective state machine powered by a quantum-inspired expressions. Responsible for the internal mood, emotional responses, and assigns emotional weight to memory formation randomness.

## Diagram
```mermaid
flowchart TD

subgraph group_entry["User interaction"]
  node_app["Interactive app<br/>[app.py]"]
end

subgraph group_control["Brain orchestration"]
  node_brain["Brain controller<br/>[brain.py]"]
  node_network_map["Network registry<br/>[network.py]"]
end

subgraph group_networks["Cognitive networks"]
  node_sal["Salience network<br/>[sal.py]"]
  node_rag["Context and attention<br/>[sal.py]"]
  node_cen["Executive network<br/>[cen.py]"]
  node_lim["Limbic network<br/>[lim.py]"]
end

subgraph group_memory["Memory and transport"]
  node_memory["Memory allocation<br/>[memory.py]"]
  node_middleware[("Neo4j middleware<br/>[middleware.py]")]
  node_synapse["Interaction cache<br/>[synapse.py]"]
  node_cache_types["Cache data types"]
end

node_user(("User"))
node_groq["Groq API"]

node_user -->|"enters text"| node_app
node_app -->|"creates controller"| node_brain
node_app -->|"sends sensory data"| node_brain
node_brain -->|"builds modules"| node_network_map
node_brain -->|"dispatches pathway"| node_lim
node_brain -->|"dispatches pathway"| node_cen
node_brain -->|"dispatches pathway"| node_sal
node_lim -->|"pushes attention"| node_cen
node_sal -->|"manages context"| node_rag
node_lim -->|"extracts affect"| node_groq
node_lim -->|"starts allocation"| node_memory
node_memory -->|"sets memory payload"| node_middleware
node_synapse -->|"uses cache types"| node_cache_types

click node_app "https://github.com/ajlrza/syneuro/blob/main/app.py"
click node_brain "https://github.com/ajlrza/syneuro/blob/main/src/inference/brain.py"
click node_network_map "https://github.com/ajlrza/syneuro/blob/main/src/inference/network.py"
click node_sal "https://github.com/ajlrza/syneuro/blob/main/src/inference/networks/sal_module/sal.py"
click node_rag "https://github.com/ajlrza/syneuro/blob/main/src/inference/networks/sal_module/sal.py"
click node_cen "https://github.com/ajlrza/syneuro/blob/main/src/inference/networks/cen_module/cen.py"
click node_lim "https://github.com/ajlrza/syneuro/blob/main/src/inference/networks/lim_module/lim.py"
click node_memory "https://github.com/ajlrza/syneuro/blob/main/src/transport/memory.py"
click node_middleware "https://github.com/ajlrza/syneuro/blob/main/src/transport/middleware.py"
click node_synapse "https://github.com/ajlrza/syneuro/blob/main/src/transport/synapse.py"
click node_cache_types "https://github.com/ajlrza/syneuro/blob/main/src/transport/memory_dataclasses.py"

classDef toneNeutral fill:#f8fafc,stroke:#334155,stroke-width:1.5px,color:#0f172a
classDef toneBlue fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#172554
classDef toneAmber fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#78350f
classDef toneMint fill:#dcfce7,stroke:#16a34a,stroke-width:1.5px,color:#14532d
classDef toneRose fill:#ffe4e6,stroke:#e11d48,stroke-width:1.5px,color:#881337
classDef toneIndigo fill:#e0e7ff,stroke:#4f46e5,stroke-width:1.5px,color:#312e81
classDef toneTeal fill:#ccfbf1,stroke:#0f766e,stroke-width:1.5px,color:#134e4a
class node_app,node_user toneBlue
class node_brain,node_network_map toneAmber
class node_sal,node_rag,node_cen,node_lim,node_groq toneMint
class node_memory,node_middleware,node_synapse,node_cache_types toneRose
```

