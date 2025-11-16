from rest_framework import serializers
from .models import Document, KnowledgeGraph, GraphNode, GraphEdge


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'uploaded_at', 'processed']
        read_only_fields = ['uploaded_at', 'processed']


class GraphNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphNode
        fields = ['id', 'label', 'node_type', 'embedding']


class GraphEdgeSerializer(serializers.ModelSerializer):
    source_label = serializers.CharField(source='source.label', read_only=True)
    target_label = serializers.CharField(source='target.label', read_only=True)
    
    class Meta:
        model = GraphEdge
        fields = ['id', 'source', 'target', 'source_label', 'target_label', 'relationship', 'weight']


class KnowledgeGraphSerializer(serializers.ModelSerializer):
    nodes = GraphNodeSerializer(many=True, read_only=True)
    edges = GraphEdgeSerializer(many=True, read_only=True)
    document_title = serializers.CharField(source='document.title', read_only=True)
    
    class Meta:
        model = KnowledgeGraph
        fields = ['id', 'document', 'document_title', 'theme', 'graph_data', 
                  'visualization_image', 'created_at', 'nodes', 'edges']
        read_only_fields = ['created_at']
