import httpx
import os
import json

# Shortcut API client
class ShortcutClient:
    def __init__(self, api_url, api_token, user_agent = os.getenv("SHORTCUT_USER_AGENT")):
        self.api_token = api_token
        self.base_url = api_url
        self.headers = {
            "Content-Type": "application/json",
            "Shortcut-Token": api_token,
            "User-Agent": user_agent
        }
    
    async def get(self, endpoint, params=None):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def post(self, endpoint, data):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                json=data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def put(self, endpoint, data):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                json=data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def delete(self, endpoint):
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.status_code
