from django.db import models
from django.utils import timezone


class Document(models.Model):
    """Model to store uploaded PDF documents"""
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


class KnowledgeGraph(models.Model):
    """Model to store knowledge graph data"""
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='graphs')
    theme = models.CharField(max_length=255, blank=True)
    graph_data = models.JSONField()  # Store NetworkX graph as JSON
    visualization_image = models.ImageField(upload_to='visualizations/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Graph for {self.document.title} - {self.theme}"


class GraphNode(models.Model):
    """Model to store individual nodes in the knowledge graph"""
    graph = models.ForeignKey(KnowledgeGraph, on_delete=models.CASCADE, related_name='nodes')
    label = models.CharField(max_length=255)
    node_type = models.CharField(max_length=100)
    embedding = models.JSONField(null=True, blank=True)  # Store normalized embeddings
    
    def __str__(self):
        return f"{self.label} ({self.node_type})"


class GraphEdge(models.Model):
    """Model to store edges/relationships in the knowledge graph"""
    graph = models.ForeignKey(KnowledgeGraph, on_delete=models.CASCADE, related_name='edges')
    source = models.ForeignKey(GraphNode, on_delete=models.CASCADE, related_name='outgoing_edges')
    target = models.ForeignKey(GraphNode, on_delete=models.CASCADE, related_name='incoming_edges')
    relationship = models.CharField(max_length=255)
    weight = models.FloatField(default=1.0)
    
    def __str__(self):
        return f"{self.source.label} -> {self.relationship} -> {self.target.label}"
