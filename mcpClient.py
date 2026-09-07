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


# =========================================================
# TAVILY CLIENT
# =========================================================

tavily_client = MultiServerMCPClient(
    {
        "tavily": {
            "transport": "streamable_http",
            "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}",
        }
    }
)


# =========================================================
# AVIATIONSTACK CLIENT
# =========================================================

aviation_client = MultiServerMCPClient(
    {
        "aviationstack": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [
                "-m",
                "aviationstack_mcp",
                "mcp",
                "run",
            ],
            "env": {
                "AVIATION_STACK_API_KEY": AVIATION_STACK_API_KEY,
            },
        }
    }
)


# =========================================================
# WEATHER CLIENT
# =========================================================

weather_client = MultiServerMCPClient(
    {
        "weather": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [
                WEATHER_MCP_PATH,
            ],
            "env": {
                "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY,
            },
        }
    }
)


# =========================================================
# TAVILY
# =========================================================

async def tavily_search(query: str):

    tools = await tavily_client.get_tools()

    tool = next(
        (tool for tool in tools if tool.name == "tavily_search"),
        None,
    )

    if tool is None:
        raise ValueError("Tool 'tavily_search' not found")

    return await tool.ainvoke({
        "query": query
    })


# =========================================================
# AVIATIONSTACK
# =========================================================

async def list_airports(search: str = "", limit: int = 10):

    tools = await aviation_client.get_tools()

    tool = next(
        (tool for tool in tools if tool.name == "list_airports"),
        None,
    )

    if tool is None:
        raise ValueError("Tool 'list_airports' not found")

    return await tool.ainvoke({
        "search": search,
        "limit": limit,
        "offset": 0,
    })


async def list_airlines(search: str = "", limit: int = 10):

    tools = await aviation_client.get_tools()

    tool = next(
        (tool for tool in tools if tool.name == "list_airlines"),
        None,
    )

    if tool is None:
        raise ValueError("Tool 'list_airlines' not found")

    return await tool.ainvoke({
        "search": search,
        "limit": limit,
        "offset": 0,
    })


# =========================================================
# WEATHER
# =========================================================

async def current_weather(city: str):

    tools = await weather_client.get_tools()

    tool = next(
        (tool for tool in tools if tool.name == "get_current_weather"),
        None,
    )

    if tool is None:
        raise ValueError("Tool 'get_current_weather' not found")

    return await tool.ainvoke({
        "city": city
    })


async def forecast(city: str):

    tools = await weather_client.get_tools()

    tool = next(
        (tool for tool in tools if tool.name == "get_forecast"),
        None,
    )

    if tool is None:
        raise ValueError("Tool 'get_forecast' not found")

    return await tool.ainvoke({
        "city": city
    })


