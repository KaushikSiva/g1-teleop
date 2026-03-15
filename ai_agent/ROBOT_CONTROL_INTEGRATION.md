# AI Agent for Robot Control - Use Cases

## What This Feature Does

The AI agent provides **intelligent assistance** for robot teleoperation and control using multiple LLM providers (OpenRouter, Minimax) orchestrated via LangChain.

## How It Relates to Robot Control

### 1. **Intelligent Command Interpretation**
Instead of memorizing keyboard shortcuts, users can ask in natural language:
- "How do I start the robot?"
- "What button stops the robot?"
- "How do I switch to VR 3PT mode?"

The AI understands the context and provides accurate answers based on the robot control system.

### 2. **Troubleshooting Assistant**
When things go wrong, the AI can help diagnose:
- "The robot isn't moving after I press Y"
- "Quest 3 can't connect to the server"
- "The robot falls when I press 9"

The AI can guide through debugging steps and common solutions.

### 3. **Natural Language to Robot Commands**
Future integration could translate natural language to robot actions:
- User: "Move the robot forward slowly"
- AI: Interprets and sends appropriate locomotion commands
- User: "Pick up the red can"
- AI: Coordinates arm movements and grasping

### 4. **Documentation and Learning**
The AI acts as an interactive manual:
- Explains control modes (IDLE, WALK, RUN)
- Describes Quest 3 controller bindings
- Guides through setup procedures
- Provides safety information

### 5. **Multi-Provider Flexibility**
- **OpenRouter**: Access to GPT-4, Claude, Llama for general reasoning
- **Minimax**: Strong Chinese language support and alternative reasoning
- **LangChain**: Enables tool use (could connect to robot APIs)

## Example Integration Scenarios

### Scenario 1: Voice-Controlled Robot
```python
from ai_agent.agent import MultiProviderAgent
import speech_recognition

agent = MultiProviderAgent()
recognizer = speech_recognition.Recognizer()

# User speaks: "Start the robot in walk mode"
voice_command = recognize_speech()
ai_response = agent.chat(f"Interpret this robot command: {voice_command}")

# AI responds with: "Press Y to start, then use A+B to switch to WALK mode"
# System executes the interpreted command
```

### Scenario 2: Intelligent Error Recovery
```python
# Robot encounters error
error_msg = "ZMQ connection timeout"

# Ask AI for solution
solution = agent.chat(
    f"Robot error: {error_msg}. "
    "What should I check? Provide step-by-step troubleshooting."
)

# AI provides: "1. Check if Terminal 2 (C++ deploy) is running..."
```

### Scenario 3: Adaptive Control Assistance
```python
# User asks for help during teleoperation
user_question = "How do I make the robot pick up the object?"

# AI provides contextual guidance
guidance = agent.chat(
    f"User is controlling Unitree G1 robot via Quest 3. "
    f"Question: {user_question}. "
    "Provide step-by-step instructions."
)

# AI responds with Quest 3-specific instructions:
# "1. Press X to enable VR 3PT mode
#  2. Move your hands to position robot arms
#  3. Press triggers to close grippers
#  4. Lift your hands to pick up object"
```

## Technical Architecture

```
User Query
    ↓
AI Agent (LangChain)
    ↓
┌─────────────┬─────────────┐
│ OpenRouter  │   Minimax    │
│ (GPT-4,    │  (Chinese    │
│  Claude)   │   LLM)       │
└─────────────┴─────────────┘
    ↓
Robot Control System
    ↓
Unitree G1 Robot
```

## Future Enhancements

1. **Direct Robot API Integration**: AI can directly call robot control functions
2. **Predictive Assistance**: AI predicts user intent and suggests actions
3. **Safety Monitoring**: AI watches for unsafe patterns and warns users
4. **Multi-Language Support**: Minimax enables Chinese/other language interfaces
5. **Learning from Demonstrations**: AI learns from user behavior patterns

## Current Status

✅ **Implemented:**
- Multi-provider LLM integration (OpenRouter, Minimax)
- LangChain agent framework
- Basic chat interface
- Provider switching

🚧 **Future Work:**
- Direct integration with robot control APIs
- Voice command interpretation
- Real-time safety monitoring
- Command translation layer

## Why This Matters

Traditional robot control requires:
- Memorizing keyboard shortcuts
- Reading documentation
- Understanding technical jargon
- Manual troubleshooting

With AI agent:
- Natural language interaction
- Context-aware assistance
- Intelligent error recovery
- Adaptive learning

This makes robot teleoperation **more accessible** and **safer** for users.
