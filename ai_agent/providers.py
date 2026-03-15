"""LLM Provider implementations for OpenRouter and Minimax."""

import os
import requests
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()


class BaseProvider(ABC):
    """Base class for LLM providers."""
    
    @abstractmethod
    def chat(self, message: str, model: Optional[str] = None, **kwargs) -> str:
        """Send a chat message and get response."""
        pass
    
    @abstractmethod
    def stream_chat(self, message: str, model: Optional[str] = None, **kwargs):
        """Stream chat responses."""
        pass


class OpenRouterProvider(BaseProvider):
    """OpenRouter API provider - unified gateway to 100+ LLM models."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment")
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_model = "openai/gpt-4-turbo"
    
    def chat(
        self,
        message: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """Send chat message via OpenRouter."""
        model = model or self.default_model
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/NVlabs/GR00T-WholeBodyControl",
            "X-Title": "GR00T Robot Control",
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": message}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    
    def stream_chat(self, message: str, model: Optional[str] = None, **kwargs):
        """Stream chat responses from OpenRouter."""
        model = model or self.default_model
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/NVlabs/GR00T-WholeBodyControl",
            "X-Title": "GR00T Robot Control",
        }
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": message}
            ],
            "stream": True,
            **kwargs
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode("utf-8")
                if line_str.startswith("data: "):
                    data_str = line_str[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        import json
                        data = json.loads(data_str)
                        if "choices" in data and len(data["choices"]) > 0:
                            delta = data["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                    except json.JSONDecodeError:
                        continue


class MinimaxProvider(BaseProvider):
    """Minimax AI provider - Chinese LLM with strong reasoning capabilities."""
    
    def __init__(self, api_key: Optional[str] = None, group_id: Optional[str] = None):
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY")
        self.group_id = group_id or os.getenv("MINIMAX_GROUP_ID")
        
        if not self.api_key:
            raise ValueError("MINIMAX_API_KEY not found in environment")
        if not self.group_id:
            raise ValueError("MINIMAX_GROUP_ID not found in environment")
        
        self.base_url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
        self.default_model = "abab6.5s-chat"
    
    def chat(
        self,
        message: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Send chat message via Minimax."""
        model = model or self.default_model
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "temperature": temperature,
            "bot_setting": [
                {
                    "bot_name": "Assistant",
                    "content": "You are a helpful AI assistant for robot control and teleoperation."
                }
            ],
            "group_id": self.group_id,
            **kwargs
        }
        
        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        elif "reply" in result:
            return result["reply"]
        else:
            raise ValueError(f"Unexpected Minimax response format: {result}")
    
    def stream_chat(self, message: str, model: Optional[str] = None, **kwargs):
        """Stream chat responses from Minimax."""
        model = model or self.default_model
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "stream": True,
            "bot_setting": [
                {
                    "bot_name": "Assistant",
                    "content": "You are a helpful AI assistant for robot control and teleoperation."
                }
            ],
            "group_id": self.group_id,
            **kwargs
        }
        
        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode("utf-8")
                if line_str.startswith("data: "):
                    data_str = line_str[6:]
                    try:
                        import json
                        data = json.loads(data_str)
                        if "choices" in data and len(data["choices"]) > 0:
                            delta = data["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                    except (json.JSONDecodeError, KeyError):
                        continue


def list_available_providers() -> List[str]:
    """List available provider names."""
    return ["openrouter", "minimax"]


def create_provider(provider_name: str, **kwargs) -> BaseProvider:
    """Factory function to create provider instances."""
    provider_name = provider_name.lower()
    
    if provider_name == "openrouter":
        return OpenRouterProvider(**kwargs)
    elif provider_name == "minimax":
        return MinimaxProvider(**kwargs)
    else:
        raise ValueError(f"Unknown provider: {provider_name}. Available: {list_available_providers()}")
