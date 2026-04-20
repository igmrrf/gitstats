import httpx
from typing import Dict, Any, Optional
import json
from ..core.config import settings
from ..core.redis import redis_client
from .ai_providers import AIProviderFactory

class AIService:
    @staticmethod
    async def generate_resume(user_data: Dict[str, Any], top_langs: Dict[str, int], client: httpx.AsyncClient) -> str:
        username = user_data['username']
        cache_key = f"ai:resume:{username}"
        
        cached = await redis_client.get(cache_key)
        if cached:
            return cached.decode()

        try:
            factory = AIProviderFactory()
            provider = factory.get_provider(settings.DEFAULT_AI_PROVIDER)
        except ValueError as e:
            return f"AI Generation is disabled: {str(e)}"

        prompt = f"""
        Generate a professional developer resume summary for {user_data.get('name') or username} (@{username}).
        Stats:
        - Total Stars: {user_data['stars']}
        - Total Repos: {user_data['public_repos']}
        - Top Languages: {', '.join(list(top_langs.keys())[:5])}
        - Followers: {user_data['followers']}
        
        Provide a concise, high-impact 3-paragraph summary of their engineering profile.
        """

        resume = await provider.generate_text(prompt, client)
        if not resume.startswith("Error"):
            await redis_client.setex(cache_key, 86400, resume) # Cache for 24 hours
        return resume

    @staticmethod
    def calculate_expertise_rating(top_langs: Dict[str, int]) -> Dict[str, str]:
        # Simple algorithm to rate expertise based on bytes of code
        ratings = {}
        total_bytes = sum(top_langs.values())
        if total_bytes == 0:
            return {}

        for lang, count in top_langs.items():
            percentage = (count / total_bytes) * 100
            if percentage > 50:
                ratings[lang] = "Expert"
            elif percentage > 20:
                ratings[lang] = "Proficient"
            elif percentage > 5:
                ratings[lang] = "Familiar"
            else:
                ratings[lang] = "Novice"
        return ratings
