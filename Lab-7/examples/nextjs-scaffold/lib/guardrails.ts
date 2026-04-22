import type { AgentState } from "./agent-state";

export function requiresHumanApproval(state: AgentState): boolean {
  const text = state.userRequest.toLowerCase();

  return [
    "send",
    "email",
    "submit",
    "delete",
    "book",
    "purchase",
  ].some(term => text.includes(term));
}

export function buildCheckpointMessage(state: AgentState): string {
  return `Approval required before action runs: ${state.userRequest}`;
}
