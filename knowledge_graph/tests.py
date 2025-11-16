from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Document, KnowledgeGraph, GraphNode, GraphEdge
from .graph_extractor import KnowledgeGraphExtractor
import io


class KnowledgeGraphExtractorTestCase(TestCase):
    """Test cases for the knowledge graph extractor"""
    
    def setUp(self):
        self.extractor = KnowledgeGraphExtractor()
        self.test_text = """
        Python is a programming language.
        Django uses Python for web development.
        Machine Learning requires Python.
        """
    
    def test_extract_entities(self):
        """Test entity extraction from text"""
        entities = self.extractor.extract_entities(self.test_text)
        self.assertIn("Python", entities)
        self.assertIn("Django", entities)
        self.assertGreater(len(entities), 0)
    
    def test_build_graph(self):
        """Test graph construction"""
        graph = self.extractor.build_graph(self.test_text, "Technology")
        self.assertGreater(graph.number_of_nodes(), 0)
        self.assertIn("Python", graph.nodes())
    
    def test_graph_to_json(self):
        """Test graph JSON conversion"""
        graph = self.extractor.build_graph(self.test_text, "Technology")
        json_data = self.extractor.graph_to_json(graph)
        self.assertIn("nodes", json_data)
        self.assertIn("edges", json_data)
        self.assertIn("metadata", json_data)
        self.assertEqual(json_data["metadata"]["node_count"], graph.number_of_nodes())


class DocumentModelTestCase(TestCase):
    """Test cases for Document model"""
    
    def test_document_creation(self):
        """Test creating a document"""
        doc = Document.objects.create(
            title="Test Document",
            processed=False
        )
        self.assertEqual(doc.title, "Test Document")
        self.assertFalse(doc.processed)


class APITestCase(TestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        self.client = Client()
    
    def test_api_overview(self):
        """Test API root endpoint"""
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # API root returns router endpoints
        self.assertIn("documents", data)
        self.assertIn("knowledge-graphs", data)
    
    def test_document_list(self):
        """Test document list endpoint"""
        response = self.client.get('/api/documents/')
        self.assertEqual(response.status_code, 200)
