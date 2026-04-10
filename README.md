# Asteroids Demo: An Autonomous Vector Simulation

A high-fidelity, self-running simulation of the classic *Asteroids* arcade experience, rendered with a crisp, retro vector-graphics aesthetic. This project showcases an autonomous agent-driven environment where the ship intelligently navigates, targets, and survives an ever-changing field of asteroids and UFOs.

## 🤖 The Genesis: Purely Local Intelligence

This project is a testament to the frontiers of local-first AI development. It was conceived, architected, and implemented entirely **offline** by **Gemma 4 (26B)**. 

Every line of Python code, every mathematical derivation for the physics engine, and even the very prose comprising this `README.md` were generated without a single byte of data leaving the local machine. The development workflow utilized **Ollama** to orchestr 
the **Codex CLI**, enabling a sophisticated agentic loop on a **MacBook Pro powered by the M1 Max chip**. This project stands as a demonstration of how complex, structured software can be engineered in a completely air-gapped, private, and autonomous environment.

## ✨ Key Features

- **Autonomous AI**: The ship does not merely drift; it actively tracks threats, calculates intercept trajectories, and engages targets with high-frequency, strategic shooting patterns.
- **Vector Graphics Aesthetic**: Eschewing modern fills and heavy textures, the simulation utilizes a clean, "wireframe" style—white outlines on a deep black canvas—reminiscent of classic vector arcade monitors.
- **Procedural Complexity**: Asteroids split into smaller fragments upon impact, and the environment dynamically spawns UFOs (saucers) to maintain constant tension.
- **Physics-Driven Simulation**: Implements momentum, friction, and screen-wrapping mechanics for all entities, creating the signature "infinite loop" gameplay feel.
- **Self-Sustaining Loop**: The simulation is designed to run indefinitely. Should the ship be destroyed, it respawns and re-enters the fray, ensuring a continuous, hands-free viewing experience.

## 🛠️ Tech Stack

- **Python**: The core programming language.
- **Pygame**: The engine driving the 2D rendering, collision detection, and event loop.
- **uv**: Utilized for lightning-fast dependency management and execution.

## 🚀 Getting Started

### Prerequisites

Ensure you have `python` and `uv` installed on your system.

### Installation & Execution

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd asteroids_demo
   ```

2. **Run the simulation**:
   Using `uv` ensures all dependencies (like `pygame`) are handled automatically.
   ```bash
   uv run run_demo.py
   ```

## 📂 Project Structure

The project is organized into a modular package to ensure clarity and ease of maintenance:

- `asteroids_demo/main.py`: The orchestration layer; manages the simulation loop and entity lifecycle.
- `asteroids_demo/ship.py`: Defines the autonomous ship, its AI logic, and movement physics.
- `asteroids_demo/asteroid.py`: Handles procedural generation and fragmentation logic.
- `asteroids_demo/bullet.py`: Maintains the projectile physics and screen-wrapping.
- `asteroids_demo/saucer.py`: Controls the behavior of the periodic UFO threats.

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
