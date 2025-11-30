"""
Stubbed LLM API Implementation
===============================
Provides mock/stub implementations of LLM API calls for testing and development.

These stubs return realistic, hard-coded data that allows the pipeline to run
without requiring an actual LLM API connection.
"""

from typing import Dict, List
import hashlib


def stub_call_llm_for_triples(text_segment: str) -> Dict:
    """
    STUB: Extract triples from text segment.
    
    Returns hard-coded mock triples that simulate LLM extraction results.
    The mock data is deterministic based on text content for consistency.
    
    Args:
        text_segment (str): Text to extract triples from
        
    Returns:
        Dict: Mock extracted triples
    """
    # Generate deterministic but varied responses based on text content
    text_hash = int(hashlib.md5(text_segment.encode()).hexdigest(), 16)
    variant = text_hash % 3
    
    if variant == 0:
        # Medical treatment scenario
        return {
            'entity_entity': [
                {
                    'head': 'Metformin',
                    'relation': 'treats',
                    'tail': 'Type 2 Diabetes',
                    'confidence': 0.95
                },
                {
                    'head': 'Metformin',
                    'relation': 'improves',
                    'tail': 'insulin sensitivity',
                    'confidence': 0.90
                }
            ],
            'entity_event': [
                {
                    'head': 'Patient',
                    'relation': 'participated_in',
                    'tail': 'Clinical Trial for Diabetes Management',
                    'confidence': 0.88
                }
            ],
            'event_event': [
                {
                    'head': 'Initial Diabetes Diagnosis',
                    'relation': 'led_to',
                    'tail': 'Metformin Treatment Initiation',
                    'confidence': 0.92
                }
            ]
        }
    elif variant == 1:
        # Cardiovascular scenario
        return {
            'entity_entity': [
                {
                    'head': 'ACE inhibitors',
                    'relation': 'reduce',
                    'tail': 'blood pressure',
                    'confidence': 0.93
                },
                {
                    'head': 'Hypertension',
                    'relation': 'increases_risk_of',
                    'tail': 'cardiovascular disease',
                    'confidence': 0.89
                }
            ],
            'entity_event': [
                {
                    'head': 'Diabetic patient',
                    'relation': 'underwent',
                    'tail': 'Cardiovascular Risk Assessment',
                    'confidence': 0.87
                }
            ],
            'event_event': [
                {
                    'head': 'Hypertension Detection',
                    'relation': 'triggered',
                    'tail': 'ACE Inhibitor Prescription',
                    'confidence': 0.91
                }
            ]
        }
    else:
        # Complication monitoring scenario
        return {
            'entity_entity': [
                {
                    'head': 'Diabetic nephropathy',
                    'relation': 'affects',
                    'tail': 'kidney function',
                    'confidence': 0.94
                },
                {
                    'head': 'Regular monitoring',
                    'relation': 'prevents',
                    'tail': 'end-stage renal disease',
                    'confidence': 0.86
                }
            ],
            'entity_event': [
                {
                    'head': 'Healthcare provider',
                    'relation': 'performed',
                    'tail': 'Renal Function Testing',
                    'confidence': 0.90
                }
            ],
            'event_event': [
                {
                    'head': 'Kidney Disease Detection',
                    'relation': 'enabled',
                    'tail': 'Timely Intervention',
                    'confidence': 0.88
                }
            ]
        }


def stub_call_llm_for_concepts(node_list: List[str]) -> Dict[str, str]:
    """
    STUB: Generate induced concepts for nodes.
    
    Returns hard-coded mock concept descriptions that simulate LLM analysis.
    Uses keyword matching to provide semi-realistic concepts.
    
    Args:
        node_list (List[str]): List of node names
        
    Returns:
        Dict[str, str]: Mapping of node to concept description
    """
    induced_concepts = {}
    
    for node in node_list:
        node_lower = node.lower()
        
        # Medical drugs/medications
        if any(term in node_lower for term in ['metformin', 'insulin', 'ace inhibitor', 'statin']):
            induced_concepts[node] = "a type of pharmaceutical medication"
        
        # Diseases/conditions
        elif any(term in node_lower for term in ['diabetes', 'hypertension', 'nephropathy', 'disease', 'syndrome']):
            induced_concepts[node] = "a medical disease or disorder"
        
        # Symptoms/signs
        elif any(term in node_lower for term in ['blood pressure', 'blood sugar', 'glucose', 'symptom']):
            induced_concepts[node] = "a physiological sign or symptom"
        
        # Procedures/tests
        elif any(term in node_lower for term in ['monitoring', 'testing', 'assessment', 'diagnosis', 'screening']):
            induced_concepts[node] = "a medical diagnostic or monitoring procedure"
        
        # Clinical activities (events)
        elif any(term in node_lower for term in ['trial', 'treatment', 'intervention', 'prescription', 'initiation']):
            induced_concepts[node] = "a clinical intervention or treatment activity"
        
        # Patient/people
        elif any(term in node_lower for term in ['patient', 'provider', 'individual']):
            induced_concepts[node] = "a person or healthcare stakeholder"
        
        # Body parts/systems
        elif any(term in node_lower for term in ['kidney', 'liver', 'heart', 'function', 'tissue']):
            induced_concepts[node] = "a body part or physiological system"
        
        # Risk factors
        elif any(term in node_lower for term in ['risk', 'sensitivity', 'resistance']):
            induced_concepts[node] = "a health risk factor or biological mechanism"
        
        # Default for unmatched terms
        else:
            induced_concepts[node] = "a medical concept"
    
    return induced_concepts


def stub_call_llm_for_wenyanwen(text_segment: str) -> Dict:
    """
    STUB: Extract triples from text segment.

    Returns hard-coded mock triples that simulate LLM extraction results.
    The mock data is deterministic based on text content for consistency.

    Args:
        text_segment (str): Text to extract triples from

    Returns:
        Dict: Mock extracted triples
    """
    # Generate deterministic but varied responses based on text content
    text_hash = int(hashlib.md5(text_segment.encode()).hexdigest(), 16)
    variant = text_hash % 3

    if variant == 0:
        # Medical treatment scenario
        return {
            'entity_entity': [
                {
                    'head': 'Metformin',
                    'relation': 'treats',
                    'tail': 'Type 2 Diabetes',
                    'confidence': 0.95
                },
                {
                    'head': 'Metformin',
                    'relation': 'improves',
                    'tail': 'insulin sensitivity',
                    'confidence': 0.90
                }
            ],
            'entity_event': [
                {
                    'head': 'Patient',
                    'relation': 'participated_in',
                    'tail': 'Clinical Trial for Diabetes Management',
                    'confidence': 0.88
                }
            ],
            'event_event': [
                {
                    'head': 'Initial Diabetes Diagnosis',
                    'relation': 'led_to',
                    'tail': 'Metformin Treatment Initiation',
                    'confidence': 0.92
                }
            ]
        }
    elif variant == 1:
        # Cardiovascular scenario
        return {
            'entity_entity': [
                {
                    'head': 'ACE inhibitors',
                    'relation': 'reduce',
                    'tail': 'blood pressure',
                    'confidence': 0.93
                },
                {
                    'head': 'Hypertension',
                    'relation': 'increases_risk_of',
                    'tail': 'cardiovascular disease',
                    'confidence': 0.89
                }
            ],
            'entity_event': [
                {
                    'head': 'Diabetic patient',
                    'relation': 'underwent',
                    'tail': 'Cardiovascular Risk Assessment',
                    'confidence': 0.87
                }
            ],
            'event_event': [
                {
                    'head': 'Hypertension Detection',
                    'relation': 'triggered',
                    'tail': 'ACE Inhibitor Prescription',
                    'confidence': 0.91
                }
            ]
        }
    else:
        # Complication monitoring scenario
        return {
            'entity_entity': [
                {
                    'head': 'Diabetic nephropathy',
                    'relation': 'affects',
                    'tail': 'kidney function',
                    'confidence': 0.94
                },
                {
                    'head': 'Regular monitoring',
                    'relation': 'prevents',
                    'tail': 'end-stage renal disease',
                    'confidence': 0.86
                }
            ],
            'entity_event': [
                {
                    'head': 'Healthcare provider',
                    'relation': 'performed',
                    'tail': 'Renal Function Testing',
                    'confidence': 0.90
                }
            ],
            'event_event': [
                {
                    'head': 'Kidney Disease Detection',
                    'relation': 'enabled',
                    'tail': 'Timely Intervention',
                    'confidence': 0.88
                }
            ]
        }

