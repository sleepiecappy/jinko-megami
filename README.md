# jinkomegami

人工女神 - Environment-Aware Humanoid*

<small>*...more like a JSON interface so anyone can use their own character.</small>

This project aims to provide a foundation for what could become a digital companion. It features a decoupled system that uses real-time perception and AI-driven reasoning, allowing a digital character to understand and react to your environment.

## Core Concept

The system is designed around a modular "Sense → Perceive → Reason → Act" loop. This architecture ensures that each part can be replaced, upgraded, or customized independently.

- Sense: Sensors and Data Feeds

  This is the raw input from the physical world. It includes video streams from a camera, audio from a microphone, or even data from other APIs (like weather or notifications).

- Perceive: On-Device Interpretation

  This stage translates raw sensor data into meaningful information. A fast, on-device model processes the camera feed to identify objects ("person", "laptop") and transcribes raw audio into text ("Hello, how are you?"). The goal is low-latency, real-time understanding.

- Reason: Contextual Action Planning

  The perceived information (e.g., "Sees a person, hears 'Hello'") is combined with the character's predefined personality and sent to an AI. The AI's job is to determine the most appropriate emotional state and action for the character to take.

- Act: Sensory Representation of Action

  This is the final output you see and hear. The action command from the Reasoning stage is sent to a 3D engine or other frontend, which executes the visual animation and plays the audible response.



## Configuration and Setup

1. This project is managed by `uv`, make sure you have it installed.
It can be found at https://docs.astral.sh/uv/getting-started/installation/

2. With `uv` available, clone this repository if not already and `cd` into the directory.

3. Install the required python version using `uv`: 

```shell 
uv python install 3.13
```

4. Create a new virtual environment if this is your first time setting it up:

```shell
uv venv --managed-python
```

more info can be found at their [docs](https://docs.astral.sh/uv/reference/cli/#uv-venv)

5. Install dependencies by running:
```shell
uv sync
```

Ruff is used to lint the project, to run it use:
```shell
uv run ruff check
```

other commands that are interesting to run during development are:
 - `analyze`:  Run analysis over Python source code
 - `format`: Run the Ruff formatter

 More information can be found at https://docs.astral.sh/ruff/