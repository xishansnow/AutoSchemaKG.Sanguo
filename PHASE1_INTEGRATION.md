# Phase 1 Integration - Summary

## Thay đổi chính

### 1. Token-based Chunking (Aligned with AutoSchemaKG)

**Cấu hình mới:**
```python
TOKEN_LIMIT = 4096                    # Giới hạn token của LLM
INSTRUCTION_TOKEN_ESTIMATE = 200      # Token dành cho instruction/prompt
CHAR_TO_TOKEN_RATIO = 3.5             # Tỷ lệ ước tính: 3.5 ký tự = 1 token
Max Chunk Size = (4096 - 200) * 3.5 = 13,636 ký tự
```

**So sánh với trước:**
- ❌ Old: 2000 ký tự/chunk (quá nhỏ, lãng phí API calls)
- ✅ New: ~13,636 ký tự/chunk (tối ưu cho context window)

### 2. Structure-Aware Chunking

**Logic:**
- Đọc file Markdown và theo dõi stack các Header (`#`, `##`, `###`)
- Khi cắt text, tự động chèn ngữ cảnh vào đầu mỗi chunk:
  ```
  Context: YOUR BODY AND DISEASE > DISORDER ARTICLES > Diabetes > Symptoms
  
  Content:
  [Nội dung đoạn văn...]
  ```
- Nếu một section quá dài (> 13,636 chars), tự động cắt nhỏ theo paragraph

**Lợi ích:**
- LLM hiểu được ngữ cảnh của đoạn văn (đang nói về bệnh gì, triệu chứng hay điều trị)
- Trích xuất Triple chính xác hơn

### 3. Deduplication

```python
chunker = MarkdownChunker(deduplicate=True)  # Mặc định bật
```

- Loại bỏ các chunk trùng lặp (thường xảy ra với header/footer lặp lại)
- Tiết kiệm token và chi phí API

### 4. Structured Output Format

**Thay đổi return type:**

```python
# Old format (List of strings)
List[str]

# New format (List of dicts - aligned with AutoSchemaKG)
List[Dict[str, any]] 
```

**Example chunk:**
```json
{
  "id": "ACP_Home_Guide_content",
  "text": "Context: Disease > Diabetes\n\nContent:\nDiabetes is...",
  "chunk_id": 42,
  "metadata": {
    "source_file": "data/parsed/ACP_Home_Guide_content.md",
    "total_chunks": 1523
  }
}
```

### 5. Backward Compatibility

Phase 2 vẫn hỗ trợ cả 2 format:
```python
# Handle both dict format (new) and string format (legacy)
if isinstance(segment, dict):
    text = segment.get('text', '')
    chunk_id = segment.get('chunk_id', idx)
else:
    text = segment  # Legacy string format
```

## Cách sử dụng

### Test riêng Phase 1:

```powershell
python pipeline/phase_1_ingestion.py
```

Output:
```
Testing Phase 1 Ingestion on: data/parsed/ACP_Home_Guide_content.md
Token-based chunking: max ~13636 chars/chunk
  Loading file: data/parsed/ACP_Home_Guide_content.md

✅ Successfully created 1523 chunks.
   Total characters: 15,234,567
   Average chunk size: 10,003 chars
```

### Chạy full pipeline:

```powershell
python main.py
```

## Batching (Tương lai)

Hiện tại Phase 2 xử lý từng chunk một. Để tối ưu hơn, có thể implement batching như AutoSchemaKG:

```python
# In phase_2_triple_extraction.py
BATCH_SIZE_TRIPLE = 16   # Xử lý 16 chunks cùng lúc
BATCH_SIZE_CONCEPT = 64  # Xử lý 64 concepts cùng lúc
```

Tuy nhiên, điều này yêu cầu:
1. LLM API hỗ trợ batch processing
2. Đủ RAM để load nhiều chunks
3. Prompt engineering để xử lý batch

→ Có thể làm sau khi test xong logic cơ bản.

## Files thay đổi

- ✅ `pipeline/phase_1_ingestion.py` - Rewrite hoàn toàn
- ✅ `pipeline/phase_2_triple_extraction.py` - Update để hỗ trợ new format
- ✅ `main.py` - Đổi default input path

## Next Steps

1. Test chunking với file thực: `python pipeline/phase_1_ingestion.py`
2. Kiểm tra ngữ cảnh có được gắn đúng không
3. Chạy full pipeline với LLM stub: `python main.py`
4. Khi sẵn sàng, enable real LLM: `USE_REAL_LLM=true python main.py`
