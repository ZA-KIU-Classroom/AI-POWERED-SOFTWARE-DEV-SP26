# MCP Setup Guide

**CS-AI-2025 Lab 6, Spring 2026**

---

## What You Are Building

You are wrapping one of your existing capstone backend functions as an MCP (Model Context Protocol) server tool. Once wrapped, any MCP-compatible client — Cursor, Claude Desktop, Claude Code, VS Code — can discover and call your function automatically, without you writing any integration code.

The goal of Lab 6 is to experience this once: write the server, connect a client, call the tool. You do not need to build a production-grade MCP server today.

---

## Choosing Your First Tool

Use this decision framework from the Week 7 lecture:

| Question | If yes... | If no... |
|---|---|---|
| Does the AI need to decide *when* to call it based on user intent? | Good tool candidate | Call it in regular code |
| Does it return real data, not a hardcoded string? | Good tool candidate | Not worth exposing as a tool |
| Is it read-only (search, get, list, fetch)? | Strongly recommended for your first tool | Add confirmation logic before using write/delete/send as a tool |

**Recommended first tools:**
- A search function that queries your capstone's data
- A lookup function that fetches a single record
- A summarisation or classification wrapper around an LLM call

**Avoid as first tools:**
- Anything that writes to a database
- Anything that sends an email or notification
- Anything that modifies or deletes records

---

## TypeScript MCP Server

### Installation

```bash
# In a new mcp-server/ directory inside your team repo
mkdir mcp-server && cd mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install --save-dev typescript @types/node ts-node
```

Create `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true
  },
  "include": ["src/**/*"]
}
```

### Minimal server with one tool

```typescript
// src/server.ts
import { McpServer }           from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z }                   from "zod";

// ─── 1. Create the server ────────────────────────────────────────────────────
const server = new McpServer({
  name:    "capstone-tools",
  version: "1.0.0",
});

// ─── 2. Register a tool ──────────────────────────────────────────────────────
// Replace this example with your actual capstone function.
// The description tells the AI model WHEN to call this tool.
// Be explicit — vague descriptions produce wrong calls.
server.tool(
  "search_knowledge_base",
  "Search the capstone knowledge base for information relevant to a user query. " +
  "Call this when the user asks a question that may be answered by the project's documents or data.",
  {
    query: z.string().describe("The natural language search query"),
    top_k: z.number().default(5).describe("Maximum number of results to return"),
  },
  async ({ query, top_k }) => {
    // ── Replace with your actual implementation ──
    // Example: call your RAG pipeline from Week 5
    const results = await yourRagSearch(query, top_k);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(results),
        },
      ],
    };
  }
);

// ─── 3. Connect via stdio transport ──────────────────────────────────────────
const transport = new StdioServerTransport();
await server.connect(transport);

// ─── Placeholder — replace with your real implementation ─────────────────────
async function yourRagSearch(query: string, topK: number): Promise<object[]> {
  // TODO: import and call your Week 5 RAG service here
  return [
    { score: 0.95, content: `Result for: ${query}`, source: "example.md" },
  ];
}
```

### Build and run

```bash
# Build TypeScript
npx tsc

# Run the server
node dist/server.js
```

---

## Python MCP Server

### Installation

```bash
# In a new mcp-server/ directory inside your team repo
mkdir mcp-server && cd mcp-server
uv init
uv add mcp
# or: pip install mcp
```

### Minimal server with one tool

```python
# server.py
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# ─── 1. Create the server ────────────────────────────────────────────────────
app = Server("capstone-tools")

# ─── 2. Register tools ───────────────────────────────────────────────────────
@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_knowledge_base",
            description=(
                "Search the capstone knowledge base for information relevant to a user query. "
                "Call this when the user asks a question that may be answered by the project's "
                "documents or data."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The natural language search query",
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(
    name: str,
    arguments: dict,
) -> list[types.TextContent]:

    if name == "search_knowledge_base":
        query = arguments["query"]
        top_k = arguments.get("top_k", 5)

        # ── Replace with your actual implementation ──
        results = await your_rag_search(query, top_k)

        return [
            types.TextContent(
                type="text",
                text=str(results),
            )
        ]

    raise ValueError(f"Unknown tool: {name}")


# ─── Placeholder — replace with your real implementation ─────────────────────
async def your_rag_search(query: str, top_k: int) -> list:
    # TODO: import and call your Week 5 RAG service here
    return [
        {"score": 0.95, "content": f"Result for: {query}", "source": "example.md"}
    ]


# ─── 3. Run via stdio transport ──────────────────────────────────────────────
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
```

### Run

```bash
python server.py
```

---

## Testing Your Server with MCP Inspector

MCP Inspector is a browser-based tool that connects to your server and lets you call tools manually.

```bash
# In a separate terminal from your server
npx @modelcontextprotocol/inspector
```

Then in the Inspector UI:

1. Select transport: **stdio**
2. Command: `node dist/server.js` (TypeScript) or `python server.py` (Python)
3. Click **Connect**
4. Navigate to **Tools** — your tool should appear
5. Click the tool, fill in the arguments, click **Call**
6. Verify you see a `content` array with your result

If no tools appear, check that your server starts without errors in a separate terminal first.

---

## Connecting Cursor to Your MCP Server

Once your server is working in the Inspector, you can connect Cursor.

Edit Cursor's MCP config (usually `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "capstone-tools": {
      "command": "node",
      "args": ["/absolute/path/to/your/mcp-server/dist/server.js"]
    }
  }
}
```

For Python:

```json
{
  "mcpServers": {
    "capstone-tools": {
      "command": "python",
      "args": ["/absolute/path/to/your/mcp-server/server.py"]
    }
  }
}
```

Restart Cursor. Open the Composer (Cmd+I) and look for your tool name in the tool picker.

---

## Input Validation

Your tool must validate arguments before executing logic. The model can pass unexpected types.

**TypeScript (Zod handles this automatically):**

Zod validates arguments at the schema level before your handler runs. If the model passes a number where a string is expected, Zod rejects it before your code sees it.

**Python (add explicit validation):**

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search_knowledge_base":
        query = arguments.get("query")
        if not query or not isinstance(query, str):
            return [types.TextContent(
                type="text",
                text='{"error": "query must be a non-empty string"}'
            )]
        top_k = int(arguments.get("top_k", 5))
        top_k = max(1, min(top_k, 20))   # clamp to safe range
        # ... rest of handler
```

---

## Security Checklist Before Committing

- [ ] My tool does not accept raw SQL or shell commands as arguments
- [ ] My tool does not expose environment variables or API keys in its output
- [ ] All arguments are validated for type and range before use
- [ ] If my tool calls an external API, it has a try/except and returns a structured error
- [ ] My tool's description is specific enough that the model will not call it at inappropriate times

---

*MCP setup guide for CS-AI-2025 Lab 6, Spring 2026.*
