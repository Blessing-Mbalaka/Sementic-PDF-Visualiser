# Semantic PDF Visualizer

A modern Django web application that extracts knowledge graphs from PDF documents and visualizes them using NetworkX. This application provides an intuitive interface for uploading PDF documents, extracting entities and relationships, and creating interactive knowledge graph visualizations.

## Features

- 📄 **PDF Document Upload**: Upload PDF documents through a user-friendly web interface
- 🔍 **Knowledge Extraction**: Automatically extract entities and relationships from documents
- 📊 **Graph Visualization**: Interactive canvas-based visualization of knowledge graphs
- 🎨 **Theme Support**: Customize knowledge graphs with themes
- 🚀 **RESTful API**: Full API support for programmatic access
- 💾 **Persistent Storage**: Save and manage multiple documents and their graphs
- 📈 **Real-time Stats**: View graph statistics (nodes, edges, connections)

## Technology Stack

- **Backend**: Django 5.2.8, Django REST Framework
- **Graph Processing**: NetworkX
- **PDF Parsing**: PyPDF2
- **Visualization**: Matplotlib (backend), HTML5 Canvas (frontend)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite (default, configurable)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Blessing-Mbalaka/Sementic-PDF-Visualiser.git
cd Sementic-PDF-Visualiser
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser (optional, for admin access):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Access the application:
- Main app: http://localhost:8000/
- Admin panel: http://localhost:8000/admin/
- API: http://localhost:8000/api/

## Usage

### Web Interface

1. **Upload a Document**:
   - Select a PDF file
   - Enter a title (optional)
   - Click "Upload Document"

2. **Extract Knowledge Graph**:
   - Optionally specify a theme
   - Click "Extract Knowledge Graph"
   - View the generated visualization and statistics

3. **Browse Documents**:
   - View all uploaded documents in the "Recent Documents" section

### API Endpoints

#### Upload Document
```bash
POST /api/documents/
Content-Type: multipart/form-data

{
  "file": <pdf_file>,
  "title": "Document Title"
}
```

#### Process Document
```bash
POST /api/documents/{id}/process/
Content-Type: application/json

{
  "theme": "Technology"
}
```

#### List Documents
```bash
GET /api/documents/
```

#### Get Knowledge Graphs
```bash
GET /api/knowledge-graphs/
```

#### Get Graph Data
```bash
GET /api/knowledge-graphs/{id}/graph_data/
```

## Project Structure

```
Sementic-PDF-Visualiser/
├── knowledge_graph/              # Main Django app
│   ├── migrations/               # Database migrations
│   ├── templates/                # HTML templates
│   │   └── knowledge_graph/
│   │       └── index.html        # Main UI
│   ├── admin.py                  # Admin configuration
│   ├── graph_extractor.py        # Knowledge graph extraction logic
│   ├── models.py                 # Database models
│   ├── serializers.py            # API serializers
│   ├── urls.py                   # App URL configuration
│   └── views.py                  # View functions and API endpoints
├── knowledge_graph_project/      # Django project settings
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Main URL configuration
│   └── wsgi.py                   # WSGI configuration
├── media/                        # Uploaded files and visualizations
├── static/                       # Static files
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## How It Works

1. **PDF Text Extraction**: Uses PyPDF2 to extract text content from uploaded PDF files

2. **Entity Recognition**: Identifies entities using simple NLP patterns:
   - Capitalized words (proper nouns)
   - Multi-word entities
   - Filters common sentence starters

3. **Relationship Extraction**: Finds relationships between entities:
   - Detects relationship verbs (is, has, uses, contains, etc.)
   - Connects entities appearing in the same sentence

4. **Graph Construction**: Creates a NetworkX directed graph:
   - Entities become nodes
   - Relationships become edges
   - Stores metadata (theme, types, weights)

5. **Visualization**:
   - Backend: Matplotlib generates static PNG images
   - Frontend: HTML5 Canvas renders interactive visualizations

## API Examples

### Python
```python
import requests

# Upload document
with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/documents/',
        files={'file': f},
        data={'title': 'My Document'}
    )
doc_id = response.json()['id']

# Process document
response = requests.post(
    f'http://localhost:8000/api/documents/{doc_id}/process/',
    json={'theme': 'Science'}
)
graph_data = response.json()
```

### JavaScript
```javascript
// Upload document
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('title', 'My Document');

const uploadResponse = await fetch('/api/documents/', {
    method: 'POST',
    body: formData
});
const doc = await uploadResponse.json();

// Process document
const processResponse = await fetch(`/api/documents/${doc.id}/process/`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ theme: 'Science' })
});
const graphData = await processResponse.json();
```

## Development

### Running Tests
```bash
python manage.py test
```

### Linting
```bash
# Install flake8
pip install flake8

# Run linter
flake8 knowledge_graph/
```

## Future Enhancements

- [ ] Advanced NLP using spaCy or transformers
- [ ] Semantic embeddings with sentence-transformers
- [ ] Interactive graph manipulation (drag, zoom, filter)
- [ ] Graph export (JSON, GraphML, etc.)
- [ ] Multi-document graph merging
- [ ] Search and filter capabilities
- [ ] User authentication and authorization
- [ ] Graph analytics and metrics

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with Django and Django REST Framework
- Graph processing powered by NetworkX
- PDF parsing with PyPDF2
- Inspired by knowledge graph concepts from the gnkadimeng/knowledgeEcosystem repository
