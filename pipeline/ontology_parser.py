"""
Ontology Parser Module
======================
Parses multiple ontology formats: RDF/XML, Turtle
Converts to unified format for searching and matching
"""

import re
from typing import Dict
from pathlib import Path


class OntologyParser:
    """
    Universal parser for different ontology formats.
    Supports: RDF/XML (.xrdf), Turtle (.ttl)
    """
    
    def __init__(self, ontology_dir: str = "ontologies"):
        self.ontology_dir = ontology_dir
        self.ontologies = {}
        self.format_handlers = {
            '.xrdf': self._parse_rdf_xml,
            '.ttl': self._parse_turtle,
            '.owl': self._parse_rdf_xml,
        }
    
    def load_all_ontologies(self) -> Dict[str, Dict]:
        """Load all ontology files and convert to unified format."""
        ontology_path = Path(self.ontology_dir)
        
        if not ontology_path.exists():
            print(f"⚠ Ontology directory not found: {self.ontology_dir}")
            return {}
        
        print(f"  Scanning ontology directory: {self.ontology_dir}")
        
        for file in sorted(ontology_path.iterdir()):
            if file.is_file() and file.suffix in self.format_handlers:
                ont_name = file.stem.upper()
                try:
                    print(f"    Loading {ont_name} ({file.suffix})...", end=" ", flush=True)
                    handler = self.format_handlers[file.suffix]
                    ont_data = handler(str(file))
                    self.ontologies[ont_name] = ont_data
                    print(f"✓ ({len(ont_data)} concepts)")
                except Exception as e:
                    print(f"✗ Error: {str(e)[:50]}")
        
        return self.ontologies
    
    def _parse_rdf_xml(self, file_path: str) -> Dict:
        """Parse RDF/XML ontology files (.xrdf, .owl)."""
        try:
            import rdflib
            g = rdflib.Graph()
            g.parse(file_path, format='xml')
            
            ontology_data = {}
            from rdflib.namespace import RDFS, SKOS
            
            for subject in g.subjects():
                subj_str = str(subject)
                
                # Get label
                labels = list(g.objects(subject, RDFS.label)) or \
                         list(g.objects(subject, SKOS.prefLabel))
                label = str(labels[0]) if labels else subj_str.split('/')[-1]
                
                # Get description
                comments = list(g.objects(subject, RDFS.comment)) or \
                          list(g.objects(subject, SKOS.definition))
                description = str(comments[0]) if comments else ""
                
                # Extract ID
                concept_id = subj_str.split('/')[-1].split('#')[-1]
                
                ontology_data[concept_id] = {
                    'name': label,
                    'label': label,
                    'uri': subj_str,
                    'description': description,
                    'id': concept_id
                }
            
            return ontology_data
            
        except ImportError:
            print(f"(rdflib not installed, using fallback)", end=" ", flush=True)
            return self._parse_rdf_xml_fallback(file_path)
        except Exception as e:
            print(f"(fallback: {str(e)[:30]})", end=" ", flush=True)
            return self._parse_rdf_xml_fallback(file_path)
    
    def _parse_rdf_xml_fallback(self, file_path: str) -> Dict:
        """Fallback: Simple regex-based RDF/XML parsing."""
        ontology_data = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract rdf:Description blocks
            descriptions = re.findall(
                r'<rdf:Description[^>]*rdf:about="([^"]+)"[^>]*>(.*?)</rdf:Description>',
                content,
                re.DOTALL
            )
            
            for uri, block in descriptions:
                concept_id = uri.split('/')[-1].split('#')[-1]
                
                # Extract label
                label_match = re.search(r'<(?:rdfs|skos):label[^>]*>([^<]+)</(?:rdfs|skos):label>', block)
                label = label_match.group(1) if label_match else concept_id
                
                # Extract comment
                comment_match = re.search(r'<(?:rdfs|skos):(?:comment|definition)[^>]*>([^<]+)</(?:rdfs|skos):(?:comment|definition)>', block)
                description = comment_match.group(1) if comment_match else ""
                
                ontology_data[concept_id] = {
                    'name': label,
                    'label': label,
                    'uri': uri,
                    'description': description,
                    'id': concept_id
                }
        
        except Exception as e:
            pass
        
        return ontology_data
    
    def _parse_turtle(self, file_path: str) -> Dict:
        """Parse Turtle (.ttl) ontology files."""
        try:
            import rdflib
            g = rdflib.Graph()
            g.parse(file_path, format='turtle')
            
            ontology_data = {}
            from rdflib.namespace import RDFS, SKOS
            
            for subject in g.subjects():
                subj_str = str(subject)
                
                # Get label
                labels = list(g.objects(subject, RDFS.label)) or \
                         list(g.objects(subject, SKOS.prefLabel))
                label = str(labels[0]) if labels else subj_str.split('/')[-1]
                
                # Get description
                comments = list(g.objects(subject, RDFS.comment)) or \
                          list(g.objects(subject, SKOS.definition))
                description = str(comments[0]) if comments else ""
                
                # Extract ID
                concept_id = subj_str.split('/')[-1].split('#')[-1]
                
                ontology_data[concept_id] = {
                    'name': label,
                    'label': label,
                    'uri': subj_str,
                    'description': description,
                    'id': concept_id
                }
            
            return ontology_data
            
        except ImportError:
            print(f"(rdflib not installed, using fallback)", end=" ", flush=True)
            return self._parse_turtle_fallback(file_path)
        except Exception as e:
            print(f"(fallback: {str(e)[:30]})", end=" ", flush=True)
            return self._parse_turtle_fallback(file_path)
    
    def _parse_turtle_fallback(self, file_path: str) -> Dict:
        """Fallback: Simple regex-based Turtle parsing."""
        ontology_data = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            current_uri = None
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Match URI lines
                uri_match = re.match(r'^(?:<([^>]+)>|(\w+):(\w+))', line)
                if uri_match:
                    if uri_match.group(1):
                        current_uri = uri_match.group(1)
                    else:
                        current_uri = f"{uri_match.group(2)}:{uri_match.group(3)}"
                    
                    concept_id = current_uri.split('/')[-1].split('#')[-1]
                    
                    if concept_id not in ontology_data:
                        ontology_data[concept_id] = {
                            'name': concept_id,
                            'label': concept_id,
                            'uri': current_uri,
                            'description': '',
                            'id': concept_id
                        }
                
                # Match labels
                if current_uri and ('rdfs:label' in line or 'skos:prefLabel' in line):
                    label_match = re.search(r'"([^"]+)"', line)
                    if label_match:
                        concept_id = current_uri.split('/')[-1].split('#')[-1]
                        ontology_data[concept_id]['label'] = label_match.group(1)
                        ontology_data[concept_id]['name'] = label_match.group(1)
        
        except Exception as e:
            pass
        
        return ontology_data