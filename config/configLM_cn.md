
# 🚀 LM Studio — GGUF 本地模型 curl 示例

本文档指导如何通过 `http://localhost:1234/v1/chat/completions` 调用 **LM Studio API** 来使用各种 GGUF 模型。
只需复制相应的命令块并在终端中运行即可。
使用前，需要在 LM Studio 中将模型加载到 GPU 上。

---

## 🦉 Hermes 3 — Llama 3.1 8B (Q4_K_M)

**模型文件：** `Hermes-3-Llama-3.1-8B.Q4_K_M.gguf`
**API 模型 ID：** `hermes-3-llama-3.1-8b`

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "hermes-3-llama-3.1-8b",
    "messages": [
      { "role": "system", "content": "Always answer in rhymes. Today is Thursday" },
      { "role": "user", "content": "What day is it today?" }
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": false
}'
```

---

## 🐉 Deepseek 0528 distill QWen3 — 8B (Q4_K_M)

**模型文件：** `DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf`
**API 模型 ID：** `deepseek/deepseek-r1-0528-qwen3-8b`

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek/deepseek-r1-0528-qwen3-8b",
    "messages": [
        {
            "role": "system",
            "content": "Always answer in rhymes. Today is Thursday"
        },
        {
            "role": "user",
            "content": "What day is it today?"
        }
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": false
}'
```
---

## 🐉 通义千问 3 — 8B (Q6_K)

**模型文件：** `Qwen3-8B-Q6_K.gguf`
**API 模型 ID：** `qwen3-8b`

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-8b",
    "messages": [
      { "role": "system", "content": "Always answer in rhymes. Today is Thursday" },
      { "role": "user", "content": "What day is it today?" }
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": false
}'
```

---

## 🐉 通义千问 3 — 14B (Q4_K_M)

**模型文件：** `Qwen3-14B-Q4_K_M.gguf`
**API 模型 ID：** `qwen3-14b`

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-14b",
    "messages": [
      { "role": "system", "content": "Always answer in rhymes. Today is Thursday" },
      { "role": "user", "content": "What day is it today?" }
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": false
}'
```

---

## 🦙 Meta Llama 3.1 — 8B 指令 (Q5_K_M)

**模型文件：** `Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf`
**API 模型 ID：** `meta-llama-3.1-8b-instruct@q5_k_m`

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama-3.1-8b-instruct@q5_k_m",
    "messages": [
      { "role": "system", "content": "Always answer in rhymes. Today is Thursday" },
      { "role": "user", "content": "What day is it today?" }
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": false
}'
```

---

## 🦙 Meta Llama 3.1 — 8B 指令 (Q6_K)

**模型文件：** `Meta-Llama-3.1-8B-Instruct-Q6_K.gguf`
**API 模型 ID：** `meta-llama-3.1-8b-instruct@q6_k`

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama-3.1-8b-instruct@q6_k",
    "messages": [
      { "role": "system", "content": "Always answer in rhymes. Today is Thursday" },
      { "role": "user", "content": "What day is it today?" }
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": false
}'
```

---

## 🦙 Meta Llama 3.1 — 8B 指令 (Q8_0)

**模型文件：** `Meta-Llama-3.1-8B-Instruct-Q8_0.gguf`
**API 模型 ID：** `meta-llama-3.1-8b-instruct@q8_0`

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama-3.1-8b-instruct@q8_0",
    "messages": [
      { "role": "system", "content": "Always answer in rhymes. Today is Thursday" },
      { "role": "user", "content": "What day is it today?" }
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": false
}'
```

---

