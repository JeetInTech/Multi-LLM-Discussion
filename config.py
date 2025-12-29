"""
Configuration for Multi-LLM Group Chat Discussion System
Uses FREE LLM providers only!
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# FREE LLM OPTIONS - API keys loaded from .env file
# =============================================================================

# Option 1: OLLAMA (Recommended - 100% Free, runs locally)
# Install: https://ollama.com/download
# Then run: ollama pull llama3.2
# No API key needed!

# Option 2: GROQ (Free tier - very fast cloud inference)
# Get free key: https://console.groq.com/keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Option 3: GOOGLE GEMINI (Free tier - 15 requests/minute)
# Get free key: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Option 4: HUGGINGFACE (Free inference API)
# Get free key: https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

# =============================================================================
# PROVIDER SELECTION
# =============================================================================
# Using "mixed" with DIFFERENT models for true diversity
LLM_PROVIDER = "mixed"

# =============================================================================
# 5 DIFFERENT LLMs - 3 Ollama (GPU) + 2 Groq = 5 unique models!
# =============================================================================
# Ollama will auto-detect NVIDIA GPU. Make sure CUDA drivers are installed.
MIXED_ASSIGNMENTS = {
    # Ollama models (3) - runs on your NVIDIA GPU
    "logical": {"provider": "ollama", "model": "llama3.2"},       # Meta Llama
    "skeptical": {"provider": "ollama", "model": "mistral"},      # Mistral AI
    "synthesizer": {"provider": "ollama", "model": "phi3"},       # Microsoft Phi
    
    # Groq models (2) - fast cloud inference  
    "creative": {"provider": "groq", "model": "llama-3.3-70b-versatile"},  # Large Llama
    "practical": {"provider": "groq", "model": "qwen/qwen3-32b"},          # Alibaba Qwen
}

# Fallback models (if using single provider mode)
MODELS = {
    "ollama": "llama3.2",
    "groq": "llama-3.1-8b-instant",
    "google": "gemini-1.5-flash",
    "huggingface": "mistralai/Mistral-7B-Instruct-v0.3"
}

# Ollama Settings (for local LLMs with NVIDIA GPU)
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_TIMEOUT = 180  # 3 minutes timeout for GPU model loading

# Conversation Settings
MAX_ROUNDS = 3  # Number of discussion rounds
ENABLE_SYNTHESIZER = True  # Include the 5th neutral participant

# Temperature settings for each persona (affects creativity/randomness)
PERSONA_TEMPERATURES = {
    "logical": 0.3,
    "creative": 0.8,
    "skeptical": 0.5,
    "practical": 0.4,
    "synthesizer": 0.3
}

# =============================================================================
# QUICK SETUP GUIDE
# =============================================================================
# 
# EASIEST: Use Ollama (100% free, local)
#   1. Download Ollama: https://ollama.com/download
#   2. Open terminal and run: ollama pull llama3.2
#   3. Run: python main.py "your topic"
#
# ALTERNATIVE: Use Groq (free cloud, very fast)
#   1. Get free API key: https://console.groq.com/keys
#   2. Set GROQ_API_KEY above
#   3. Set LLM_PROVIDER = "groq"
#   4. Run: python main.py "your topic"
#
