"""
Knowledge Graph Extraction Module
Extracts entities and relationships from PDF documents and creates knowledge graphs.
"""
import re
import json
import io
from typing import List, Dict, Tuple, Set
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader


class KnowledgeGraphExtractor:
    """Extract knowledge graphs from text using simple NLP techniques"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.entities = set()
        self.relationships = []
        
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text content from PDF file"""
        try:
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")
    
    def extract_entities(self, text: str) -> Set[str]:
        """
        Extract entities from text using simple patterns.
        Looks for capitalized words and common noun phrases.
        """
        # Split text into sentences
        sentences = re.split(r'[.!?]+', text)
        entities = set()
        
        for sentence in sentences:
            # Find capitalized words (potential entities)
            words = sentence.split()
            for i, word in enumerate(words):
                # Clean word
                clean_word = re.sub(r'[^\w\s]', '', word)
                
                # Add capitalized words (likely proper nouns)
                if clean_word and clean_word[0].isupper() and len(clean_word) > 2:
                    # Skip common sentence starters
                    if i == 0 and clean_word.lower() in ['the', 'a', 'an', 'this', 'that']:
                        continue
                    entities.add(clean_word)
                
                # Look for multi-word entities (consecutive capitalized words)
                if i < len(words) - 1:
                    next_word = re.sub(r'[^\w\s]', '', words[i + 1])
                    if next_word and next_word[0].isupper():
                        multi_word = f"{clean_word} {next_word}"
                        if len(multi_word) > 5:
                            entities.add(multi_word)
        
        return entities
    
    def extract_relationships(self, text: str, entities: Set[str]) -> List[Tuple[str, str, str]]:
        """
        Extract relationships between entities.
        Simple pattern matching for common relationship verbs.
        """
        relationships = []
        relationship_verbs = [
            'is', 'are', 'was', 'were', 'has', 'have', 'had',
            'uses', 'use', 'used', 'contains', 'contain', 'includes', 'include',
            'requires', 'require', 'provides', 'provide', 'enables', 'enable',
            'creates', 'create', 'supports', 'support', 'implements', 'implement',
            'extends', 'extend', 'inherits', 'inherit', 'depends', 'depend'
        ]
        
        sentences = re.split(r'[.!?]+', text)
        entities_list = list(entities)
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Find entities in this sentence
            found_entities = [e for e in entities_list if e.lower() in sentence_lower]
            
            if len(found_entities) >= 2:
                # Find relationship verb
                for verb in relationship_verbs:
                    pattern = r'\b' + verb + r'\b'
                    if re.search(pattern, sentence_lower):
                        # Create relationships between entities
                        for i in range(len(found_entities) - 1):
                            source = found_entities[i]
                            target = found_entities[i + 1]
                            relationships.append((source, verb, target))
                        break
        
        return relationships
    
    def build_graph(self, text: str, theme: str = "") -> nx.DiGraph:
        """Build a NetworkX graph from extracted entities and relationships"""
        # Extract entities and relationships
        entities = self.extract_entities(text)
        relationships = self.extract_relationships(text, entities)
        
        # Create graph
        graph = nx.DiGraph()
        
        # Add nodes
        for entity in entities:
            graph.add_node(entity, node_type='entity', theme=theme)
        
        # Add edges
        for source, relationship, target in relationships:
            if source in entities and target in entities:
                graph.add_edge(source, target, relationship=relationship, weight=1.0)
        
        return graph
    
    def visualize_graph(self, graph: nx.DiGraph, output_path: str = None, 
                       theme: str = "", figsize=(12, 8)) -> str:
        """
        Visualize the knowledge graph using matplotlib.
        Returns the path to the saved image.
        """
        if graph.number_of_nodes() == 0:
            raise ValueError("Graph has no nodes to visualize")
        
        plt.figure(figsize=figsize)
        
        # Use spring layout for better visualization
        pos = nx.spring_layout(graph, k=2, iterations=50, seed=42)
        
        # Draw nodes
        nx.draw_networkx_nodes(graph, pos, node_color='lightblue', 
                              node_size=3000, alpha=0.9)
        
        # Draw labels
        nx.draw_networkx_labels(graph, pos, font_size=10, font_weight='bold')
        
        # Draw edges
        nx.draw_networkx_edges(graph, pos, edge_color='gray', 
                              arrows=True, arrowsize=20, width=2)
        
        # Draw edge labels (relationships)
        edge_labels = nx.get_edge_attributes(graph, 'relationship')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels, font_size=8)
        
        plt.title(f"Knowledge Graph{' - ' + theme if theme else ''}", 
                 fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, format='png', dpi=150, bbox_inches='tight')
        
        plt.close()
        return output_path
    
    def graph_to_json(self, graph: nx.DiGraph) -> Dict:
        """Convert NetworkX graph to JSON format for frontend"""
        nodes = []
        edges = []
        
        for node in graph.nodes():
            nodes.append({
                'id': node,
                'label': node,
                'type': graph.nodes[node].get('node_type', 'entity')
            })
        
        for source, target, data in graph.edges(data=True):
            edges.append({
                'source': source,
                'target': target,
                'relationship': data.get('relationship', 'related_to'),
                'weight': data.get('weight', 1.0)
            })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'metadata': {
                'node_count': graph.number_of_nodes(),
                'edge_count': graph.number_of_edges()
            }
        }
