import os
from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.base import ContentFile
from .models import Document, KnowledgeGraph, GraphNode, GraphEdge
from .serializers import (
    DocumentSerializer, KnowledgeGraphSerializer,
    GraphNodeSerializer, GraphEdgeSerializer
)
from .graph_extractor import KnowledgeGraphExtractor


def index(request):
    """Main page view"""
    return render(request, 'knowledge_graph/index.html')


class DocumentViewSet(viewsets.ModelViewSet):
    """API endpoint for document management"""
    queryset = Document.objects.all().order_by('-uploaded_at')
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Process a document to extract knowledge graph"""
        document = self.get_object()
        theme = request.data.get('theme', '')
        
        try:
            # Extract knowledge graph
            extractor = KnowledgeGraphExtractor()
            
            # Open and read the PDF file
            document.file.open('rb')
            text = extractor.extract_text_from_pdf(document.file)
            document.file.close()
            
            # Build graph
            graph = extractor.build_graph(text, theme)
            
            if graph.number_of_nodes() == 0:
                return Response(
                    {'error': 'No entities could be extracted from the document'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create visualization
            vis_filename = f'graph_{document.id}_{theme or "default"}.png'
            vis_path = os.path.join(settings.MEDIA_ROOT, 'visualizations', vis_filename)
            os.makedirs(os.path.dirname(vis_path), exist_ok=True)
            
            extractor.visualize_graph(graph, vis_path, theme)
            
            # Convert graph to JSON
            graph_json = extractor.graph_to_json(graph)
            
            # Save knowledge graph
            kg = KnowledgeGraph.objects.create(
                document=document,
                theme=theme,
                graph_data=graph_json,
                visualization_image=f'visualizations/{vis_filename}'
            )
            
            # Save nodes and edges
            node_map = {}
            for node_data in graph_json['nodes']:
                node = GraphNode.objects.create(
                    graph=kg,
                    label=node_data['label'],
                    node_type=node_data['type']
                )
                node_map[node_data['id']] = node
            
            for edge_data in graph_json['edges']:
                source_node = node_map.get(edge_data['source'])
                target_node = node_map.get(edge_data['target'])
                if source_node and target_node:
                    GraphEdge.objects.create(
                        graph=kg,
                        source=source_node,
                        target=target_node,
                        relationship=edge_data['relationship'],
                        weight=edge_data['weight']
                    )
            
            # Mark document as processed
            document.processed = True
            document.save()
            
            serializer = KnowledgeGraphSerializer(kg)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class KnowledgeGraphViewSet(viewsets.ModelViewSet):
    """API endpoint for knowledge graph management"""
    queryset = KnowledgeGraph.objects.all().order_by('-created_at')
    serializer_class = KnowledgeGraphSerializer
    
    @action(detail=True, methods=['get'])
    def graph_data(self, request, pk=None):
        """Get graph data in JSON format for visualization"""
        kg = self.get_object()
        return Response(kg.graph_data)


@api_view(['GET'])
def api_overview(request):
    """API overview endpoint"""
    return Response({
        'endpoints': {
            'documents': '/api/documents/',
            'knowledge_graphs': '/api/knowledge-graphs/',
            'upload_document': '/api/documents/ (POST)',
            'process_document': '/api/documents/{id}/process/ (POST)',
            'get_graph_data': '/api/knowledge-graphs/{id}/graph_data/',
        },
        'version': '1.0.0'
    })
