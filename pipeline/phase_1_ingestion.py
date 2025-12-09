"""
Phase 1: Document Ingestion & Preprocessing
======================================================
Handles the loading of parsed Markdown files and segments them into 
context-aware chunks for the Triple Extraction phase.
"""

import os
import re
from typing import List, Dict, Tuple, Set
from pipeline.chunker import MarkdownChunker, PlainTextChunker
from pipeline.wenyanwen import WenyanTransformer
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # Import Progress Bar library

# CONFIGURE NUMBER OF THREADS
# With RTX 3080 10GB + Llama 3 8B, level 4-5 is optimal.
MAX_WORKERS = 5

# Token/length configuration defaults (aligned with Phase 1 integration doc)
# TOKEN_LIMIT = 4096
# INSTRUCTION_TOKEN_ESTIMATE = 200
# CHAR_TO_TOKEN_RATIO = 3.5


def load_and_segment_text(file_path: str, deduplicate: bool = True, use_real_llm: bool = False) -> List[Dict[str, any]]:
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
        
    # Parallel processing of all chunks
    total_chunks = len(raw_chunks)
    print(f"  🚀 Starting Parallel Transform on {total_chunks} segments with {MAX_WORKERS} threads...")
    print(f"  ⚡ GPU Utilization target: MAX POWER")
    
    transformed_chunks = [None] * total_chunks
    
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(raw_chunks))) as executor:
        # Submit all transformation tasks
        future_to_idx = {
            executor.submit(transformer.transform_single_segment, chunk["text"], use_real_llm): idx 
            for idx, chunk in enumerate(raw_chunks)
        }
        
        with tqdm(total=total_chunks, desc="  Transforming", unit="seg", ncols=100) as pbar:
            # Collect results as they complete
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    transformed_text = future.result()
                    transformed_chunks[idx] = {
                        **raw_chunks[idx],
                        "text": transformed_text
                    }
                except Exception as e:
                    pbar.write(f"  ✗ Error transforming chunk {idx}: {e}")
                    # Keep original text if transformation fails
                    transformed_chunks[idx] = raw_chunks[idx]
                finally:
                    pbar.update(1)
        
    print(f"\n  ✅ Parallel transformation complete! Processed {total_chunks} segments.")
                
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