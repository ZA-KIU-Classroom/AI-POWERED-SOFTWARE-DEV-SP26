export interface EpisodeEvent {
  ts: string;
  eventType: string;
  sessionId: string;
  model: string | null;
  success: boolean;
  retryCount: number;
  timeoutMs: number;
  latencyMs: number;
  errorType: string | null;
  approvalRequired: boolean;
  approved: boolean | null;
  costUsd: number;
  notes?: string;
}
