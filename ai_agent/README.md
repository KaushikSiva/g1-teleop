# AI Agent Integration

Multi-provider LLM integration using OpenRouter, LangChain, and Minimax.

## Features

- **OpenRouter**: Unified API gateway for multiple LLM providers
- **LangChain**: Agent framework for chaining and tooling
- **Minimax**: Alternative LLM provider integration
- **Multi-provider support**: Switch between providers seamlessly

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export OPENROUTER_API_KEY="your-openrouter-key"
export MINIMAX_API_KEY="your-minimax-key"
export MINIMAX_GROUP_ID="your-group-id"
```

Or create a `.env` file:
```
OPENROUTER_API_KEY=your-key-here
MINIMAX_API_KEY=your-key-here
MINIMAX_GROUP_ID=your-group-id
```

## Usage

```python
from ai_agent.agent import MultiProviderAgent

agent = MultiProviderAgent()
response = agent.chat("Hello, how can you help with robot control?")
print(response)
```

## Providers

- **OpenRouter**: Access to 100+ models (GPT-4, Claude, Llama, etc.)
- **Minimax**: Chinese LLM provider with strong reasoning
- **LangChain**: Orchestration and tooling framework
