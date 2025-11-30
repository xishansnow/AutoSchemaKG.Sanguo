"""
Ontology Loader Module
======================
Manages medical ontologies and provides search/matching capabilities
Supports: DOID, HPO, MeSH, RxNorm
"""

from typing import Dict, List, Optional
from pipeline.ontology_parser import OntologyParser


class OntologyLoader:
    """Manages loaded ontologies and provides search/matching."""
    
    def __init__(self, ontology_dir: str = "ontologies"):
        self.ontology_dir = ontology_dir
        self.ontologies = {}
        self.loaded = False
        self.parser = OntologyParser(ontology_dir)
        
        self._load_all_ontologies()
    
    def _load_all_ontologies(self) -> None:
        """Load all ontologies using the parser."""
        self.ontologies = self.parser.load_all_ontologies()
        self.loaded = len(self.ontologies) > 0
    
    def search_concept(self, concept: str, ontology_name: Optional[str] = None) -> List[Dict]:
        """Search for a concept across ontologies."""
        if not self.loaded:
            return []
        
        results = []
        search_term = concept.lower()
        
        # Determine which ontologies to search
        ontologies_to_search = (
            {ontology_name: self.ontologies[ontology_name]} 
            if ontology_name and ontology_name in self.ontologies 
            else self.ontologies
        )
        
        for ont_name, ont_data in ontologies_to_search.items():
            if isinstance(ont_data, dict):
                for key, entry in ont_data.items():
                    # Search in multiple fields
                    search_fields = [
                        entry.get('name', '').lower(),
                        entry.get('label', '').lower(),
                        entry.get('description', '').lower(),
                        entry.get('id', '').lower()
                    ]
                    
                    if any(search_term in field for field in search_fields):
                        results.append({
                            'ontology': ont_name,
                            'ontology_id': key,
                            'data': entry,
                            'score': self._calculate_relevance_score(search_term, entry)
                        })
        
        # Sort by relevance score
        results.sort(key=lambda x: x['score'], reverse=True)
        return results
    
    def get_best_match(self, concept: str, threshold: float = 0.4) -> Optional[Dict]:
        """Get the best matching concept across all ontologies."""
        results = self.search_concept(concept)
        
        if results and results[0]['score'] >= threshold:
            best = results[0]
            return {
                'ontology': best['ontology'],
                'ontology_id': best['ontology_id'],
                'uri': best['data'].get('uri', ''),
                'label': best['data'].get('name') or best['data'].get('label') or concept,
                'score': best['score']
            }
        
        return None
    
    def get_all_matches(self, concept: str, threshold: float = 0.2) -> List[Dict]:
        """Get all matching concepts above threshold."""
        results = self.search_concept(concept)
        return [
            {
                'ontology': r['ontology'],
                'ontology_id': r['ontology_id'],
                'uri': r['data'].get('uri', ''),
                'label': r['data'].get('name') or r['data'].get('label') or concept,
                'score': r['score']
            }
            for r in results if r['score'] >= threshold
        ]
    
    def _calculate_relevance_score(self, search_term: str, entry: Dict) -> float:
        """Calculate relevance score (0-1)."""
        score = 0.0
        name = entry.get('name', '').lower()
        label = entry.get('label', '').lower()
        description = entry.get('description', '').lower()
        
        # Exact match
        if search_term == name or search_term == label:
            score = 1.0
        # Partial match in name/label
        elif search_term in name or search_term in label:
            score = 0.8
        # Word boundary match
        elif f' {search_term}' in f' {name}' or f' {search_term}' in f' {label}':
            score = 0.7
        # Match in description
        elif search_term in description:
            score = 0.5
        
        return score
    
    def list_ontologies(self) -> List[str]:
        """List all loaded ontologies."""
        return list(self.ontologies.keys())
    
    def get_ontology_stats(self) -> Dict:
        """Get statistics about loaded ontologies."""
        return {
            name: len(ont_data) if isinstance(ont_data, dict) else 0
            for name, ont_data in self.ontologies.items()
        }