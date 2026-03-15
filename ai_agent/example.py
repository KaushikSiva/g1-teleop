"""Example usage of the AI agent system."""

import os
from ai_agent.agent import MultiProviderAgent, create_agent


def example_basic_chat():
    """Basic chat example."""
    print("=== Basic Chat Example ===")
    
    # Create agent (defaults to OpenRouter)
    agent = create_agent(provider="openrouter")
    
    # Simple chat
    response = agent.chat("What is the Unitree G1 robot?")
    print(f"Response: {response}\n")


def example_provider_switching():
    """Example of switching between providers."""
    print("=== Provider Switching Example ===")
    
    agent = create_agent(provider="openrouter")
    
    # Chat with OpenRouter
    response1 = agent.chat("Hello from OpenRouter!", provider="openrouter")
    print(f"OpenRouter: {response1[:100]}...\n")
    
    # Switch to Minimax
    if "minimax" in agent.list_providers():
        agent.switch_provider("minimax")
        response2 = agent.chat("Hello from Minimax!", provider="minimax")
        print(f"Minimax: {response2[:100]}...\n")


def example_streaming():
    """Example of streaming responses."""
    print("=== Streaming Example ===")
    
    agent = create_agent(provider="openrouter")
    
    print("Streaming response:")
    for chunk in agent.stream_chat("Explain robot teleoperation in 3 sentences."):
        print(chunk, end="", flush=True)
    print("\n")


def example_langchain_agent():
    """Example using LangChain agent framework."""
    print("=== LangChain Agent Example ===")
    
    agent = create_agent(provider="openrouter")
    
    # Use LangChain agent with tools
    response = agent.chat(
        "Switch to minimax provider and then tell me about robot control.",
        use_langchain=True
    )
    print(f"LangChain Agent: {response}\n")


def example_robot_control_assistant():
    """Example of using agent for robot control assistance."""
    print("=== Robot Control Assistant Example ===")
    
    agent = create_agent(provider="openrouter")
    
    questions = [
        "How do I start the robot in simulation?",
        "What are the Quest 3 controller bindings?",
        "How do I switch between locomotion modes?",
    ]
    
    for question in questions:
        response = agent.chat(question)
        print(f"Q: {question}")
        print(f"A: {response[:200]}...\n")


if __name__ == "__main__":
    # Check if API keys are set
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Warning: OPENROUTER_API_KEY not set. Some examples may fail.")
    
    if not os.getenv("MINIMAX_API_KEY"):
        print("Warning: MINIMAX_API_KEY not set. Minimax examples will be skipped.")
    
    # Run examples
    try:
        example_basic_chat()
    except Exception as e:
        print(f"Example failed: {e}")
    
    try:
        example_provider_switching()
    except Exception as e:
        print(f"Example failed: {e}")
    
    try:
        example_streaming()
    except Exception as e:
        print(f"Example failed: {e}")
    
    try:
        example_langchain_agent()
    except Exception as e:
        print(f"Example failed: {e}")
    
    try:
        example_robot_control_assistant()
    except Exception as e:
        print(f"Example failed: {e}")
