import { NextRequest, NextResponse } from "next/server";

import type { AgentState } from "@/lib/agent-state";
import { retryWithBackoff, withTimeout } from "@/lib/retry";
import { requiresHumanApproval, buildCheckpointMessage } from "@/lib/guardrails";

async function fakeModelCall(prompt: string): Promise<string> {
  await new Promise(resolve => setTimeout(resolve, 100));
  return `Model output for: ${prompt}`;
}

export async function POST(req: NextRequest) {
  const body = await req.json();

  const state: AgentState = {
    sessionId: body.sessionId ?? crypto.randomUUID(),
    userRequest: body.message ?? "",
    messages: body.messages ?? [],
    currentStep: "research",
    approvalRequired: false,
    approved: null,
    retryCount: 0,
    timeoutMs: 8000,
    lastError: null,
    researchNotes: null,
    finalResponse: null,
  };

  try {
    const researchNotes = await retryWithBackoff(async (attempt) => {
      state.retryCount = attempt - 1;
      return await withTimeout(fakeModelCall(state.userRequest), state.timeoutMs);
    });

    state.researchNotes = researchNotes;
    state.currentStep = "write";
    state.finalResponse = `Draft based on research: ${researchNotes}`;

    state.approvalRequired = requiresHumanApproval(state);

    if (state.approvalRequired) {
      state.currentStep = "human_review";
      state.approved = false;
      state.finalResponse = buildCheckpointMessage(state);
    } else {
      state.currentStep = "done";
    }

    return NextResponse.json({ state });
  } catch (error) {
    state.currentStep = "failed";
    state.lastError = error instanceof Error ? error.message : "unknown_error";

    return NextResponse.json({ state }, { status: 500 });
  }
}
