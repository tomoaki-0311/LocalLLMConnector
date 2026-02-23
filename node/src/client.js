class LocalLLMClient {
  constructor({ baseUrl = "http://localhost:11434", timeoutMs = 60000 } = {}) {
    this.baseUrl = baseUrl;
    this.timeoutMs = timeoutMs;
  }

  async generate({ model, prompt, options = undefined, stream = false }) {
    if (stream) {
      throw new Error("stream=true is not supported in this simple client.");
    }

    const payload = { model, prompt, stream: false };
    if (options) payload.options = options;

    const data = await this.#postJson("/api/generate", payload);
    return data.response || "";
  }

  async chat({ model, messages, options = undefined, stream = false }) {
    if (stream) {
      throw new Error("stream=true is not supported in this simple client.");
    }

    const payload = { model, messages, stream: false };
    if (options) payload.options = options;

    const data = await this.#postJson("/api/chat", payload);
    return (data.message && data.message.content) || "";
  }

  async #postJson(path, payload) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const res = await fetch(`${this.baseUrl}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });

      if (!res.ok) {
        const body = await res.text();
        throw new Error(`HTTP ${res.status}: ${body}`);
      }

      return await res.json();
    } finally {
      clearTimeout(timeout);
    }
  }
}

module.exports = { LocalLLMClient };
