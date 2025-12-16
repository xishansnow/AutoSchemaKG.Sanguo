"""
Phase 1: Document Ingestion & Preprocessing
======================================================
Handles the loading of parsed Markdown files and segments them into 
context-aware chunks for the Triple Extraction phase.
"""

import os
import re
from typing import List, Dict, Tuple, Set
import json
from pathlib import Path
from pipeline.chunker import MarkdownChunker, PlainTextChunker
from pipeline.wenyanwen import WenyanTransformer
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # Import Progress Bar library

# CONFIGURE NUMBER OF THREADS
# With RTX 3080 10GB + Llama 3 8B, level 4-5 is optimal.    
MAX_WORKERS = int(os.getenv("MODEL_MAX_THREADS", "5"))

# Replace hard-coded path with env-configurable path
LOG_DIR = Path(os.getenv("OUTPUT_DIR", "output"))
_PHASE1_API_LOG = Path(os.getenv("PHASE1_API_LOG", str(LOG_DIR / "phase1_llm_calls.jsonl")))
_PHASE1_API_LOG.parent.mkdir(parents=True, exist_ok=True)

def _append_phase1_api_log(entry: dict):
    """Append one JSON line to output/phase1_llm_calls.jsonl"""
    try:
        with open(_PHASE1_API_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        # never fail the extractor because of logging
        print(f"  ⚠ Warning: failed to write phase1 api log: {e}")



def load_and_segment_text(file_path: str, deduplicate: bool = True, is_wenyanwen: bool = True, use_real_llm: bool = False) -> List[Dict[str, any]]:
    """
    Load a historical text document (Markdown or Text) and segment it.
    Returns structured chunks with metadata (aligned with AutoSchemaKG format).
    
    Args:
        file_path (str): Path to the file (can be .md or .txt)
        deduplicate (bool): Whether to remove duplicate chunks
        
    Returns:
        List[Dict]: List of chunk dictionaries with 'id', 'text', 'chunk_id', 'metadata'
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    print(f"  Loading file: {file_path}")
    
    # Extract document ID from filename
    doc_id = os.path.splitext(os.path.basename(file_path))[0]
    
    # Use MarkdownChunker for .md files else fallback to Plain text splitting
    if file_path.endswith('.md'):
        chunker = MarkdownChunker(deduplicate=deduplicate)
        raw_segments = chunker.chunk_file(file_path)
    else:        
        chunker = PlainTextChunker(deduplicate=deduplicate)        
        raw_segments = chunker.chunk_file(file_path)   
        
    # Filter out very short chunks (often artifacts)
    raw_segments = [s for s in raw_segments if len(s) > 50]
    
    # Format as structured chunks (AutoSchemaKG format)
    # Each chunk is a dict with 'id', 'text', 'chunk_id', 'metadata'    
    structured_chunks = []
    for idx, text in enumerate(raw_segments):
        chunk = {
            "id": doc_id,
            "text": text,
            "chunk_id": idx,
            "metadata": {
                "source_file": file_path,
                "total_chunks": len(raw_segments)
            }
        }
        structured_chunks.append(chunk)
        
    # Transform from wenyanwen (classical Chinese) to baihuawen (modern Chinese) if needed
    if is_wenyanwen:
        structured_chunks = _transform_chunks(structured_chunks, use_real_llm)
    
    # Transform from wenyanwen (classical Chinese) to baihuawen (modern Chinese) if needed
    # transformer = WenyanTransformer()  
    # for idx, chunk in enumerate(structured_chunks):                
    #     text = transformer.transform_single_segment(chunk["text"], use_real_llm)
    #     structured_chunks[idx]["text"] = text
        
    return structured_chunks

def _transform_chunks(raw_chunks: List[Dict], use_real_llm: bool = False) -> List[Dict]:
    """
    Transform a list of text segments from wenyanwen to baihuawen.
    
    Args:
        raw_chunks (List[str]): List of text segments in wenyanwen            
        use_real_llm (bool): Whether to use real LLM API calls
    Returns:
        List[str]: Transformed text segments in baihuawen
    """  
       
    transformer = WenyanTransformer()
    
    # Define checkpoint file path
    checkpoint_file = LOG_DIR / "phase1_transform_checkpoint.jsonl"
    checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing checkpoints if any
    completed_indices = set()
    transformed_chunks = [None] * len(raw_chunks)
    
    if checkpoint_file.exists():
        print(f"  📂 Loading existing checkpoint from {checkpoint_file}")
        try:
            with open(checkpoint_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)
                        idx = entry["chunk_id"]
                        completed_indices.add(idx)
                        transformed_chunks[idx] = entry["chunk"]
            print(f"  ✓ Loaded {len(completed_indices)} completed transformations")
        except Exception as e:
            print(f"  ⚠ Warning: failed to load checkpoint: {e}")
            completed_indices = set()
    
    # Filter out already completed chunks
    pending_chunks = [(idx, chunk) for idx, chunk in enumerate(raw_chunks) if idx not in completed_indices]
    total_chunks = len(raw_chunks)
    pending_count = len(pending_chunks)
    
    if pending_count == 0:
        print(f"  ✅ All {total_chunks} chunks already transformed!")
        return transformed_chunks
    
    print(f"  🚀 Starting Parallel Transform on {pending_count}/{total_chunks} segments with {MAX_WORKERS} threads...")
    print(f"  ⚡ GPU Utilization target: MAX POWER")
    
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, pending_count)) as executor:
        # Submit transformation tasks for pending chunks only
        future_to_idx = {
            executor.submit(transformer.transform_single_segment, chunk["text"], use_real_llm): idx 
            for idx, chunk in pending_chunks
        }
        
        with tqdm(total=pending_count, desc="  Transforming", unit="seg", ncols=100, initial=0) as pbar:
            # Collect results as they complete
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:                    
                    transformed_text = future.result()
                    transformed_text = transformed_text.replace('\n', '')
                    transformed_chunk = {
                        **raw_chunks[idx],
                        "text": transformed_text
                    }
                    transformed_chunks[idx] = transformed_chunk
                    
                    # Save checkpoint immediately after each successful transformation
                    try:
                        with open(checkpoint_file, "a", encoding="utf-8") as f:
                            checkpoint_entry = {
                                "chunk_id": idx,
                                "chunk": transformed_chunk
                            }
                            f.write(json.dumps(checkpoint_entry, ensure_ascii=False) + "\n")
                    except Exception as e:
                        pbar.write(f"  ⚠ Warning: failed to save checkpoint for chunk {idx}: {e}")
                    
                except Exception as e:
                    pbar.write(f"  ✗ Error transforming chunk {idx}: {e}")
                    # Keep original text if transformation fails
                    transformed_chunks[idx] = raw_chunks[idx]
                    # Also save the original as checkpoint to mark it as "processed"
                    try:
                        with open(checkpoint_file, "a", encoding="utf-8") as f:
                            checkpoint_entry = {
                                "chunk_id": idx,
                                "chunk": raw_chunks[idx]
                            }
                            f.write(json.dumps(checkpoint_entry, ensure_ascii=False) + "\n")
                    except Exception as ce:
                        pbar.write(f"  ⚠ Warning: failed to save checkpoint for failed chunk {idx}: {ce}")
                finally:
                    pbar.update(1)
        
    print(f"\n  ✅ Parallel transformation complete! Processed {total_chunks} segments.")
    print(f"  💾 Checkpoint saved to {checkpoint_file}")
                
    return transformed_chunks


# if __name__ == "__main__":
#     # Test the chunking logic directly
#     import sys
#     import json
    
#     # Default test file
#     test_file = "data/sanguo_origin.txt"
    
#     # Allow passing file path as argument
#     if len(sys.argv) > 1:
#         test_file = sys.argv[1]
        
#     print(f"Testing Phase 1 Ingestion on: {test_file}")
#     print(f"Token-based chunking: max ~{int((TOKEN_LIMIT - INSTRUCTION_TOKEN_ESTIMATE) * CHAR_TO_TOKEN_RATIO)} chars/chunk")
    
#     try:
#         chunks = load_and_segment_text(test_file)
#         print(f"\n✅ Successfully created {len(chunks)} chunks.")
        
#         # Statistics
#         total_chars = sum(len(chunk['text']) for chunk in chunks)
#         avg_chars = total_chars / len(chunks) if chunks else 0
#         print(f"   Total characters: {total_chars:,}")
#         print(f"   Average chunk size: {avg_chars:.0f} chars")
        
#         print("\n--- Sample Chunk 1 ---")
#         if len(chunks) > 0:
#             print(json.dumps(chunks[0], indent=2, ensure_ascii=False)[:500])
            
#         print("\n--- Sample Chunk 2 ---")
#         if len(chunks) > 1:
#             print(json.dumps(chunks[1], indent=2, ensure_ascii=False)[:500])
            
#         print("\n--- Sample Chunk 10 ---")
#         if len(chunks) > 10:
#             print(json.dumps(chunks[10], indent=2, ensure_ascii=False)[:500])
            
#     except Exception as e:
#         print(f"\n❌ Error: {e}")
#         import traceback
#         traceback.print_exc()