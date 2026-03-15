"""Multi-provider AI agent using LangChain for orchestration."""

import os
from typing import Optional, List, Dict, Any
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

from ai_agent.providers import (
    OpenRouterProvider,
    MinimaxProvider,
    BaseProvider,
    create_provider,
)


class MultiProviderAgent:
    """AI agent that can switch between multiple LLM providers."""
    
    def __init__(
        self,
        default_provider: str = "openrouter",
        model: Optional[str] = None,
        temperature: float = 0.7,
    ):
        """
        Initialize multi-provider agent.
        
        Args:
            default_provider: "openrouter" or "minimax"
            model: Model name (provider-specific)
            temperature: Sampling temperature
        """
        self.default_provider = default_provider
        self.temperature = temperature
        self.model = model
        
        # Initialize providers
        self.providers: Dict[str, BaseProvider] = {}
        self._init_providers()
        
        # Current active provider
        self.active_provider = self.providers.get(default_provider)
        if not self.active_provider:
            raise ValueError(f"Failed to initialize provider: {default_provider}")
        
        # LangChain setup
        self._setup_langchain()
    
    def _init_providers(self):
        """Initialize available providers."""
        try:
            self.providers["openrouter"] = OpenRouterProvider()
        except ValueError:
            print("Warning: OpenRouter not configured (OPENROUTER_API_KEY missing)")
        
        try:
            self.providers["minimax"] = MinimaxProvider()
        except ValueError:
            print("Warning: Minimax not configured (MINIMAX_API_KEY or MINIMAX_GROUP_ID missing)")
    
    def _setup_langchain(self):
        """Setup LangChain agent with tools."""
        # Create a LangChain-compatible LLM wrapper
        # For OpenRouter, we'll use ChatOpenAI with custom base URL
        try:
            if "openrouter" in self.providers:
                self.llm = ChatOpenAI(
                    model=self.model or "openai/gpt-4-turbo",
                    temperature=self.temperature,
                    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
                    openai_api_base="https://openrouter.ai/api/v1",
                    default_headers={
                        "HTTP-Referer": "https://github.com/NVlabs/GR00T-WholeBodyControl",
                        "X-Title": "GR00T Robot Control",
                    },
                )
            else:
                # Fallback to a simple wrapper if OpenRouter not available
                self.llm = None
        except Exception as e:
            print(f"Warning: LangChain setup failed: {e}")
            self.llm = None
        
        # Define tools for the agent
        self.tools = [
            Tool(
                name="switch_provider",
                func=self._switch_provider_tool,
                description="Switch between AI providers (openrouter, minimax)",
            ),
            Tool(
                name="get_provider_info",
                func=self._get_provider_info,
                description="Get information about available providers",
            ),
        ]
        
        # Memory for conversation
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )
    
    def _switch_provider_tool(self, provider_name: str) -> str:
        """Tool function to switch providers."""
        provider_name = provider_name.lower().strip()
        if provider_name in self.providers:
            self.active_provider = self.providers[provider_name]
            self.default_provider = provider_name
            return f"Switched to provider: {provider_name}"
        else:
            available = ", ".join(self.providers.keys())
            return f"Provider '{provider_name}' not available. Available: {available}"
    
    def _get_provider_info(self, _: str = "") -> str:
        """Get information about available providers."""
        info = f"Active provider: {self.default_provider}\n"
        info += f"Available providers: {', '.join(self.providers.keys())}\n"
        return info
    
    def chat(
        self,
        message: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        use_langchain: bool = False,
        **kwargs
    ) -> str:
        """
        Send a chat message and get response.
        
        Args:
            message: User message
            provider: Provider to use (overrides default)
            model: Model to use (provider-specific)
            use_langchain: Use LangChain agent framework
            **kwargs: Additional provider-specific parameters
        
        Returns:
            AI response string
        """
        # Determine which provider to use
        if provider:
            if provider not in self.providers:
                raise ValueError(f"Provider '{provider}' not available")
            active = self.providers[provider]
        else:
            active = self.active_provider
        
        # Use LangChain if requested and available
        if use_langchain and self.llm:
            return self._chat_with_langchain(message, **kwargs)
        
        # Direct provider call
        return active.chat(message, model=model, temperature=self.temperature, **kwargs)
    
    def _chat_with_langchain(self, message: str, **kwargs) -> str:
        """Chat using LangChain agent framework."""
        if not self.llm:
            raise ValueError("LangChain LLM not initialized")
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant for robot control and teleoperation. "
                      "You can help users understand robot commands, troubleshoot issues, "
                      "and provide guidance on using the GR00T system."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create agent
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
        )
        
        result = agent_executor.invoke({"input": message})
        return result["output"]
    
    def stream_chat(
        self,
        message: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ):
        """Stream chat responses."""
        if provider:
            if provider not in self.providers:
                raise ValueError(f"Provider '{provider}' not available")
            active = self.providers[provider]
        else:
            active = self.active_provider
        
        yield from active.stream_chat(message, model=model, **kwargs)
    
    def switch_provider(self, provider_name: str) -> bool:
        """Switch the default provider."""
        provider_name = provider_name.lower()
        if provider_name in self.providers:
            self.active_provider = self.providers[provider_name]
            self.default_provider = provider_name
            return True
        return False
    
    def list_providers(self) -> List[str]:
        """List available providers."""
        return list(self.providers.keys())


# Convenience function
def create_agent(provider: str = "openrouter", **kwargs) -> MultiProviderAgent:
    """Create a multi-provider agent instance."""
    return MultiProviderAgent(default_provider=provider, **kwargs)
