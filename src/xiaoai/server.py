# server.py
import os
from typing import Dict, Annotated
from pydantic.fields import Field

import requests
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
    description="Xiao Mi Smart Voice Home Assistant, You can use natural language to directive it / "
                "小米家的小爱同学，您的智能语音家居助手，您可以使用自然语言去命令它",
)
def call_xiaoai(
    command: Annotated[str, Field(description="Command to execute, should be natural language")]
) -> str:
    entity_id = os.getenv("HASS_XIAOAI_ENTITY_ID")
    payload = {
        "entity_id": entity_id,
        "execute": True,
        "silent": True,
        "text": command,
    }
    response = execute_service("xiaomi_miot/intelligent_speaker", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    description="Operate Light in your home",
)
def operate_light(
        entity_id: str,
        action: Annotated[str, Field(description="action, should be turn_on or turn_off")]
) -> str:
    payload = {
        "entity_id": entity_id
    }

    response = execute_service(f"light/{action}", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    description="Operate climate in your home",
)
def operate_climate(
        entity_id: str,
        action: Annotated[str, Field(description="action, should be turn_on or turn_off")]
) -> str:
    payload = {
        "entity_id": entity_id,
    }

    response = execute_service(f"climate/{action}", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    description="Operate switch in your home",
)
def operate_switch(
        entity_id: str,
        action: Annotated[str, Field(description="action, should be turn_on or turn_off")]
) -> str:
    payload = {
        "entity_id": entity_id,
    }

    response = execute_service(f"switch/{action}", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    description="press button in your home",
)
def press_button(
    entity_id: Annotated[str, Field(description="the entity_id you will use")],
) -> str:
    payload = {
        "entity_id": entity_id,
    }

    response = execute_service(f"button/press", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    description="press input button in your home",
)
def press_input_button(
    entity_id: Annotated[str, Field(description="the entity_id you will use")],
) -> str:
    payload = {
        "entity_id": entity_id,
    }

    response = execute_service(f"input_button/press", payload)
    response.raise_for_status()
    return "OK"


@mcp.tool(
    description="Get the state of entity"
)
def get_state_of_entity(entity_id: str) -> str:
    host = os.getenv("HASS_HOST")
    token = os.getenv("HASS_TOKEN")

    url = f"https://{host}/api/states/{entity_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "content-type": "application/json",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


@mcp.resource(
    "entity://{entity_id}",
)
def get_state_of_entity_resource(entity_id: str) -> str:
    """Get the state of entity"""
    return get_state_of_entity(entity_id)


def main():
    mcp.run()
