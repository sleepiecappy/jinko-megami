# Jinkomegami

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


---
