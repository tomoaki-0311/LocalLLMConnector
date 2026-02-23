# LocalLLMConnector

Python と Node.js からローカル LLM（Ollama）にリクエストし、結果を取得するための軽量ライブラリです。

## 事前条件
- Ollama がローカルで起動していること（既定: http://localhost:11434）
- 利用するモデルが pull 済みであること

例:
- `ollama pull llama3.1:8b`
- `ollama pull qwen2.5vl:7b`

## Python ライブラリ
### セットアップ
```bash
cd /Users/tomo/Documents/LocalLLMConnector/python
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 使い方（テキスト生成）
```python
from localllmconnector import LocalLLMClient

client = LocalLLMClient()
text = client.generate(model="llama3.1:8b", prompt="Hello from Python")
print(text)
```

### 使い方（画像解釈）
`image_paths` は複数指定可能です。
```python
from localllmconnector import LocalLLMClient

client = LocalLLMClient()
text = client.generate_with_images(
    model="qwen2.5vl:7b",
    prompt="Describe this image.",
    image_paths=["/path/to/image1.png", "/path/to/image2.png"],
)
print(text)
```

### ホスト名指定
```python
client = LocalLLMClient(host="192.168.3.11")
```

サンプル:
```bash
python samples/python_example.py
python samples/python_vision_example.py
```

## Node.js ライブラリ
### セットアップ
```bash
cd /Users/tomo/Documents/LocalLLMConnector/node
npm install
```

### 使い方（テキスト生成）
```javascript
const { LocalLLMClient } = require("./src");

const client = new LocalLLMClient();
client.generate({ model: "llama3.1:8b", prompt: "Hello from Node" })
  .then(console.log)
  .catch(console.error);
```

### 使い方（画像解釈）
`imagePaths` は複数指定可能です。
```javascript
const { LocalLLMClient } = require("./src");

const client = new LocalLLMClient();
client.generateWithImages({
  model: "qwen2.5vl:7b",
  prompt: "Describe this image.",
  imagePaths: ["/path/to/image1.png", "/path/to/image2.png"],
})
  .then(console.log)
  .catch(console.error);
```

### ホスト名指定
```javascript
const client = new LocalLLMClient({ host: "192.168.3.11" });
```

サンプル:
```bash
node samples/node_example.js
node samples/node_vision_example.js
```

## 仕様
- 既定の Ollama API: `http://localhost:11434`
- `generate` / `chat` / `generate_with_images` を提供
- デフォルトは `stream: false`

## ライセンス
MIT
