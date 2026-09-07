import os
import asyncio
from pdb import main
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATION_STACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

import os
import sys
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATION_STACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEATHER_MCP_PATH = os.path.join(BASE_DIR, "custom_mcp.py")

client = MultiServerMCPClient(
    {
        "tavily": {
            "transport": "streamable_http",
            "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
        },

        "aviationstack": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [
                "-m",
                "aviationstack_mcp",
                "mcp",
                "run"
            ],
            "env": {
                "AVIATION_STACK_API_KEY": AVIATION_STACK_API_KEY
            }
        },

        "weather": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [
                WEATHER_MCP_PATH
            ],
            "env": {
                "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY
            }
        }
    }
)
# Cache tools so we don't load them repeatedly
_tools_cache = None


async def get_tools():
    global _tools_cache

    if _tools_cache is None:
        try:
            _tools_cache = await client.get_tools()

            print("\n========== AVAILABLE MCP TOOLS ==========")
            for tool in _tools_cache:
                print(tool.name)
            print("=========================================\n")

        except Exception as e:
            print("\n========== FULL ERROR ==========")
            print(type(e))
            print(repr(e))
            raise

    return _tools_cache

async def call_tool(tool_name: str, args: dict = None):
    tools = await get_tools()

    tool = next(
        (tool for tool in tools if tool.name == tool_name),
        None,
    )

    if tool is None:
        raise ValueError(f"Tool '{tool_name}' not found")

    return await tool.ainvoke(args or {})


# ------------------------
# Tavily MCP Tools
# ------------------------



async def tavily_search(query: str):
    return await call_tool("tavily_search", {"query": query})


async def list_airports(search: str = "", limit: int = 10):
    return await call_tool("list_airports", {"search": search, "limit": limit, "offset": 0})


async def list_airlines(search: str = "", limit: int = 10):
    return await call_tool("list_airlines", {"search": search, "limit": limit, "offset": 0})


async def current_weather(city: str):
    return await call_tool("get_current_weather", {"city": city})


async def forecast(city: str):
    return await call_tool("get_forecast", {"city": city})
