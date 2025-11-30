# 🚀 LM Studio — Mẫu cURL cho các mô hình GGUF cục bộ

Tài liệu này hướng dẫn cách gọi API **LM Studio** (qua `http://localhost:1234/v1/chat/completions`) cho các mô hình GGUF khác nhau.  
Chỉ cần sao chép khối lệnh tương ứng và chạy trong terminal.
Cần Load Model trên LM Studio vào GPU trước khi sử dụng.

---

## 🦉 Hermes 3 — Llama 3.1 8B (Q4_K_M)

**Model file:** `Hermes-3-Llama-3.1-8B.Q4_K_M.gguf`  
**Model ID trong API:** `hermes-3-llama-3.1-8b`

```bash
curl http://localhost:1234/v1/chat/completions   -H "Content-Type: application/json"   -d '{
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

## 🐉 Qwen 3 — 8B (Q6_K)

**Model file:** `Qwen3-8B-Q6_K.gguf`  
**Model ID trong API:** `qwen3-8b`

```bash
curl http://localhost:1234/v1/chat/completions   -H "Content-Type: application/json"   -d '{
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

## 🐉 Qwen 3 — 14B (Q4_K_M)

**Model file:** `Qwen3-14B-Q4_K_M.gguf`  
**Model ID trong API:** `qwen3-14b`

```bash
curl http://localhost:1234/v1/chat/completions   -H "Content-Type: application/json"   -d '{
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


## 🦙 Meta Llama 3.1 — 8B Instruct (Q5_K_M)

**Model file:** `Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf`  
**Model ID trong API:** `meta-llama-3.1-8b-instruct@q5_k_m`

```bash
curl http://localhost:1234/v1/chat/completions   -H "Content-Type: application/json"   -d '{
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

## 🦙 Meta Llama 3.1 — 8B Instruct (Q6_K)

**Model file:** `Meta-Llama-3.1-8B-Instruct-Q6_K.gguf`  
**Model ID trong API:** `meta-llama-3.1-8b-instruct@q6_k`

```bash
curl http://localhost:1234/v1/chat/completions   -H "Content-Type: application/json"   -d '{
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

## 🦙 Meta Llama 3.1 — 8B Instruct (Q8_0)

**Model file:** `Meta-Llama-3.1-8B-Instruct-Q8_0.gguf`  
**Model ID trong API:** `meta-llama-3.1-8b-instruct@q8_0`

```bash
curl http://localhost:1234/v1/chat/completions   -H "Content-Type: application/json"   -d '{
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
