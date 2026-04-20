import pytest
import httpx
import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.ai import AIService
from app.services.ai_providers import AIProviderFactory, GeminiProvider, OpenAIProvider
from app.core.config import settings

@pytest.mark.asyncio
async def test_ai_provider_factory_default():
    with patch("app.services.ai_providers.settings") as mock_settings:
        mock_settings.GEMINI_API_KEY = "test-key"
        factory = AIProviderFactory()
        provider = factory.get_provider("gemini")
        assert isinstance(provider, GeminiProvider)

@pytest.mark.asyncio
async def test_ai_provider_factory_openai():
    with patch("app.services.ai_providers.settings") as mock_settings:
        mock_settings.OPENAI_API_KEY = "test-key"
        factory = AIProviderFactory()
        provider = factory.get_provider("openai")
        assert isinstance(provider, OpenAIProvider)

@pytest.mark.asyncio
async def test_gemini_provider_generate_text():
    provider = GeminiProvider(api_key="test-key")
    client = AsyncMock(spec=httpx.AsyncClient)
    
    mock_resp = unittest.mock.MagicMock(spec=httpx.Response)
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": "Gemini Resume"}]}}]
    }
    client.post.return_value = mock_resp
    
    result = await provider.generate_text("test prompt", client)
    assert result == "Gemini Resume"
    
    client.post.assert_called_once()
    args, kwargs = client.post.call_args
    assert "generativelanguage.googleapis.com" in args[0]
    assert kwargs["json"]["contents"][0]["parts"][0]["text"] == "test prompt"

@pytest.mark.asyncio
async def test_ai_service_uses_configured_provider():
    user_data = {"username": "testuser", "stars": 10, "public_repos": 5, "followers": 2}
    top_langs = {"Python": 1000}
    client = AsyncMock(spec=httpx.AsyncClient)
    
    with patch("app.services.ai.AIProviderFactory") as MockFactory:
        mock_provider = AsyncMock()
        mock_provider.generate_text.return_value = "Mocked Resume"
        MockFactory.return_value.get_provider.return_value = mock_provider
        
        with patch("app.services.ai.redis_client") as mock_redis:
            mock_redis.get.return_value = None # Cache miss
            mock_redis.setex = AsyncMock()
            
            resume = await AIService.generate_resume(user_data, top_langs, client)
            
            assert resume == "Mocked Resume"
            mock_provider.generate_text.assert_called_once()
            mock_redis.setex.assert_called_once()
