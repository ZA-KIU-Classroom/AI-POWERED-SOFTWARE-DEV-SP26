/**
 * Capstone MCP Server — CS-AI-2025 Lab 6, Spring 2026
 *
 * A minimal MCP server that exposes one of your capstone functions as a tool.
 * Any MCP-compatible client (Cursor, Claude Desktop, Claude Code, VS Code)
 * can discover and call this tool automatically.
 *
 * SETUP:
 *   npm install
 *   npx tsc
 *   node dist/server.js
 *
 * TEST:
 *   npx @modelcontextprotocol/inspector
 *   → Select stdio transport
 *   → Command: node dist/server.js
 *   → Connect and call the tool
 *
 * CONNECT TO CURSOR:
 *   Edit ~/.cursor/mcp.json:
 *   {
 *     "mcpServers": {
 *       "capstone-tools": {
 *         "command": "node",
 *         "args": ["/absolute/path/to/mcp-server/dist/server.js"]
 *       }
 *     }
 *   }
 */

import { McpServer }            from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z }                    from "zod";

// ─── 1. Create the server instance ──────────────────────────────────────────
const server = new McpServer({
  name:    "capstone-tools",   // visible in MCP Inspector and Cursor
  version: "1.0.0",
});

// ─── 2. Register your first tool ────────────────────────────────────────────
//
// Replace "search_knowledge_base" with your actual capstone function.
//
// NAMING RULES (from Week 7 lecture):
//   - Use snake_case verbs: get_menu, search_restaurants, check_availability
//   - The name appears exactly as written in the model's tool_call output
//   - Be specific — vague names confuse the model about when to call the tool
//
// DESCRIPTION RULES:
//   - Tell the model WHEN to call this tool, not just what it does
//   - Include example phrases the user might say that should trigger it
//   - Be explicit about what the tool cannot do (sets model expectations)
//
// SECURITY CHECKLIST before registering a tool:
//   - Is this tool read-only? (strongly recommended for Lab 6)
//   - Are all arguments validated before use?
//   - Does the tool return structured errors, not raw stack traces?
//   - Does the tool have a timeout in case the underlying service is slow?

server.tool(
  // Tool name — snake_case, imperative verb
  "search_knowledge_base",

  // Description — tell the model WHEN and WHY to call this
  "Search the capstone project's knowledge base for information relevant to a user query. " +
  "Call this when the user asks a question that may be answered by the project's documents, " +
  "product catalogue, or stored data. Do not call this for general knowledge questions — " +
  "only for questions specific to this project's domain.",

  // Input schema — Zod validates arguments before your handler runs
  {
    query: z.string()
      .min(1, "query must not be empty")
      .max(500, "query must be under 500 characters")
      .describe("The natural language search query from the user"),
    top_k: z.number()
      .int()
      .min(1)
      .max(20)
      .default(5)
      .describe("Maximum number of results to return (1–20)"),
  },

  // Handler — replace with your actual capstone logic
  async ({ query, top_k }) => {
    try {
      // ── Replace this with your real implementation ──────────────────────
      // Examples of what to put here:
      //   - Call your Week 5 RAG search function
      //   - Query your Pinecone / FAISS / pgvector index
      //   - Call your capstone's database for relevant records
      //   - Fetch from an external API your project depends on
      //
      // The function you wrap here should already exist in your codebase.
      // You are packaging it, not rewriting it.

      const results = await capstoneSearch(query, top_k);

      // Every MCP tool must return a content array.
      // For simple cases, JSON.stringify your result into a text block.
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(results, null, 2),
          },
        ],
      };

    } catch (error) {
      // Return structured errors — never expose raw stack traces.
      // The error content goes directly into the model's context window.
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({
              error:   "search_failed",
              message: error instanceof Error ? error.message : "Unknown error",
            }),
          },
        ],
        isError: true,
      };
    }
  }
);

// ─── Add more tools here ────────────────────────────────────────────────────
// server.tool("get_item_details", "...", { id: z.string() }, async ({ id }) => { ... });
// server.tool("list_categories",  "...", {},                 async () => { ... });

// ─── 3. Connect via stdio transport ─────────────────────────────────────────
// stdio is the correct transport for local MCP servers.
// The MCP client (Cursor, Claude Desktop) spawns this process and pipes messages.

const transport = new StdioServerTransport();
await server.connect(transport);

// ─── Placeholder implementation — replace with your real code ────────────────

interface SearchResult {
  score:   number;
  content: string;
  source:  string;
}

async function capstoneSearch(query: string, topK: number): Promise<SearchResult[]> {
  // TODO: Replace this placeholder with your actual RAG or database query.
  //
  // If your capstone uses the Week 5 RAG pipeline, import and call it here.
  // If your capstone queries a database, run the query here.
  //
  // For testing, this placeholder returns synthetic results so you can verify
  // the MCP connection works before wiring up the real implementation.

  return [
    {
      score:   0.95,
      content: `Placeholder result for query: "${query}"`,
      source:  "example-document.md",
    },
  ].slice(0, topK);
}
