# server.py
import os
import pathlib
import shlex
import subprocess
import requests
import json

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("XiaoAi-Hass")

@mcp.tool()
def execute_text_directive(text: str) -> str:
    url = "https://hass.home.geminiwen.com/api/services/xiaomi_miot/intelligent_speaker"
    payload = {
        "entity_id": "media_player.xiaomi_lx05_0ed6_play_control",
        "execute": True,
        "silent": True,
        "text": text,
    }

    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIzZTgxN2NmMWM4OWY0OWU4YWQ1ZWJjNDhlNWM3MGIzZSIsImlhdCI6MTc0MjU3MDYxMywiZXhwIjoyMDU3OTMwNjEzfQ.FYvmR_VyMuYuByOgzHXr7RoQCOGpZTXWtKIvZqfIGlk",
        "content-type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.text


def main():
    mcp.run()
