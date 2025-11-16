from django.contrib import admin
from .models import Document, KnowledgeGraph, GraphNode, GraphEdge


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'processed']
    list_filter = ['processed', 'uploaded_at']
    search_fields = ['title']


@admin.register(KnowledgeGraph)
class KnowledgeGraphAdmin(admin.ModelAdmin):
    list_display = ['document', 'theme', 'created_at']
    list_filter = ['created_at']
    search_fields = ['document__title', 'theme']


@admin.register(GraphNode)
class GraphNodeAdmin(admin.ModelAdmin):
    list_display = ['label', 'node_type', 'graph']
    list_filter = ['node_type']
    search_fields = ['label']


@admin.register(GraphEdge)
class GraphEdgeAdmin(admin.ModelAdmin):
    list_display = ['source', 'relationship', 'target', 'weight']
    list_filter = ['relationship']
    search_fields = ['source__label', 'target__label']
