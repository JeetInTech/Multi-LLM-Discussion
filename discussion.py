"""
Core discussion engine for Multi-LLM Group Chat
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from personas import PERSONAS, RESPONSE_ORDER, RESPONSE_ORDER_WITH_SYNTH
from llm_clients import BaseLLMClient, create_client
import config

@dataclass
class Message:
    """Represents a single message in the chat"""
    persona_key: str
    persona_name: str
    emoji: str
    content: str
    round_num: int

@dataclass
class Discussion:
    """Manages the entire discussion flow"""
    user_input: str
    messages: List[Message] = field(default_factory=list)
    clients: Dict[str, BaseLLMClient] = field(default_factory=dict)
    
    def __post_init__(self):
        self._setup_clients()
    
    def _setup_clients(self):
        """Initialize LLM clients based on configuration"""
        if config.LLM_PROVIDER == "mixed":
            # Use different providers AND models for each persona
            for persona_key, assignment in config.MIXED_ASSIGNMENTS.items():
                # Handle new format: {"provider": "...", "model": "..."}
                if isinstance(assignment, dict):
                    provider = assignment["provider"]
                    model = assignment.get("model", config.MODELS.get(provider, ""))
                else:
                    # Fallback for old format: just provider string
                    provider = assignment
                    model = config.MODELS.get(provider, "")
                
                api_key = self._get_api_key(provider)
                self.clients[persona_key] = create_client(provider, api_key, model)
        else:
            # Use same provider for all personas
            provider = config.LLM_PROVIDER
            api_key = self._get_api_key(provider)
            model = config.MODELS.get(provider, "")
            client = create_client(provider, api_key, model)
            
            order = RESPONSE_ORDER_WITH_SYNTH if config.ENABLE_SYNTHESIZER else RESPONSE_ORDER
            for persona_key in order:
                self.clients[persona_key] = client
    
    def _get_api_key(self, provider: str) -> str:
        """Get API key for a provider (all FREE providers)"""
        keys = {
            "groq": config.GROQ_API_KEY,
            "google": config.GOOGLE_API_KEY,
            "huggingface": config.HUGGINGFACE_API_KEY,
            "ollama": ""  # No API key needed
        }
        return keys.get(provider, "")
    
    def _build_chat_history(self, for_persona: str) -> List[Dict]:
        """Build chat history for LLM context"""
        history = []
        
        # Add user input first
        history.append({
            "role": "user",
            "content": f"[User] {self.user_input}"
        })
        
        # Add all previous messages
        for msg in self.messages:
            # Messages from this persona are "assistant", others are "user" (context)
            role = "assistant" if msg.persona_key == for_persona else "user"
            content = f"[{msg.persona_name}] {msg.content}"
            history.append({"role": role, "content": content})
        
        # Add prompt for next response
        persona = PERSONAS[for_persona]
        history.append({
            "role": "user", 
            "content": f"Now respond naturally as yourself ({persona['name']}) to this ongoing discussion. Keep it conversational and chat-like."
        })
        
        return history
    
    def _generate_response(self, persona_key: str, round_num: int) -> Message:
        """Generate a single response from a persona"""
        persona = PERSONAS[persona_key]
        client = self.clients[persona_key]
        temperature = config.PERSONA_TEMPERATURES.get(persona_key, 0.5)
        
        history = self._build_chat_history(persona_key)
        
        content = client.generate(
            system_prompt=persona["system_prompt"],
            messages=history,
            temperature=temperature
        )
        
        return Message(
            persona_key=persona_key,
            persona_name=persona["name"],
            emoji=persona["emoji"],
            content=content.strip(),
            round_num=round_num
        )
    
    def run_discussion(self, rounds: int = None) -> List[Message]:
        """Run the full discussion"""
        rounds = rounds or config.MAX_ROUNDS
        order = RESPONSE_ORDER_WITH_SYNTH if config.ENABLE_SYNTHESIZER else RESPONSE_ORDER
        
        for round_num in range(1, rounds + 1):
            for persona_key in order:
                # Synthesizer speaks less in early rounds
                if persona_key == "synthesizer" and round_num < rounds:
                    if round_num == 1:
                        continue  # Skip first round
                
                message = self._generate_response(persona_key, round_num)
                self.messages.append(message)
                yield message
    
    def get_transcript(self) -> str:
        """Get formatted chat transcript"""
        lines = [f"[User]\n{self.user_input}\n"]
        
        for msg in self.messages:
            lines.append(f"[{msg.emoji} {msg.persona_name}]\n{msg.content}\n")
        
        return "\n".join(lines)


def generate_summary(discussion: Discussion) -> str:
    """Generate a discussion summary using an LLM"""
    
    transcript = discussion.get_transcript()
    
    # Use the first available client
    client = list(discussion.clients.values())[0]
    
    summary_prompt = """You are summarizing a group discussion. Based on the transcript, provide:

1. **Key Points by Participant** - What each person contributed
2. **Main Disagreements** - Where opinions differed
3. **Areas of Agreement** - Where opinions overlapped

Keep it concise and well-organized. Use bullet points."""
    
    messages = [{"role": "user", "content": f"Discussion transcript:\n\n{transcript}\n\nPlease summarize this discussion."}]
    
    return client.generate(summary_prompt, messages, temperature=0.3)


def generate_takeaway(discussion: Discussion) -> str:
    """Generate final synthesized takeaway"""
    
    transcript = discussion.get_transcript()
    
    client = list(discussion.clients.values())[0]
    
    takeaway_prompt = """You are providing a final balanced takeaway from a group discussion. 

Write a calm, neutral conclusion that:
- Combines insights from all perspectives
- Does NOT claim there is one "correct answer"
- Clearly states uncertainties and trade-offs
- Is helpful and actionable where possible

Keep it to 2-3 short paragraphs."""
    
    messages = [{"role": "user", "content": f"Discussion transcript:\n\n{transcript}\n\nProvide a final balanced takeaway."}]
    
    return client.generate(takeaway_prompt, messages, temperature=0.3)
