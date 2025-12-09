"""
LLM API Interface
=================
Provides unified interface for both stubbed and real LLM API calls.
Automatically routes to stub or real implementation based on configuration.
"""

from typing import Dict, List
from llm_api.stubs import (
    stub_call_llm_for_triples,
    stub_call_llm_for_concepts,
    stub_call_llm_for_wenyanwen
)
from llm_api.real_api import (
    real_call_llm_for_triples,
    real_call_llm_for_concepts,
    real_call_llm_for_wenyanwen
)


def call_llm_for_wenyanwen(text_segment: str, use_real_llm: bool = False) -> str:
    """
    Extract triples from a text segment using LLM.

    Routes to either stub or real implementation based on configuration.

    Args:
        text_segment (str): Text to extract triples from
        use_real_llm (bool): If True, use real API; if False, use stub

    Returns:
        str: Transformed text from Wenyanwen to Baihuawen
    """ 
    
    if use_real_llm:
        return real_call_llm_for_wenyanwen(text_segment)
    else:
        return stub_call_llm_for_wenyanwen(text_segment)


def call_llm_for_triples(text_segment: str, use_real_llm: bool = False) -> Dict:
    """
    Extract triples from a text segment using LLM.
    
    Routes to either stub or real implementation based on configuration.
    
    Args:
        text_segment (str): Text to extract triples from
        use_real_llm (bool): If True, use real API; if False, use stub
        
    Returns:
        Dict: Extracted triples in format:
            {
                'entity_entity': [
                    {'head': str, 'relation': str, 'tail': str, 'confidence': float}
                ],
                'entity_event': [...],
                'event_event': [...]
            }
    """
    if use_real_llm:
        return real_call_llm_for_triples(text_segment)
    else:
        return stub_call_llm_for_triples(text_segment)


def call_llm_for_concepts(node_list: List[str], use_real_llm: bool = False, triples_list: List[Dict] = None) -> Dict[
    str, str]:
    """
    Generate induced concepts for a list of nodes using LLM.
    
    Routes to either stub or real implementation based on configuration.
    Implements AutoSchemaKG approach with separate handling for entities and events.
    
    Args:
        node_list (List[str]): List of node names to generate concepts for
        use_real_llm (bool): If True, use real API; if False, use stub
        triples_list (List[Dict], optional): List of triples for context extraction (used in real mode)
        
    Returns:
        Dict[str, str]: Mapping of node name to induced concept phrases
            Example: {"Metformin": "medication, drug, pharmaceutical, treatment"}
    """
    if use_real_llm:
        return real_call_llm_for_concepts(node_list, triples_list)
    else:
        return stub_call_llm_for_concepts(node_list)
