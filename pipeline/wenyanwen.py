"""
Wenyanwen Transform Module: Transform History Text from Wenyanwen to Baihuawen
============================================================
Handles the transformation of historical texts from Wenyanwen (Classical Chinese) to Baihuawen (Modern Chinese),
context-aware chunks for the Triple Extraction phase.
"""
import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from pipeline.chunker import MarkdownChunker, PlainTextChunker
from llm_api.interface import call_llm_for_wenyanwen
from tqdm import tqdm  # Import Progress Bar library


# CONFIGURE NUMBER OF THREADS
MAX_WORKERS = 5

# Replace hard-coded path with env-configurable path
LOG_DIR = Path(os.getenv("OUTPUT_DIR", "output"))
_WENYANWEN_API_LOG = Path(os.getenv("WENYANWEN_API_LOG", str(LOG_DIR / "wenyanwen_llm_calls.jsonl")))
_WENYANWEN_API_LOG.parent.mkdir(parents=True, exist_ok=True)

# Token/length configuration defaults 
TOKEN_LIMIT = 4096
INSTRUCTION_TOKEN_ESTIMATE = 200
CHAR_TO_TOKEN_RATIO = 3.5

def _append_wenyanwen_api_log(entry: dict):
    """Append one JSON line to output/wenyanwen_llm_calls.jsonl"""
    try:
        with open(_WENYANWEN_API_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        # never fail the extractor because of logging
        print(f"  ⚠ Warning: failed to write wenyanwen api log: {e}")

"""
Use LLM to convert classical Chinese (wenyanwen) text to modern Chinese (baihuawen)
"""
class WenyanTransformer:
    """
    Classical Chinese to Modern Chinese transformer
    """
    
    def __init__(self, use_real_llm: bool = False):
        """
        Initialize the transformer
        """
        self.use_real_llm = use_real_llm

    
    def transform_from_segments(self, text_segments: List[Dict]) -> Tuple[List[Dict], Set[str]]:
        """
        Extract triples from all text segments using Parallel Processing with Progress Bar.
        """
        self.all_triples = []
        self.unique_nodes = set()
        
        total_segments = len(text_segments)
        print(f"  🚀 Starting Parallel Extraction on {total_segments} segments with {MAX_WORKERS} threads...")
        print(f"  ⚡ GPU Utilization target: MAX POWER")

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit all tasks to the queue
            future_to_idx = {
                executor.submit(self.transform_single_segment, segment, idx): idx 
                for idx, segment in enumerate(text_segments, 1)
            }
            
            # Initialize Progress Bar (TQDM)
            # ncols=100: progress bar display width
            # unit='seg': counting unit is segment
            with tqdm(total=total_segments, desc="  Processing", unit="seg", ncols=100) as pbar:
                for future in as_completed(future_to_idx):
                    idx = future_to_idx[future]
                    
                    try:
                        # Get result from thread
                        segment_triples = future.result()
                        
                        if segment_triples:
                            self.all_triples.extend(segment_triples)
                            # Update status line with number of triples found in this segment
                            pbar.set_postfix_str(f"Found {len(segment_triples)} triples", refresh=False)
                        
                        # Increment progress by 1
                        pbar.update(1)
                        
                    except Exception as e:
                        # Use pbar.write to print errors without breaking the progress bar interface
                        pbar.write(f"  ✗ Error in segment {idx}: {e}")
                        pbar.update(1)

        print(f"\n  ✅ Parallel extraction complete! Processed {total_segments} segments.")

        # Aggregate unique nodes once at the end
        print("  Aggregating unique nodes...", end="\r")
        for triple in self.all_triples:
            self.unique_nodes.add(triple['head'])
            self.unique_nodes.add(triple['tail'])
            
        return self.all_triples, self.unique_nodes

    def transform_single_segment(self, segment, use_real_llm: bool = False) -> str:
        """
        Helper function to process a single segment (runs inside a thread).
        """
        
        # Call LLM API
        try:
            # Wenyanwenize input
            segment = call_llm_for_wenyanwen(segment, use_real_llm = use_real_llm)            
            
        except Exception as e:            
            status = "error"
            response_serialized = {"error": str(e)}                     
            print(f"  ⚠ Warning: failed to transfomr wenyanwen : {e}")
        
                
        return segment


# def convert_to_baihua(self, segment: Dict) -> Dict:
#         """
#         Convert classical Chinese (wenyanwen) to modern Chinese (baihua).
#         :param segment: Dictionary containing classical Chinese text, format: {'text': classical_text, ...}
#         :return: Dictionary containing modern Chinese text, format: {'text': modern_text, ...}
#         """
#         try:
#             # Extract classical Chinese text
#             wenyanwen_text = segment.get('text', '')

#             # Call LLM API for conversion
#             baihua_text = call_llm_for_wenyanwen(wenyanwen_text, use_real_llm=self.use_real_llm)

#             # Return converted result
#             return {**segment, 'text': baihua_text}
#         except Exception as e:
#             print(f"⚠ Classical Chinese conversion failed: {e}")
#             return {**segment, 'text': segment.get('text', '')}  # Preserve original text
        


# if __name__ == "__main__":
#     # Example usage
#     transformer = WenyanTransformer()
    
#     sample_text = "曹操字孟德,沛国谯人也。"
#     result = transformer.transform(sample_text)
#     print(f"Original text: {sample_text}")
#     print(f"Translated text: {result}")