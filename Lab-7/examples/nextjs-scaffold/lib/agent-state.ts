export interface ChatMessage {
  role: string;
  content: string;
}

export interface AgentState {
  sessionId: string;
  userRequest: string;
  messages: ChatMessage[];
  currentStep: string;
  approvalRequired: boolean;
  approved: boolean | null;
  retryCount: number;
  timeoutMs: number;
  lastError: string | null;
  researchNotes: string | null;
  finalResponse: string | null;
}
