# Capstone MCP Server (TypeScript)

**CS-AI-2025 Lab 6, Spring 2026**

A minimal MCP server that wraps one of your capstone functions so any MCP-compatible client can discover and call it.

---

## Setup

```bash
npm install
npx tsc
```

---

## Test with MCP Inspector

```bash
# In a separate terminal
npx @modelcontextprotocol/inspector
```

In the Inspector UI:
1. Transport: **stdio**
2. Command: `node dist/server.js`
3. Click **Connect**
4. Navigate to **Tools** — your tool should appear
5. Call the tool and verify the result

---

## Connect to Cursor

Edit `~/.cursor/mcp.json` (create it if it does not exist):

```json
{
  "mcpServers": {
    "capstone-tools": {
      "command": "node",
      "args": ["/absolute/path/to/this/directory/dist/server.js"]
    }
  }
}
```

Restart Cursor. Open Composer (Cmd+I) and look for your tool in the tool picker.

---

## What to Modify

Open `src/server.ts` and replace two things:

1. **The tool name, description, and schema** — reflect your actual capstone function
2. **The `capstoneSearch` placeholder** — call your real RAG pipeline, database, or API

Do not change the `McpServer`, `StdioServerTransport`, or `server.connect()` boilerplate — those handle the protocol automatically.

---

## Committing

Place this folder inside your team repo:

```
your-team-repo/
└── mcp-server/          ← this folder's contents go here
    ├── src/
    │   └── server.ts
    ├── package.json
    └── tsconfig.json
```

Then tag and push:

```bash
git add mcp-server/
git commit -m "lab6: mcp server scaffold with search_knowledge_base tool"
git tag lab6-mcp-checkpoint
git push origin main --tags
```

---

*MCP server scaffold for CS-AI-2025 Lab 6, Spring 2026.*
