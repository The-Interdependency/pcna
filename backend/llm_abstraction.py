"""
LLM Orchestrator - Hot-swappable multi-provider LLM abstraction
Supports: OpenAI, Anthropic, Google Gemini with automatic fallback
"""
import asyncio
import logging
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

from emergentintegrations.llm.chat import LlmChat, UserMessage

load_dotenv()

logger = logging.getLogger("llm_orchestrator")

class LLMProvider:
    """Individual LLM provider wrapper"""
    def __init__(self, api_key: str, provider: str, model: str):
        self.api_key = api_key
        self.provider = provider
        self.model = model
        self.chat = None
        self.failures = 0
        self.max_failures = 3
        
    async def initialize(self, system_message: str = "You are a helpful AI assistant."):
        """Initialize chat session"""
        try:
            self.chat = LlmChat(
                api_key=self.api_key,
                session_id=f"{self.provider}-{self.model}",
                system_message=system_message
            )
            self.chat.with_model(self.provider, self.model)
            logger.info(f"Initialized {self.provider}/{self.model}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize {self.provider}/{self.model}: {e}")
            return False
    
    async def chat_async(self, prompt: str) -> Optional[str]:
        """Send message and get response"""
        if self.failures >= self.max_failures:
            logger.warning(f"{self.provider}/{self.model} disabled due to failures")
            return None
            
        try:
            if not self.chat:
                await self.initialize()
                
            user_message = UserMessage(text=prompt)
            response = await self.chat.send_message(user_message)
            
            # Reset failure count on success
            self.failures = 0
            return response
            
        except Exception as e:
            self.failures += 1
            logger.error(f"{self.provider}/{self.model} error (failure {self.failures}/{self.max_failures}): {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if provider is available"""
        return self.failures < self.max_failures

class LLMOrchestrator:
    """
    Hot-swappable LLM orchestrator with automatic fallback
    Manages multiple providers and selects best based on task type
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.providers: Dict[str, LLMProvider] = {}
        self.primary_provider = "openai"
        self._initialize_providers()
        
    def _initialize_providers(self):
        """Initialize all supported providers"""
        # OpenAI GPT-5.2 - Best for reasoning
        self.providers["openai"] = LLMProvider(
            api_key=self.api_key,
            provider="openai",
            model="gpt-5.2"
        )
        
        # Anthropic Claude - Best for long-form, ethical reasoning
        self.providers["anthropic"] = LLMProvider(
            api_key=self.api_key,
            provider="anthropic",
            model="claude-4-sonnet-20250514"
        )
        
        # Google Gemini - Best for fast responses
        self.providers["gemini"] = LLMProvider(
            api_key=self.api_key,
            provider="gemini",
            model="gemini-2.5-pro"
        )
        
        logger.info("LLM providers registered")
    
    async def chat(self, 
                   prompt: str, 
                   provider: Optional[str] = None, 
                   model: Optional[str] = None,
                   system_message: str = "You are a helpful AI assistant.") -> str:
        """
        Send chat message with automatic fallback
        
        Args:
            prompt: User prompt
            provider: Preferred provider (openai, anthropic, gemini)
            model: Specific model to use
            system_message: System prompt
        
        Returns:
            LLM response string
        """
        # If specific provider requested, try that first
        if provider and provider in self.providers:
            result = await self._try_provider(provider, prompt, system_message, model)
            if result:
                return result
        
        # Fallback cascade: try all available providers
        fallback_order = ["openai", "anthropic", "gemini"]
        for prov in fallback_order:
            if prov in self.providers and self.providers[prov].is_available():
                result = await self._try_provider(prov, prompt, system_message, model)
                if result:
                    return result
        
        raise Exception("All LLM providers failed")
    
    async def _try_provider(self, 
                           provider: str, 
                           prompt: str, 
                           system_message: str,
                           model: Optional[str] = None) -> Optional[str]:
        """Try a specific provider"""
        try:
            llm = self.providers[provider]
            
            # Override model if specified
            if model:
                llm.model = model
                await llm.initialize(system_message)
            elif not llm.chat:
                await llm.initialize(system_message)
                
            return await llm.chat_async(prompt)
        except Exception as e:
            logger.error(f"Provider {provider} failed: {e}")
            return None
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all providers"""
        return {
            prov: {
                "available": provider.is_available(),
                "failures": provider.failures,
                "model": provider.model
            }
            for prov, provider in self.providers.items()
        }
    
    def switch_primary(self, provider: str):
        """Hot-swap primary provider"""
        if provider in self.providers:
            self.primary_provider = provider
            logger.info(f"Primary provider switched to {provider}")
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using LLM"""
        prompt = f"""Analyze the sentiment and emotional tone of the following text. 
        Return a JSON with: sentiment (positive/negative/neutral), confidence (0-1), and key_emotions (list).
        
        Text: {text}
        
        Return only valid JSON."""
        
        response = await self.chat(prompt, provider="gemini")  # Gemini is fast for this
        
        # Parse JSON response
        import json
        try:
            return json.loads(response)
        except:
            return {"sentiment": "neutral", "confidence": 0.5, "key_emotions": []}
    
    async def generate_researcher_outreach(self, researcher_profile: Dict) -> str:
        """Generate personalized researcher outreach message"""
        prompt = f"""Generate a professional, trauma-informed outreach message to a researcher.
        
        Researcher Profile:
        - Name: {researcher_profile.get('name', 'Unknown')}
        - Field: {researcher_profile.get('field', 'AI/ML')}
        - Interests: {researcher_profile.get('interests', 'machine learning, neural architectures')}
        
        The message should:
        1. Be respectful and transparent
        2. Explain PCNA (Prime Circular Neural Architecture) briefly
        3. Highlight potential collaboration opportunities
        4. Include harm reduction and ethical AI focus
        5. Be concise (under 200 words)
        
        Generate the message:"""
        
        return await self.chat(prompt, provider="anthropic")  # Claude is best for empathetic content
