"""
Capstone MCP Server — CS-AI-2025 Lab 6, Spring 2026 (Python)

A minimal MCP server that exposes one of your capstone functions as a tool.
Any MCP-compatible client (Cursor, Claude Desktop, Claude Code, VS Code)
can discover and call this tool automatically.

SETUP:
    uv add mcp
    # or: pip install mcp

RUN:
    python server.py

TEST:
    npx @modelcontextprotocol/inspector
    -> Select stdio transport
    -> Command: python server.py
    -> Connect and call the tool

CONNECT TO CURSOR:
    Edit ~/.cursor/mcp.json:
    {
      "mcpServers": {
        "capstone-tools": {
          "command": "python",
          "args": ["/absolute/path/to/this/server.py"]
        }
      }
    }
"""

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types


# ─── 1. Create the server instance ──────────────────────────────────────────
app = Server("capstone-tools")   # name visible in MCP Inspector and Cursor


# ─── 2. Declare your tools ──────────────────────────────────────────────────
#
# Replace "search_knowledge_base" with your actual capstone function.
#
# NAMING RULES (from Week 7 lecture):
#   - Use snake_case verbs: get_menu, search_restaurants, check_availability
#   - The name appears exactly as written in the model's tool_call output
#
# DESCRIPTION RULES:
#   - Tell the model WHEN to call this tool, not just what it does
#   - Include example user phrases that should trigger a call
#   - Be explicit about what the tool cannot do
#
# SECURITY CHECKLIST before registering:
#   - Is this tool read-only? (strongly recommended for Lab 6)
#   - Are all arguments validated for type and range?
#   - Does the tool return structured errors, not raw stack traces?

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_knowledge_base",
            description=(
                "Search the capstone project's knowledge base for information relevant to a user query. "
                "Call this when the user asks a question that may be answered by the project's documents, "
                "product catalogue, or stored data. Do not call this for general knowledge questions — "
                "only for questions specific to this project's domain."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type":        "string",
                        "description": "The natural language search query from the user",
                        "minLength":   1,
                        "maxLength":   500,
                    },
                    "top_k": {
                        "type":        "integer",
                        "description": "Maximum number of results to return (1–20)",
                        "minimum":     1,
                        "maximum":     20,
                        "default":     5,
                    },
                },
                "required": ["query"],
            },
        ),
        # Add more tools here by appending to this list:
        # types.Tool(name="get_item_details", description="...", inputSchema={...}),
    ]


# ─── 3. Handle tool calls ────────────────────────────────────────────────────

@app.call_tool()
async def call_tool(
    name:      str,
    arguments: dict,
) -> list[types.TextContent]:

    if name == "search_knowledge_base":
        # ── Input validation ─────────────────────────────────────────────
        query = arguments.get("query")
        if not query or not isinstance(query, str) or not query.strip():
            return [types.TextContent(
                type="text",
                text=json.dumps({"error": "invalid_argument", "message": "query must be a non-empty string"}),
            )]

        top_k = arguments.get("top_k", 5)
        if not isinstance(top_k, int):
            top_k = 5
        top_k = max(1, min(int(top_k), 20))   # clamp to safe range

        # ── Execute ──────────────────────────────────────────────────────
        try:
            results = await capstone_search(query.strip(), top_k)
            return [types.TextContent(
                type="text",
                text=json.dumps(results, indent=2),
            )]
        except Exception as e:
            # Return structured errors — never expose raw stack traces.
            # This content goes directly into the model's context window.
            return [types.TextContent(
                type="text",
                text=json.dumps({"error": "search_failed", "message": str(e)}),
            )]

    # Unknown tool — should not happen if list_tools() is correct
    return [types.TextContent(
        type="text",
        text=json.dumps({"error": "unknown_tool", "tool": name}),
    )]


# ─── Placeholder implementation — replace with your real code ────────────────

async def capstone_search(query: str, top_k: int) -> list[dict]:
    """
    Replace this placeholder with your actual capstone search logic.

    If your capstone uses the Week 5 RAG pipeline:
        from your_rag_module import search
        results = await search(query, top_k)
        return results

    If your capstone queries a database:
        records = db.query("SELECT ... FROM ... WHERE ...", [query])
        return [record.to_dict() for record in records[:top_k]]

    For Lab 6 testing, this placeholder returns synthetic results
    so you can verify the MCP connection works before wiring up
    the real implementation.
    """
    return [
        {
            "score":   0.95,
            "content": f"Placeholder result for query: '{query}'",
            "source":  "example-document.md",
        }
    ][:top_k]


# ─── 4. Run via stdio transport ──────────────────────────────────────────────
# stdio is the correct transport for local MCP servers.
# The MCP client spawns this process and pipes messages over stdin/stdout.

async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
