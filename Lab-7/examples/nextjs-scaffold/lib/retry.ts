export async function withTimeout<T>(promise: Promise<T>, timeoutMs: number): Promise<T> {
  return await Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new Error("timeout")), timeoutMs),
    ),
  ]);
}

export async function retryWithBackoff<T>(
  fn: (attempt: number) => Promise<T>,
  maxAttempts = 4,
  baseDelayMs = 500,
): Promise<T> {
  let lastError: unknown;

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      return await fn(attempt);
    } catch (error) {
      lastError = error;

      if (attempt === maxAttempts) {
        throw error;
      }

      const delay = baseDelayMs * Math.pow(2, attempt - 1);
      const jitter = Math.floor(Math.random() * 100);

      await new Promise(resolve => setTimeout(resolve, delay + jitter));
    }
  }

  throw lastError;
}
