"""
Visualization Utilities
=======================
Provides functions for visualizing and summarizing pipeline outputs.
"""

import networkx as nx
from typing import List, Dict, Set


def print_pipeline_summary(
    text_segments: List[str],
    all_triples: List[Dict],
    grounded_nodes: Dict[str, Dict],
    knowledge_graph: nx.MultiDiGraph
) -> None:
    """
    Print a comprehensive summary of the pipeline execution.
    
    Args:
        text_segments (List[str]): Input text segments
        all_triples (List[Dict]): Extracted triples
        grounded_nodes (Dict[str, Dict]): Grounded node data
        knowledge_graph (nx.MultiDiGraph): Final knowledge graph
    """
    print("=" * 80)
    print("PIPELINE EXECUTION SUMMARY")
    print("=" * 80)
    print()
    
    # Phase 1 Summary
    print("Phase 1 - Document Ingestion:")
    print(f"  • Text Segments: {len(text_segments)}")
    print(f"  • Total Characters: {sum(len(s) for s in text_segments)}")
    print()
    
    # Phase 2 Summary
    print("Phase 2 - Triple Extraction:")
    print(f"  • Total Triples: {len(all_triples)}")
    ee_triples = [t for t in all_triples if t['type'] == 'E-E']
    eev_triples = [t for t in all_triples if t['type'] == 'E-Ev']
    evev_triples = [t for t in all_triples if t['type'] == 'Ev-Ev']
    print(f"    - Entity-Entity (E-E): {len(ee_triples)}")
    print(f"    - Entity-Event (E-Ev): {len(eev_triples)}")
    print(f"    - Event-Event (Ev-Ev): {len(evev_triples)}")
    print()
    
    # Sample triples
    if ee_triples:
        print("  Sample E-E Triple:")
        sample = ee_triples[0]
        print(f"    ({sample['head']}) --[{sample['relation']}]--> ({sample['tail']})")
    if eev_triples:
        print("  Sample E-Ev Triple:")
        sample = eev_triples[0]
        print(f"    ({sample['head']}) --[{sample['relation']}]--> ({sample['tail']})")
    if evev_triples:
        print("  Sample Ev-Ev Triple:")
        sample = evev_triples[0]
        print(f"    ({sample['head']}) --[{sample['relation']}]--> ({sample['tail']})")
    print()
    
    # Phase 3 Summary
    print("Phase 3 - Schema Induction & Grounding:")
    print(f"  • Unique Nodes: {len(grounded_nodes)}")
    print(f"  • Concepts Induced: {len(grounded_nodes)}")
    print(f"  • Nodes Grounded: {len(grounded_nodes)}")
    print()
    
    # Sample grounded nodes
    sample_nodes = list(grounded_nodes.items())[:3]
    if sample_nodes:
        print("  Sample Grounded Nodes:")
        for node_name, data in sample_nodes:
            print(f"    • {node_name}")
            print(f"      - Concept: {data['induced_concept']}")
            print(f"      - Ontology ID: {data['ontology_id']}")
            print(f"      - Semantic Type: {data['semantic_type']}")
    print()
    
    # Phase 4 Summary
    print("Phase 4 - Knowledge Graph:")
    print(f"  • Total Nodes: {knowledge_graph.number_of_nodes()}")
    print(f"  • Total Edges: {knowledge_graph.number_of_edges()}")
    
    # Node type distribution
    entity_nodes = [n for n, d in knowledge_graph.nodes(data=True) if d.get('node_type') == 'entity']
    event_nodes = [n for n, d in knowledge_graph.nodes(data=True) if d.get('node_type') == 'event']
    print(f"    - Entity Nodes: {len(entity_nodes)}")
    print(f"    - Event Nodes: {len(event_nodes)}")
    
    # Graph connectivity
    is_connected = nx.is_weakly_connected(knowledge_graph)
    print(f"  • Weakly Connected: {'Yes' if is_connected else 'No'}")
    
    if knowledge_graph.number_of_nodes() > 0:
        # Most connected nodes
        degrees = dict(knowledge_graph.degree())
        top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"  • Most Connected Nodes:")
        for node, degree in top_nodes:
            print(f"    - {node}: {degree} connections")
    print()


def save_graph_visualization(kg: nx.MultiDiGraph, output_path: str) -> None:
    """
    Save a visualization of the knowledge graph.
    
    Args:
        kg (nx.MultiDiGraph): Knowledge graph to visualize
        output_path (str): Path to save the visualization
    """
    try:
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        import matplotlib.pyplot as plt
        
        # Create figure
        plt.figure(figsize=(16, 12))
        
        # Use spring layout for better node distribution
        if kg.number_of_nodes() > 0:
            pos = nx.spring_layout(kg, k=2, iterations=50, seed=42)
            
            # Separate entity and event nodes
            entity_nodes = [n for n, d in kg.nodes(data=True) if d.get('node_type') == 'entity']
            event_nodes = [n for n, d in kg.nodes(data=True) if d.get('node_type') == 'event']
            
            # Draw entity nodes
            nx.draw_networkx_nodes(
                kg, pos,
                nodelist=entity_nodes,
                node_color='lightblue',
                node_size=1000,
                alpha=0.8,
                label='Entity Nodes'
            )
            
            # Draw event nodes
            nx.draw_networkx_nodes(
                kg, pos,
                nodelist=event_nodes,
                node_color='lightcoral',
                node_size=1000,
                alpha=0.8,
                label='Event Nodes'
            )
            
            # Draw edges with different colors for triple types
            ee_edges = [(u, v) for u, v, d in kg.edges(data=True) if d.get('triple_type') == 'E-E']
            eev_edges = [(u, v) for u, v, d in kg.edges(data=True) if d.get('triple_type') == 'E-Ev']
            evev_edges = [(u, v) for u, v, d in kg.edges(data=True) if d.get('triple_type') == 'Ev-Ev']
            
            if ee_edges:
                nx.draw_networkx_edges(kg, pos, edgelist=ee_edges, edge_color='blue', 
                                      alpha=0.3, arrows=True, arrowsize=10, width=1.5)
            if eev_edges:
                nx.draw_networkx_edges(kg, pos, edgelist=eev_edges, edge_color='green',
                                      alpha=0.3, arrows=True, arrowsize=10, width=1.5)
            if evev_edges:
                nx.draw_networkx_edges(kg, pos, edgelist=evev_edges, edge_color='red',
                                      alpha=0.3, arrows=True, arrowsize=10, width=1.5)
            
            # Draw labels with smaller font
            nx.draw_networkx_labels(kg, pos, font_size=8, font_weight='bold')
            
            plt.title("Medical-SchemaKG: Onto-MedKG Knowledge Graph", fontsize=16, fontweight='bold')
            plt.legend(loc='upper left', fontsize=10)
            plt.axis('off')
            plt.tight_layout()
            
            # Save figure
            plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
        else:
            print("  ⚠ Graph is empty, skipping visualization")
            
    except ImportError:
        print("  ⚠ matplotlib not installed, skipping visualization")
        print("    Install with: pip install matplotlib")
    except Exception as e:
        print(f"  ⚠ Visualization failed: {e}")


def export_detailed_report(
    text_segments: List[str],
    all_triples: List[Dict],
    grounded_nodes: Dict[str, Dict],
    knowledge_graph: nx.MultiDiGraph,
    output_path: str
) -> None:
    """
    Export a detailed markdown report of the pipeline execution.
    
    Args:
        text_segments (List[str]): Input text segments
        all_triples (List[Dict]): Extracted triples
        grounded_nodes (Dict[str, Dict]): Grounded node data
        knowledge_graph (nx.MultiDiGraph): Final knowledge graph
        output_path (str): Path to save the report
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Medical-SchemaKG Pipeline Execution Report\n\n")
        
        # Phase 1
        f.write("## Phase 1: Document Ingestion\n\n")
        f.write(f"- **Text Segments**: {len(text_segments)}\n")
        f.write(f"- **Total Characters**: {sum(len(s) for s in text_segments)}\n\n")
        
        # Phase 2
        f.write("## Phase 2: Triple Extraction\n\n")
        f.write(f"- **Total Triples**: {len(all_triples)}\n")
        ee_triples = [t for t in all_triples if t['type'] == 'E-E']
        eev_triples = [t for t in all_triples if t['type'] == 'E-Ev']
        evev_triples = [t for t in all_triples if t['type'] == 'Ev-Ev']
        f.write(f"  - Entity-Entity (E-E): {len(ee_triples)}\n")
        f.write(f"  - Entity-Event (E-Ev): {len(eev_triples)}\n")
        f.write(f"  - Event-Event (Ev-Ev): {len(evev_triples)}\n\n")
        
        # List all triples
        f.write("### All Extracted Triples\n\n")
        for i, triple in enumerate(all_triples, 1):
            f.write(f"{i}. **[{triple['type']}]** ({triple['head']}) --[{triple['relation']}]--> ({triple['tail']})\n")
        f.write("\n")
        
        # Phase 3
        f.write("## Phase 3: Schema Induction & Grounding\n\n")
        f.write(f"- **Unique Nodes**: {len(grounded_nodes)}\n\n")
        
        f.write("### Grounded Nodes\n\n")
        f.write("| Node Name | Induced Concept | Ontology ID | Semantic Type |\n")
        f.write("|-----------|----------------|-------------|---------------|\n")
        for node_name, data in sorted(grounded_nodes.items()):
            f.write(f"| {node_name} | {data['induced_concept']} | {data['ontology_id']} | {data['semantic_type']} |\n")
        f.write("\n")
        
        # Phase 4
        f.write("## Phase 4: Knowledge Graph\n\n")
        f.write(f"- **Total Nodes**: {knowledge_graph.number_of_nodes()}\n")
        f.write(f"- **Total Edges**: {knowledge_graph.number_of_edges()}\n")
        is_connected = nx.is_weakly_connected(knowledge_graph)
        f.write(f"- **Weakly Connected**: {'Yes' if is_connected else 'No'}\n\n")
        
        if knowledge_graph.number_of_nodes() > 0:
            degrees = dict(knowledge_graph.degree())
            top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:10]
            f.write("### Most Connected Nodes\n\n")
            for node, degree in top_nodes:
                f.write(f"- **{node}**: {degree} connections\n")
    
    print(f"✓ Detailed report saved to: {output_path}")
