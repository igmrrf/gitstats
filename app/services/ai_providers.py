from abc import ABC, abstractmethod

import httpx

from ..core.config import settings


class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str, client: httpx.AsyncClient) -> str:
        pass


class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent?key={self.api_key}"

    async def generate_text(self, prompt: str, client: httpx.AsyncClient) -> str:
        resp = await client.post(
            self.url, json={"contents": [{"parts": [{"text": prompt}]}]}
        )
        if resp.status_code == 200:
            data = resp.json()
            try:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                return f"Error parsing Gemini response: {resp.text}"
        return f"Error from Gemini: {resp.status_code} - {resp.text}"


class OpenAIProvider(BaseAIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/chat/completions"

    async def generate_text(self, prompt: str, client: httpx.AsyncClient) -> str:
        resp = await client.post(
            self.url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": "gpt-4",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            },
        )
        if resp.status_code == 200:
            data = resp.json()
            try:
                return data["choices"][0]["message"]["content"]
            except (KeyError, IndexError):
                return f"Error parsing OpenAI response: {resp.text}"
        return f"Error from OpenAI: {resp.status_code} - {resp.text}"


class AIProviderFactory:
    @staticmethod
    def get_provider(provider_name: str) -> BaseAIProvider:
        if provider_name.lower() == "gemini":
            if not settings.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY is not set")
            return GeminiProvider(settings.GEMINI_API_KEY)
        elif provider_name.lower() == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is not set")
            return OpenAIProvider(settings.OPENAI_API_KEY)
        else:
            raise ValueError(f"Unknown AI provider: {provider_name}")
