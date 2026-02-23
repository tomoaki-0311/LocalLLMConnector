import base64
import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def _normalize_base_url(base_url: Optional[str], host: Optional[str]) -> str:
    if base_url:
        return base_url.rstrip("/")
    if not host:
        return "http://localhost:11434"
    if host.startswith("http://") or host.startswith("https://"):
        return host.rstrip("/")
    return f"http://{host}:11434"


@dataclass
class LocalLLMClient:
    base_url: Optional[str] = None
    host: Optional[str] = None
    timeout: int = 60

    def __post_init__(self) -> None:
        self.base_url = _normalize_base_url(self.base_url, self.host)

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

    def generate_with_images(
        self,
        model: str,
        prompt: str,
        image_paths: Optional[Iterable[str]] = None,
        images_b64: Optional[Iterable[str]] = None,
        options: Optional[Dict[str, Any]] = None,
        stream: bool = False,
    ) -> str:
        if stream:
            raise ValueError("stream=True is not supported in this simple client.")

        images = self._prepare_images(image_paths, images_b64)
        payload: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "images": images,
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

    def _prepare_images(
        self,
        image_paths: Optional[Iterable[str]],
        images_b64: Optional[Iterable[str]],
    ) -> List[str]:
        if image_paths and images_b64:
            raise ValueError("Specify either image_paths or images_b64, not both.")

        if images_b64:
            return list(images_b64)

        if not image_paths:
            raise ValueError("image_paths or images_b64 must be provided for images.")

        images: List[str] = []
        for path in image_paths:
            with open(path, "rb") as f:
                images.append(base64.b64encode(f.read()).decode("utf-8"))
        return images

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
