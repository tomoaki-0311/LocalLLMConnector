const fs = require("fs");

function normalizeBaseUrl(baseUrl, host) {
  if (baseUrl) return baseUrl.replace(/\/$/, "");
  if (!host) return "http://localhost:11434";
  if (host.startsWith("http://") || host.startsWith("https://")) {
    return host.replace(/\/$/, "");
  }
  return `http://${host}:11434`;
}

class LocalLLMClient {
  constructor({ baseUrl = undefined, host = undefined, timeoutMs = 60000 } = {}) {
    this.baseUrl = normalizeBaseUrl(baseUrl, host);
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

  async generateWithImages({
    model,
    prompt,
    imagePaths = undefined,
    imagesBase64 = undefined,
    options = undefined,
    stream = false,
  }) {
    if (stream) {
      throw new Error("stream=true is not supported in this simple client.");
    }

    const images = this.#prepareImages(imagePaths, imagesBase64);
    const payload = { model, prompt, images, stream: false };
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

  #prepareImages(imagePaths, imagesBase64) {
    if (imagePaths && imagesBase64) {
      throw new Error("Specify either imagePaths or imagesBase64, not both.");
    }
    if (imagesBase64) return imagesBase64;
    if (!imagePaths || imagePaths.length === 0) {
      throw new Error("imagePaths or imagesBase64 must be provided for images.");
    }

    return imagePaths.map((p) => fs.readFileSync(p).toString("base64"));
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
