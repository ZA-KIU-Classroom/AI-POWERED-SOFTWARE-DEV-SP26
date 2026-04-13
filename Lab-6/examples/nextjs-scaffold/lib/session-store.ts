/**
 * Session Store — CS-AI-2025 Lab 6, Spring 2026
 *
 * In-memory conversation state management with sliding window trimming.
 * Sessions live in module-level memory — they are lost when the server restarts.
 * This is acceptable for Lab 6. Migrate to Redis in Week 12 without changing
 * this interface.
 */

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type Role = "system" | "user" | "assistant";

export interface Message {
  role:    Role;
  content: string;
}

// ---------------------------------------------------------------------------
// In-process store
// ---------------------------------------------------------------------------

// In Next.js, module-level state persists across requests within a single
// server process. In development with hot reload, this resets on file changes.
const _sessions = new Map<string, Message[]>();

// Keep the system prompt plus the last MAX_TURNS * 2 messages (one user + one
// assistant per turn). At ~100 tokens per message, 20 turns ≈ 4,000 history tokens.
const MAX_TURNS = 20;

// ---------------------------------------------------------------------------
// Public interface
// ---------------------------------------------------------------------------

/**
 * Return a copy of the message history for this session.
 * Returns an empty array if the session does not exist.
 */
export function loadSession(sessionId: string): Message[] {
  return [...(_sessions.get(sessionId) ?? [])];
}

/**
 * Save the message history, applying the sliding window trim.
 * The system prompt is always preserved.
 */
export function saveSession(sessionId: string, messages: Message[]): void {
  _sessions.set(sessionId, trim(messages));
}

/**
 * Delete all history for a session.
 * Expose this via DELETE /api/session/[id] for user-controlled deletion.
 */
export function deleteSession(sessionId: string): void {
  _sessions.delete(sessionId);
}

/** Return the number of messages in a session (debugging only). */
export function sessionLength(sessionId: string): number {
  return _sessions.get(sessionId)?.length ?? 0;
}

/** Return all active session IDs (debugging only — never expose to users). */
export function listSessions(): string[] {
  return [..._sessions.keys()];
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

function trim(messages: Message[]): Message[] {
  const system    = messages.filter(m => m.role === "system");
  const nonSystem = messages.filter(m => m.role !== "system");

  const maxNonSystem = MAX_TURNS * 2;   // user + assistant per turn

  if (nonSystem.length <= maxNonSystem) {
    return [...system, ...nonSystem];
  }

  // Keep only the most recent messages beyond the system prompt
  return [...system, ...nonSystem.slice(-maxNonSystem)];
}
