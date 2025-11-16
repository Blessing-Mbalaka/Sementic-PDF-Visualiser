# Setup Guide

This guide will help you set up and run the Knowledge Graph Visualizer application.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Blessing-Mbalaka/Sementic-PDF-Visualiser.git
cd Sementic-PDF-Visualiser
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Django 5.2.8
- Django REST Framework
- PyPDF2 (for PDF parsing)
- NetworkX (for graph operations)
- Matplotlib (for visualization)
- NumPy (for numerical operations)
- Pillow (for image handling)

### 4. Run Database Migrations

```bash
python manage.py migrate
```

This creates the SQLite database and all necessary tables.

### 5. Create a Superuser (Optional)

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Create Required Directories

```bash
mkdir -p media/documents media/visualizations
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:
- Main application: http://localhost:8000/
- Admin panel: http://localhost:8000/admin/
- API root: http://localhost:8000/api/

## Configuration

### Settings

Key settings are in `knowledge_graph_project/settings.py`:

- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Add your domain names for production
- `SECRET_KEY`: Generate a new secret key for production
- `DATABASES`: Configure your database (default is SQLite)

### Media Files

Uploaded PDFs are stored in `media/documents/`
Generated visualizations are stored in `media/visualizations/`

Make sure these directories have proper write permissions.

### Static Files

For production, collect static files:

```bash
python manage.py collectstatic
```

## Testing

Run the test suite:

```bash
python manage.py test
```

Run tests with verbosity:

```bash
python manage.py test -v 2
```

Run specific tests:

```bash
python manage.py test knowledge_graph.tests.KnowledgeGraphExtractorTestCase
```

## Development

### Code Style

The project follows PEP 8 style guidelines. You can check code style using:

```bash
pip install flake8
flake8 knowledge_graph/
```

### Database

To reset the database:

```bash
rm db.sqlite3
python manage.py migrate
```

### Clearing Media Files

To clear uploaded files and visualizations:

```bash
rm -rf media/documents/*
rm -rf media/visualizations/*
```

## Troubleshooting

### Import Errors

If you encounter import errors, make sure you've activated your virtual environment and installed all dependencies:

```bash
pip install -r requirements.txt
```

### Database Errors

If you encounter database errors, try:

```bash
python manage.py migrate --run-syncdb
```

### Permission Errors

Make sure the `media` directory is writable:

```bash
chmod -R 755 media/
```

### Port Already in Use

If port 8000 is already in use, specify a different port:

```bash
python manage.py runserver 8080
```

## Production Deployment

For production deployment:

1. **Set Environment Variables**:
   - Set `DEBUG=False`
   - Set a strong `SECRET_KEY`
   - Configure `ALLOWED_HOSTS`

2. **Use a Production Database**:
   - PostgreSQL (recommended)
   - MySQL
   - Other Django-supported databases

3. **Use a Production Server**:
   - Gunicorn
   - uWSGI
   - Nginx as reverse proxy

4. **Configure Static Files**:
   ```bash
   python manage.py collectstatic
   ```

5. **Set Up Media File Serving**:
   - Use a CDN or cloud storage (S3, Azure Blob, etc.)
   - Configure proper permissions

6. **Enable HTTPS**:
   - Use Let's Encrypt for free SSL certificates
   - Configure Django's security settings

7. **Configure Logging**:
   - Set up proper logging in settings.py
   - Monitor application logs

Example production settings snippet:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Support

For issues and questions:
- Check the README.md for general information
- See API_DOCUMENTATION.md for API details
- Open an issue on GitHub

## License

This project is open source and available under the MIT License.
