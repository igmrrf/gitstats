import httpx
from typing import Dict, List, Any, Optional
import asyncio
from ..core.redis import redis_client
import json

class GitHubService:
    BASE_URL = "https://api.github.com"
    CACHE_EXPIRATION = 3600  # 1 hour
    _semaphore = asyncio.Semaphore(3)  # Limit concurrency to 3

    def __init__(self, access_token: str, client: httpx.AsyncClient):
        self.headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.client = client
        self.username: Optional[str] = None

    async def _get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        # Use a stable cache key that includes the username if available
        prefix = f"gh:{self.username}" if self.username else "gh:anonymous"
        cache_key = f"{prefix}:{endpoint}:{json.dumps(params, sort_keys=True)}"
        
        async with self._semaphore:
            cached = await redis_client.get(cache_key)
            if cached:
                # redis_client.get returns bytes since we disabled auto-decoding in pool
                return json.loads(cached.decode('utf-8'))

            resp = await self.client.get(
                f"{self.BASE_URL}{endpoint}",
                headers=self.headers,
                params=params
            )
            resp.raise_for_status()
            data = resp.json()
            
            await redis_client.setex(
                cache_key,
                self.CACHE_EXPIRATION,
                json.dumps(data)
            )
            return data

    async def get_user_stats(self) -> Dict[str, Any]:
        user_data = await self._get("/user")
        self.username = user_data["login"] # Store username for subsequent cache keys
        repos = await self._get("/user/repos", params={"per_page": 100, "type": "owner"})
        
        total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
        total_forks = sum(repo.get("forks_count", 0) for repo in repos)
        
        return {
            "username": user_data["login"],
            "name": user_data.get("name"),
            "stars": total_stars,
            "forks": total_forks,
            "public_repos": user_data["public_repos"],
            "followers": user_data["followers"],
            "following": user_data["following"]
        }

    async def get_top_languages(self) -> Dict[str, int]:
        repos = await self._get("/user/repos", params={"per_page": 100, "type": "owner"})
        languages_tasks = [
            self._get(f"/repos/{repo['owner']['login']}/{repo['name']}/languages")
            for repo in repos if not repo["fork"]
        ]
        
        languages_results = await asyncio.gather(*languages_tasks)
        
        aggregated_langs = {}
        for lang_dict in languages_results:
            for lang, bytes_count in lang_dict.items():
                aggregated_langs[lang] = aggregated_langs.get(lang, 0) + bytes_count
        
        return dict(sorted(aggregated_langs.items(), key=lambda item: item[1], reverse=True))

    async def get_repo_pins(self, count: int = 6) -> List[Dict[str, Any]]:
        # For simplicity, we'll take top N repos by stars as "pins" for now. 
        # Real GitHub pins are fetched via GraphQL but we'll stick to REST for Phase 3.
        repos = await self._get("/user/repos", params={"sort": "stargazers", "per_page": count})
        return [{
            "name": repo["name"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "description": repo.get("description"),
            "language": repo.get("language")
        } for repo in repos]
