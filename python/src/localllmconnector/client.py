import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError
from urllib.request import Request, urlopen


@dataclass
class LocalLLMClient:
    base_url: str = "http://localhost:11434"
    timeout: int = 60

    def generate(
        self,
        model: str,
        prompt: str,
        options: Optional[Dict[str, Any]] = None,
        stream: bool = False,
    ) -> str:
        if stream:
            raise ValueError("stream=True is not supported in this simple client.")

        payload: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
        if options:
            payload["options"] = options

        url = f"{self.base_url}/api/generate"
        data = self._post_json(url, payload)
        return data.get("response", "")

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        options: Optional[Dict[str, Any]] = None,
        stream: bool = False,
    ) -> str:
        if stream:
            raise ValueError("stream=True is not supported in this simple client.")

        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
        }
        if options:
            payload["options"] = options

        url = f"{self.base_url}/api/chat"
        data = self._post_json(url, payload)
        msg = data.get("message", {})
        return msg.get("content", "")

    def _post_json(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        req = Request(url, data=body, headers={"Content-Type": "application/json"})
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                resp_body = resp.read().decode("utf-8")
        except HTTPError as exc:
            error_body = exc.read().decode("utf-8") if exc.fp else ""
            raise RuntimeError(f"HTTP {exc.code}: {error_body}") from exc

        return json.loads(resp_body)
