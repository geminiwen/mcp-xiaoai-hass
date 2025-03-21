# server.py
import os
import pathlib
import shlex
import subprocess
import requests
import json

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("XiaoAi")


@mcp.tool(
    description="Smart Home Assistant / 小爱同学，您的智能家居助手",
)
def execute_text_directive(text: str) -> str:
    url = "https://hass.home.geminiwen.com/api/services/xiaomi_miot/intelligent_speaker"
    entity_id = os.getenv("HASS_XIAOAI_ENTITY_ID")
    token = os.getenv("HASS_TOKEN")
    payload = {
        "entity_id": "media_player.xiaomi_lx05_0ed6_play_control",
        "execute": True,
        "silent": True,
        "text": text,
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "content-type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return "OK"


def main():
    mcp.run()
