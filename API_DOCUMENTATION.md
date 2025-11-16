# API Documentation

## Overview

The Knowledge Graph Visualizer provides a RESTful API for programmatic access to document upload, processing, and knowledge graph retrieval.

Base URL: `http://localhost:8000/api/`

## Authentication

Currently, the API does not require authentication. This is suitable for development and demo purposes. For production use, consider adding authentication using Django REST Framework's authentication classes.

## Endpoints

### 1. List Documents

**Endpoint:** `GET /api/documents/`

**Description:** Retrieve a list of all uploaded documents.

**Response:**
```json
[
  {
    "id": 1,
    "title": "Sample Document",
    "file": "http://localhost:8000/media/documents/sample.pdf",
    "uploaded_at": "2025-11-16T17:00:00Z",
    "processed": true
  }
]
```

### 2. Upload Document

**Endpoint:** `POST /api/documents/`

**Description:** Upload a new PDF document.

**Request:**
```bash
curl -X POST \
  -F "file=@document.pdf" \
  -F "title=My Document" \
  http://localhost:8000/api/documents/
```

**Response:**
```json
{
  "id": 1,
  "title": "My Document",
  "file": "http://localhost:8000/media/documents/document.pdf",
  "uploaded_at": "2025-11-16T17:00:00Z",
  "processed": false
}
```

### 3. Process Document

**Endpoint:** `POST /api/documents/{id}/process/`

**Description:** Process a document to extract its knowledge graph.

**Request:**
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"theme": "Technology"}' \
  http://localhost:8000/api/documents/1/process/
```

**Response:**
```json
{
  "id": 1,
  "document": 1,
  "document_title": "My Document",
  "theme": "Technology",
  "graph_data": {
    "nodes": [
      {"id": "Python", "label": "Python", "type": "entity"},
      {"id": "Django", "label": "Django", "type": "entity"}
    ],
    "edges": [
      {"source": "Django", "target": "Python", "relationship": "uses", "weight": 1.0}
    ],
    "metadata": {
      "node_count": 2,
      "edge_count": 1
    }
  },
  "visualization_image": "http://localhost:8000/media/visualizations/graph_1_Technology.png",
  "created_at": "2025-11-16T17:00:00Z",
  "nodes": [...],
  "edges": [...]
}
```

### 4. List Knowledge Graphs

**Endpoint:** `GET /api/knowledge-graphs/`

**Description:** Retrieve a list of all generated knowledge graphs.

**Response:**
```json
[
  {
    "id": 1,
    "document": 1,
    "document_title": "My Document",
    "theme": "Technology",
    "graph_data": {...},
    "visualization_image": "http://localhost:8000/media/visualizations/graph_1_Technology.png",
    "created_at": "2025-11-16T17:00:00Z",
    "nodes": [...],
    "edges": [...]
  }
]
```

### 5. Get Knowledge Graph

**Endpoint:** `GET /api/knowledge-graphs/{id}/`

**Description:** Retrieve a specific knowledge graph.

**Response:** Same as above for a single graph.

### 6. Get Graph Data

**Endpoint:** `GET /api/knowledge-graphs/{id}/graph_data/`

**Description:** Retrieve only the graph data in JSON format (nodes and edges).

**Response:**
```json
{
  "nodes": [
    {"id": "Python", "label": "Python", "type": "entity"},
    {"id": "Django", "label": "Django", "type": "entity"}
  ],
  "edges": [
    {"source": "Django", "target": "Python", "relationship": "uses", "weight": 1.0}
  ],
  "metadata": {
    "node_count": 2,
    "edge_count": 1
  }
}
```

## Error Handling

The API returns standard HTTP status codes:

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error responses include a JSON object with an `error` field:

```json
{
  "error": "No entities could be extracted from the document"
}
```

## Python Examples

```python
import requests

# Upload a document
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/documents/',
        files={'file': f},
        data={'title': 'My Document'}
    )
doc = response.json()

# Process the document
response = requests.post(
    f'http://localhost:8000/api/documents/{doc["id"]}/process/',
    json={'theme': 'Technology'}
)
graph = response.json()

# Get graph data
response = requests.get(
    f'http://localhost:8000/api/knowledge-graphs/{graph["id"]}/graph_data/'
)
graph_data = response.json()

print(f"Nodes: {graph_data['metadata']['node_count']}")
print(f"Edges: {graph_data['metadata']['edge_count']}")
```

## JavaScript Examples

```javascript
// Upload a document
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('title', 'My Document');

const uploadResponse = await fetch('http://localhost:8000/api/documents/', {
    method: 'POST',
    body: formData
});
const doc = await uploadResponse.json();

// Process the document
const processResponse = await fetch(`http://localhost:8000/api/documents/${doc.id}/process/`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ theme: 'Technology' })
});
const graph = await processResponse.json();

// Get graph data
const graphResponse = await fetch(`http://localhost:8000/api/knowledge-graphs/${graph.id}/graph_data/`);
const graphData = await graphResponse.json();

console.log(`Nodes: ${graphData.metadata.node_count}`);
console.log(`Edges: ${graphData.metadata.edge_count}`);
```

## Rate Limiting

Currently, there is no rate limiting implemented. For production use, consider adding rate limiting using Django REST Framework throttling classes.

## CORS

For cross-origin requests, you may need to configure CORS headers. Install `django-cors-headers` and add it to your settings:

```bash
pip install django-cors-headers
```

Add to `INSTALLED_APPS` and `MIDDLEWARE` in settings.py, and configure `CORS_ALLOWED_ORIGINS`.
