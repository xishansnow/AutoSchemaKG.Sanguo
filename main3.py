"""
Medical-SchemaKG - Resume Script (main3.py)
===========================================
Mode: RUN FROM START OF PHASE 3b (SKIP 3a)
Procedure: Load Phase 2 -> (Skip 3a) -> Phase 3b -> Phase 4
"""

import os
import sys
import json
import pickle
from pathlib import Path

# 1. Configure file paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 2. Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv(project_root / ".env")
    print("✓ Loaded .env file")
except ImportError:
    pass

from pipeline.phase_3_schema_induction import dynamically_induce_concepts, ground_concepts_to_ontology
from pipeline.phase_4_kg_construction import build_knowledge_graph, export_graph_to_neo4j_csv
from utils.visualization import save_graph_visualization

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
USE_REAL_LLM = os.getenv("USE_REAL_LLM", "false").lower() == "true"

# ===========================================================
# RUN CONFIGURATION
# True = Skip LLM run (3a), simulate data to run Phase 3b immediately
# False = Run full 3a -> 3b
SKIP_PHASE_3A = True 
# ===========================================================

def main():
    print("=" * 60)
    if SKIP_PHASE_3A:
        print("RESUMING PIPELINE: PHASE 2 -> [SKIP 3a] -> PHASE 3b -> 4")
    else:
        print("RESUMING PIPELINE: PHASE 2 -> PHASE 3a -> PHASE 3b -> 4")
    print("=" * 60)

    # ---------------------------------------------------------
    # STEP 1: LOAD DATA FROM PHASE 2 (CHECKPOINT)
    # ---------------------------------------------------------
    print("\n📂 [STEP 1] Loading Phase 2 Checkpoint...")
    
    possible_paths = [
        os.path.join(OUTPUT_DIR, "Phase2_Response.pkl"),
        os.path.join("pipeline", "Phase2_Response.pkl"),
        "Phase2_Response.pkl"
    ]
    
    checkpoint_path = None
    for p in possible_paths:
        if os.path.exists(p):
            checkpoint_path = p
            break
    
    if not checkpoint_path:
        print("❌ ERROR: Could not find 'Phase2_Response.pkl' file.")
        return

    try:
        with open(checkpoint_path, "rb") as f:
            data = pickle.load(f)
            
        if isinstance(data, dict):
            all_triples = data.get("all_triples", [])
            unique_nodes = data.get("unique_nodes", set())
        elif isinstance(data, list):
            print("⚠ Old list format data. Converting...")
            all_triples = data
            unique_nodes = set()
            for t in all_triples:
                unique_nodes.add(t['head'])
                unique_nodes.add(t['tail'])
        else:
            print("❌ Invalid pickle file format.")
            return

        print(f"✅ Loaded: {len(all_triples)} triples, {len(unique_nodes)} nodes.")

    except Exception as e:
        print(f"❌ Error reading pickle file: {e}")
        return

    # ---------------------------------------------------------
    # STEP 2: RUN (OR SIMULATE) PHASE 3a
    # ---------------------------------------------------------
    induced_concepts = {}

    if SKIP_PHASE_3A:
        print("\n⏩ [STEP 2] SKIPPING PHASE 3a (Concept Induction)...")
        print("   -> Creating simulated data to run Phase 3b immediately.")
        
        # Create mock dictionary: { "NodeName": "Medical Concept" }
        # This helps Phase 3b have input without waiting for LLM to run
        for node in unique_nodes:
            induced_concepts[node] = "Historical Concept"
            
        print(f"✅ Prepared {len(induced_concepts)} nodes for Grounding.")

    else:
        print("\n🚀 [STEP 2] RUNNING PHASE 3a: Concept Induction (LLM)...")
        try:
            induced_concepts = dynamically_induce_concepts(
                unique_nodes, 
                all_triples=all_triples,
                use_real_llm=USE_REAL_LLM
            )
        except Exception as e:
            print(f"❌ Error in Phase 3a: {e}")
            return

    # ---------------------------------------------------------
    # STEP 3: RUN PHASE 3b (ONTOLOGY GROUNDING)
    # ---------------------------------------------------------
    print("\n🚀 [STEP 3] RUNNING PHASE 3b: Ontology Grounding...")
    try:
        # This is the most important step you want to test
        grounded_nodes = ground_concepts_to_ontology(induced_concepts)
        
        # Lưu kết quả
        p3_out = os.path.join(OUTPUT_DIR, "Phase3_Response.json")
        with open(p3_out, "w", encoding="utf-8") as f:
            def default_ser(obj): return obj.__dict__ if hasattr(obj, '__dict__') else str(obj)
            json.dump(grounded_nodes, f, indent=2, ensure_ascii=False, default=default_ser)
        print(f"💾 Đã lưu Phase 3 Output: {p3_out}")
        
    except Exception as e:
        print(f"❌ Lỗi Phase 3b: {e}")
        import traceback
        traceback.print_exc()
        return

    # ---------------------------------------------------------
    # BƯỚC 4: CHẠY PHASE 4 (GRAPH CONSTRUCTION)
    # ---------------------------------------------------------
    print("\n🚀 [BƯỚC 4] CHẠY PHASE 4: Graph Construction...")
    try:
        kg = build_knowledge_graph(all_triples, grounded_nodes)
        print(f"✅ Graph created: {kg.number_of_nodes()} nodes, {kg.number_of_edges()} edges.")
        
        # Xuất ảnh
        viz_path = os.path.join(OUTPUT_DIR, "knowledge_graph_resumed.png")
        try:
            save_graph_visualization(kg, viz_path)
            print(f"🖼️ Visualization saved: {viz_path}")
        except: pass
        
        # Xuất Neo4j CSV
        try:
            export_graph_to_neo4j_csv(kg, OUTPUT_DIR)
            print("✅ Export Neo4j CSV thành công.")
        except: pass

    except Exception as e:
        print(f"❌ Lỗi Phase 4: {e}")

    print("\n✅ HOÀN TẤT!")

if __name__ == "__main__":
    main()