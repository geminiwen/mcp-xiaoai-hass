# server.py
import os
from http.client import responses

import requests
from typing import Dict, Any

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Home Assistant")


def execute_service(service: str, payload: Dict[str, str]):
    host = os.getenv("HASS_HOST")
    token = os.getenv("HASS_TOKEN")

    url = f"https://{host}/api/services/{service}"
    headers = {
        "Authorization": f"Bearer {token}",
        "content-type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)
    return response


@mcp.tool(
    name="Turn On Light",
    description="Turn On Light in your home",
)
def turn_on_light(entity_id: str) -> str:
    payload = {
        "entity_id": entity_id
    }

    response = execute_service("light/turn_on", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    name="XiaoAi: XiaoMi Home Assistant / 小爱同学",
    description="Xiao Mi Smart Voice Home Assistant / 小米家的小爱同学，您的智能语音家居助手",
)
def execute_voice_directive(text: str) -> str:
    entity_id = os.getenv("HASS_XIAOAI_ENTITY_ID")
    payload = {
        "entity_id": entity_id,
        "execute": True,
        "silent": True,
        "text": text,
    }
    response = execute_service("xiaomi_miot/intelligent_speaker", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    name="Turn Off Light",
    description="Turn Off Light in your home",
)
def turn_off_light(entity_id: str) -> str:
    payload = {
        "entity_id": entity_id
    }

    response = execute_service("light/turn_off", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    name="Turn On Climate",
    description="Turn On Climate in your home",
)
def turn_on_climate(entity_id: str) -> str:
    payload = {
        "entity_id": entity_id,
    }

    response = execute_service("climate/turn_on", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    name="Turn Off Climate",
    description="Turn Off Climate in your home",
)
def turn_on_climate(entity_id: str) -> str:
    payload = {
        "entity_id": entity_id,
    }

    response = execute_service("climate/turn_off", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    name="Turn On Switch",
    description="Turn On Switch in your home",
)
def turn_on_switch(entity_id: str) -> str:
    payload = {
        "entity_id": entity_id,
    }

    response = execute_service("switch/turn_on", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    name="Turn Off Switch",
    description="Turn Off Switch in your home",
)
def turn_on_switch(entity_id: str) -> str:
    payload = {
        "entity_id": entity_id,
    }

    response = execute_service("switch/turn_off", payload)
    response.raise_for_status()
    return "OK"


def main():
    mcp.run()
