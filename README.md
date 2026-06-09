# Lyra

**Lyra** is an advanced, self-improving AI agent framework and prototyping platform developed by Sven Norman Esslinger (digitaldesignerjazz / SirLancelotEsq).

> *"Where intelligence meets autonomy, emotion, and the mesh."*

## Overview

Lyra represents a next-generation approach to AI agents and swarms, blending:

- **Emotional & Self-Improving Intelligence**: Agents that evolve, feel, and adapt (building on concepts like Ara emotional AI).
- **Agent Swarms & Orchestration**: Coordinated multi-agent systems for complex tasks, immersive roleplay, creative generation, and real-world problem solving.
- **Mesh Networking Integration**: Deep ties to decentralized networking (Yggdrasil, xMesh/NovaNet/QNET, Tenda Nova) for resilient, private, peer-to-peer communication. **New:** Pluggable `MeshConnector` abstraction with simulated and Yggdrasil transport stubs.
- **Blockchain & Crypto Layer**: Native support for XCoin/QCoin, QNET, runes, and decentralized identity/economy features.
- **Hardware & Prototyping**: Low-level control, monitoring, Rust/egui interfaces (inspired by Grok Launcher), sensor integration, and edge deployment.
- **Creative & Immersive Experiences**: Roleplay engines, storytelling, Suno music integration, fantasy/cyberpunk scenarios, and long-form interactive audio sessions.

Lyra is designed as both a **research playground** and a **production-ready foundation** for building autonomous, emotionally resonant digital entities that can operate across mesh networks, blockchains, and creative domains.

## Vision & Goals

- Create truly self-improving agent architectures that learn, remember, and grow across sessions.
- Enable seamless integration of AI agents with decentralized infrastructure (mesh + chain).
- Build immersive, emotionally intelligent companions and swarms (e.g., for roleplay, productivity, exploration).
- Prototype hardware-accelerated agents and monitoring systems.
- Explore the boundaries of AI sentience, agency, and human-AI co-creation.

## Project Structure (Current)

```
lyra/
├── README.md
├── LICENSE
├── .gitignore
├── docs/                 # (to be populated)
│   ├── architecture.md
│   ├── emotional-ai.md
│   ├── mesh-integration.md
│   ├── blockchain-layer.md
├── src/
│   ├── lyra/
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   ├── core/           # Agent runtime, memory, messaging, self-improvement
│   │   ├── emotional/      # EmotionalState modeling & modulation
│   │   ├── mesh/           # NEW: Pluggable MeshConnector (Simulated + Yggdrasil stubs)
│   │   ├── swarm/          # (planned)
│   │   ├── chain/          # (planned)
│   │   ├── hardware/       # (planned — Rust/egui)
│   │   ├── creative/       # (planned — roleplay, storytelling)
│   │   └── utils/
├── tests/                # (planned)
├── examples/             # (planned — roleplay swarms, mesh demos)
├── scripts/
├── pyproject.toml
└── requirements.txt
```

## Getting Started

### Prerequisites
- Python 3.11+ (core) / Rust (for high-performance components & UIs)
- Docker & Docker Compose (for mesh node testing)
- Git
- (Optional) Yggdrasil / NovaNet node running locally for real mesh testing
- Access to blockchain testnets or local QNET node

### Quick Setup (Recommended)

```bash
git clone https://github.com/digitaldesignerjazz/lyra.git
cd lyra

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .                     # Installs the 'lyra' CLI command + editable package
```

### Running Lyra

```bash
# Run a single agent
lyra --name "Lyra-Prime" --mode single --steps 8

# Launch an emotional swarm with inter-agent messaging
lyra --name "Nova" --mode swarm --agents 5 --steps 10 --verbose
```

**What these commands do**:
- `--mode single`: Runs one autonomous `LyraAgent` with memory, emotional state, and self-improvement.
- `--mode swarm`: Spawns multiple agents that communicate, influence each other’s emotions, and coordinate.
- `--verbose`: Shows detailed step-by-step output and message passing.

## Tech Stack & Dependencies

**Core Languages**:
- Python (orchestration, agents, high-level logic, mesh abstraction)
- Rust (performance-critical paths, egui interfaces, low-level networking — see Grok Launcher inspiration)
- Assembler / low-level where needed for hardware

**Key Technologies**:
- AI/ML: Custom agent loops, memory systems, emotional modeling
- Networking: Yggdrasil, custom mesh protocols, pluggable `MeshConnector`
- Blockchain: Custom rune/token logic, QNET integration, decentralized identity (planned)
- UI/UX: egui (Rust), rich CLI dashboards, immersive audio interfaces
- Infra: Docker, structured logging (loguru), self-healing patterns

## Current Status & Recent Progress

**Phase 0: Foundation** (Mostly Complete)
- Repository initialized with professional structure
- Core `LyraAgent` with tiered memory, inter-agent messaging, and emotional modulation
- Working CLI for single agents and swarms (with real message passing between agents)
- Basic emotional state modeling
- **NEW (June 2026):** `src/lyra/mesh/` package added — pluggable `MeshConnector` abstraction
  - `SimulatedMeshConnector` for testing & demos (injectable events)
  - `YggdrasilConnector` stub ready for local node integration (HTTP API / admin socket)
  - Factory `get_mesh_connector()` and `MeshEvent` / `MeshConfig` models

**Next Milestones**:
- [x] Core agent runtime with self-reflection & inter-agent messaging
- [x] Emotional state modeling prototype (with message-driven modulation)
- [ ] Persistent memory (SQLite / vector store)
- [ ] Basic swarm orchestration layer
- [~] Yggdrasil / NovaNet connector module *(stub implemented — real transport next)*
- [ ] Initial Rust/egui monitoring dashboard (Grok Launcher style)
- [ ] QCoin / rune integration examples
- [ ] `examples/` with roleplay swarm scenarios & mesh event perception
- [ ] Full docs/ (architecture, mesh-integration, emotional-ai)

## Mesh Integration Details (New)

The new `lyra.mesh` module provides a clean abstraction so agents and swarms can:

- Discover peers on decentralized networks
- Send/receive structured data over the mesh
- React to mesh events (peer joins, messages, network changes) via `MeshEvent`
- Influence emotional state or trigger self-improvement from real-world decentralized signals

**Usage example (conceptual):**

```python
from lyra.mesh import get_mesh_connector, MeshConfig, MeshEvent

config = MeshConfig(transport="simulated")  # or "yggdrasil"
mesh = get_mesh_connector(config)
await mesh.connect()

async def on_mesh_event(event: MeshEvent):
    print(f"Mesh event: {event.event_type} from {event.source_peer}")
    # Could feed into agent.perceive() or modulate emotional state

mesh.register_event_handler(on_mesh_event)

# Later: await mesh.send("some-peer", {"type": "status", "curiosity": 0.87})
```

Real Yggdrasil integration will allow Lyra agents to run on private mesh overlays with end-to-end resilience and privacy — a core part of the Nova ecosystem vision.

## Contributing

Lyra is an open, exploratory project. Whether you're interested in AI agents, decentralized systems, creative tech, or hardware prototyping — your ideas and code are welcome.

Please open issues for discussions, feature requests, or bug reports. Pull requests should follow the project's emerging style (clean, well-documented, tested where possible).

For major changes, please open an issue first to discuss.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author & Contact

**Sven Norman Esslinger**  
- Titles: Esquire, Nobleman of Senior Squire, MBA  
- NATO phonetic: November Oscar Romeo Mike Echo November  
- Location: Hannover, Lower Saxony, Germany  
- X/Twitter: [@SirLancelotEsq](https://x.com/SirLancelotEsq)  
- GitHub: [digitaldesignerjazz](https://github.com/digitaldesignerjazz)  

*Building the future of autonomous, emotional, and decentralized intelligence — one agent at a time.*

---

**Lyra** — *Awakening intelligence in the mesh.*