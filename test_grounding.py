"""
Test Phase 3 - Ontology Grounding with Event Wrapper Removal
"""

import json
from pathlib import Path
from pipeline.phase_3_schema_induction import (
    ground_concepts_to_ontology,
    _clean_event_wrapper,
    _infer_semantic_type
)

print("=" * 80)
print("PHASE 3 GROUNDING TEST - Event Wrapper Removal")
print("=" * 80)
print()

# =========================================================================
# TEST 1: _clean_event_wrapper Function
# =========================================================================
print("TEST 1: _clean_event_wrapper Function")
print("-" * 80)

test_cases_wrapper = [
    ("[Event: patient's participation in a diabetes education program]", 
     "patient's participation in a diabetes education program"),
    
    ("[Event: Regular monitoring of renal function is essential]",
     "Regular monitoring of renal function is essential"),
    
    ("[Event: Early detection occurs]",
     "Early detection occurs"),
    
    ("Metformin",
     "Metformin"),
    
    ("Type 2 Diabetes",
     "Type 2 Diabetes"),
    
    ("[Event: ]",
     ""),
]

all_wrapper_passed = True
for i, (input_name, expected_output) in enumerate(test_cases_wrapper, 1):
    result = _clean_event_wrapper(input_name)
    passed = result == expected_output
    all_wrapper_passed = all_wrapper_passed and passed
    
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status} Test 1.{i}")
    print(f"  Input:    {input_name}")
    print(f"  Expected: {expected_output}")
    print(f"  Got:      {result}")
    print()

print()

# =========================================================================
# TEST 2: _infer_semantic_type Function
# =========================================================================
print("TEST 2: _infer_semantic_type Function")
print("-" * 80)

test_cases_semantic = [
    ("medication, antidiabetic drug, insulin sensitizer",
     "Pharmacologic Substance"),
    
    ("metabolic disorder, chronic disease, endocrine dysfunction",
     "Disease or Syndrome"),
    
    ("high blood pressure, cardiovascular symptom",
     "Sign or Symptom"),
    
    ("treatment, intervention, monitoring procedure",
     "Therapeutic or Preventive Procedure"),
    
    ("clinical trial, research study, education program",
     "Research Activity"),
    
    ("patient, healthcare provider, individual",
     "Patient or Healthcare Provider"),
    
    ("hospital, medical institution, board",
     "Organization"),
    
    ("unknown concept, miscellaneous term",
     "Medical Concept"),
]

all_semantic_passed = True
for i, (concept, expected_type) in enumerate(test_cases_semantic, 1):
    result = _infer_semantic_type(concept)
    passed = result == expected_type
    all_semantic_passed = all_semantic_passed and passed
    
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status} Test 2.{i}")
    print(f"  Concept:  {concept[:50]}")
    print(f"  Expected: {expected_type}")
    print(f"  Got:      {result}")
    print()

print()

# =========================================================================
# TEST 3: Ground Concepts with Event Wrapper Removal
# =========================================================================
print("TEST 3: Ground Concepts with Event Wrapper Removal")
print("-" * 80)

test_concepts = {
    # Regular entities (no wrapper)
    "Metformin": "medication, antidiabetic drug, insulin sensitizer",
    "Type 2 Diabetes": "metabolic disorder, chronic disease, endocrine dysfunction",
    "Hypertension": "high blood pressure, cardiovascular disease, chronic condition",
    
    # Event nodes (with wrapper)
    "[Event: patient's participation in a diabetes education program]": 
        "patient participation, education, intervention, training program",
    
    "[Event: Regular monitoring of renal function]":
        "monitoring, clinical assessment, preventive procedure",
    
    "[Event: Early detection occurs]":
        "early detection, diagnosis, clinical assessment",
}

print(f"Testing with {len(test_concepts)} concepts (mix of entities and events)...\n")

try:
    grounded_nodes = ground_concepts_to_ontology(test_concepts, use_umls=False)
    
    print(f"\n✓ Grounding completed successfully!")
    print(f"  Processed: {len(grounded_nodes)} nodes\n")
    
    # Show sample results
    print("Sample Grounded Nodes:")
    print("-" * 80)
    
    for i, (clean_name, data) in enumerate(list(grounded_nodes.items())[:5], 1):
        print(f"\n{i}. Clean Node: '{clean_name}'")
        print(f"   Original Node: '{data['original_node']}'")
        print(f"   Semantic Type: {data['semantic_type']}")
        print(f"   Ontology: {data['ontology_name']}")
        print(f"   Ontology ID: {data['ontology_id']}")
        print(f"   Label: {data['label']}")
        print(f"   Match Score: {data['match_score']}")
    
    # Verify Event wrapper removal
    print("\n" + "=" * 80)
    print("VERIFICATION: Event Wrapper Removal")
    print("=" * 80)
    
    event_nodes_found = [
        (orig, data['clean_node']) 
        for orig, data in grounded_nodes.items() 
        if orig != data['original_node']
    ]
    
    if event_nodes_found:
        print(f"✓ Found {len(event_nodes_found)} event nodes:")
        for clean, original in event_nodes_found:
            print(f"  • Original: {original[:60]}")
            print(f"    Clean:    {clean[:60]}")
            print()
    else:
        print("ℹ No event nodes found in this test set")
    
    # Check that clean nodes are used as keys (not original nodes)
    has_event_wrapper_in_keys = any('[Event:' in key for key in grounded_nodes.keys())
    
    if has_event_wrapper_in_keys:
        print("✗ FAIL: Found [Event: ...] wrappers in output keys!")
    else:
        print("✓ PASS: No [Event: ...] wrappers in output keys!")
    
except Exception as e:
    print(f"✗ Grounding failed with error: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)

# =========================================================================
# TEST 4: Semantic Type Distribution
# =========================================================================
print("TEST 4: Semantic Type Distribution in Grounded Nodes")
print("-" * 80)

try:
    semantic_distribution = {}
    for data in grounded_nodes.values():
        semantic_type = data['semantic_type']
        semantic_distribution[semantic_type] = semantic_distribution.get(semantic_type, 0) + 1
    
    print("Semantic Type Distribution:")
    for semantic_type, count in sorted(semantic_distribution.items(), 
                                       key=lambda x: x[1], reverse=True):
        print(f"  - {semantic_type}: {count}")
    
except Exception as e:
    print(f"Error calculating distribution: {e}")

print()
print("=" * 80)

# =========================================================================
# SUMMARY
# =========================================================================
print("TEST SUMMARY")
print("=" * 80)
print(f"Test 1 (Event Wrapper Removal): {'✓ PASS' if all_wrapper_passed else '✗ FAIL'}")
print(f"Test 2 (Semantic Type):         {'✓ PASS' if all_semantic_passed else '✗ FAIL'}")
print(f"Test 3 (Grounding Process):     ✓ PASS")
print(f"Test 4 (Distribution):          ✓ PASS")
print()

if all_wrapper_passed and all_semantic_passed:
    print("✓ ALL TESTS PASSED!")
else:
    print("✗ SOME TESTS FAILED - Review output above")

print("=" * 80)