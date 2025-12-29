"""
LLM API clients for FREE providers only
Supports: Ollama (local), Groq, Google Gemini, HuggingFace
"""

import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class BaseLLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    def generate(self, system_prompt: str, messages: List[Dict], temperature: float = 0.7) -> str:
        """Generate a response from the LLM"""
        pass


class OllamaClient(BaseLLMClient):
    """Ollama local LLM client - 100% FREE, uses NVIDIA GPU if available"""
    
    def __init__(self, model: str = "llama3.2", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        # Import timeout from config, default to 300 seconds
        try:
            from config import OLLAMA_TIMEOUT
            self.timeout = OLLAMA_TIMEOUT
        except ImportError:
            self.timeout = 300
    
    def generate(self, system_prompt: str, messages: List[Dict], temperature: float = 0.7) -> str:
        import requests
        
        formatted_messages = [{"role": "system", "content": system_prompt}]
        formatted_messages.extend(messages)
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": formatted_messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_gpu": 99  # Use all available GPU layers
                    }
                },
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()["message"]["content"]
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.base_url}\n"
                "Make sure Ollama is running: https://ollama.com/download"
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(
                f"Ollama timed out after {self.timeout}s. Model may still be loading.\n"
                "Try running 'ollama run {self.model}' first to warm up the model."
            )


class GroqClient(BaseLLMClient):
    """Groq API client - FREE tier available"""
    
    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant"):
        self.api_key = api_key
        self.model = model
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            from groq import Groq
            self._client = Groq(api_key=self.api_key)
        return self._client
    
    def generate(self, system_prompt: str, messages: List[Dict], temperature: float = 0.7) -> str:
        formatted_messages = [{"role": "system", "content": system_prompt}]
        formatted_messages.extend(messages)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=formatted_messages,
            temperature=temperature,
            max_tokens=500
        )
        return response.choices[0].message.content


class GoogleClient(BaseLLMClient):
    """Google Gemini API client - FREE tier available"""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model = model
        self._client = None
    
    @property
    def client(self):
        if self._client is None:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self._client = genai.GenerativeModel(
                self.model,
                generation_config={"max_output_tokens": 500}
            )
        return self._client
    
    def generate(self, system_prompt: str, messages: List[Dict], temperature: float = 0.7) -> str:
        # Format conversation for Gemini
        full_prompt = f"{system_prompt}\n\nConversation so far:\n"
        for msg in messages:
            role = "You" if msg["role"] == "assistant" else "Other"
            full_prompt += f"{role}: {msg['content']}\n"
        full_prompt += "\nYour response:"
        
        response = self.client.generate_content(
            full_prompt,
            generation_config={"temperature": temperature}
        )
        return response.text


class HuggingFaceClient(BaseLLMClient):
    """HuggingFace Inference API client - FREE tier available"""
    
    def __init__(self, api_key: str, model: str = "mistralai/Mistral-7B-Instruct-v0.3"):
        self.api_key = api_key
        self.model = model
        self.api_url = f"https://api-inference.huggingface.co/models/{model}"
    
    def generate(self, system_prompt: str, messages: List[Dict], temperature: float = 0.7) -> str:
        import requests
        
        # Format as instruction
        prompt = f"<s>[INST] {system_prompt}\n\n"
        for msg in messages:
            if msg["role"] == "user":
                prompt += f"{msg['content']}\n"
            else:
                prompt += f"[/INST] {msg['content']} </s><s>[INST] "
        prompt += "[/INST]"
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": temperature,
                "return_full_text": False
            }
        }
        
        response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "")
        return result.get("generated_text", "")


def create_client(provider: str, api_key: str = "", model: str = "") -> BaseLLMClient:
    """Factory function to create appropriate LLM client (FREE providers only)"""
    
    if provider == "ollama":
        return OllamaClient(model or "llama3.2")
    elif provider == "groq":
        return GroqClient(api_key, model or "llama-3.1-8b-instant")
    elif provider == "google":
        return GoogleClient(api_key, model or "gemini-1.5-flash")
    elif provider == "huggingface":
        return HuggingFaceClient(api_key, model or "mistralai/Mistral-7B-Instruct-v0.3")
    else:
        raise ValueError(f"Unknown provider: {provider}. Use: ollama, groq, google, huggingface")
