# PDF OCR Text Extractor - Backend

A production-ready FastAPI backend for extracting text from PDFs and images using advanced OCR technology.

## 🚀 Features

### Core Features
- ✅ **User Authentication**
  - Email/Password registration with OTP verification
  - Google OAuth integration
  - Secure session management
  - Password reset flow

- ✅ **OCR Processing**
  - Multi-page PDF support
  - Advanced image preprocessing pipeline
  - Support for JPG, PNG, TIFF, PDF
  - Real-time processing with confidence scores

- ✅ **Security**
  - Bcrypt password hashing
  - HTTPOnly secure cookies
  - CSRF protection
  - Rate limiting
  - SQL injection prevention

- ✅ **File Management**
  - Automatic file cleanup
  - File validation and sanitization
  - Temporary storage with UUID naming

## 📋 Prerequisites

- Python 3.11+
- Tesseract OCR
- PostgreSQL (production) or SQLite (development)
- Redis (optional for sessions)

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd pdf-ocr-extractor
```

### 2. Install Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng poppler-utils
```

**macOS:**
```bash
brew install tesseract poppler
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### 3. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 6. Initialize Database
```bash
# For SQLite (development)
python scripts/init_db.py

# For PostgreSQL (production)
alembic upgrade head
```

## 🏃 Running the Application

### Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop
docker-compose down
```

## 📁 Project Structure

```
pdf-ocr-extractor/
├── app/
│   ├── core/           # Core utilities (config, database, security)
│   ├── models/         # Database models
│   ├── schemas/        # Pydantic schemas
│   ├── routers/        # API endpoints
│   ├── services/       # Business logic
│   ├── middleware/     # Custom middleware
│   └── utils/          # Helper functions
├── static/            # Frontend assets
├── templates/         # HTML templates
├── uploads/           # Temporary file storage
├── logs/              # Application logs
├── tests/             # Test suite
├── docker/            # Docker configuration
├── main.py            # Application entry point
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variables template
└── README.md          # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/verify-email` - Verify email with OTP
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/google` - Google OAuth login
- `POST /api/auth/password-reset/request` - Request password reset
- `POST /api/auth/password-reset/confirm` - Confirm password reset

### Users
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update profile
- `POST /api/users/change-password` - Change password
- `DELETE /api/users/account` - Delete account

### OCR
- `POST /api/ocr/upload` - Upload and process document
- `GET /api/ocr/result/{job_id}` - Get OCR result
- `POST /api/ocr/export/{job_id}` - Export result as file
- `GET /api/ocr/languages` - Get supported languages

## 🔒 Security Features

1. **Password Security**
   - Bcrypt hashing with cost factor 12
   - Password strength validation
   - Account lockout after failed attempts

2. **Session Management**
   - Secure HTTPOnly cookies
   - 7-day session duration
   - Session rotation on privilege escalation

3. **Rate Limiting**
   - 5 login attempts per 15 minutes
   - 3 OTP requests per hour
   - 100 general requests per 15 minutes

4. **Data Protection**
   - HTTPS enforcement in production
   - CSRF protection
   - XSS prevention
   - SQL injection prevention

## 📧 Email Configuration

### Gmail Setup
1. Enable 2-factor authentication
2. Generate app-specific password
3. Update .env:
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### SendGrid Setup
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## 📊 Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🚀 Deployment

### Environment Variables
Set these in production:
- `DEBUG=False`
- `SECRET_KEY=<strong-random-key>`
- `DATABASE_URL=<production-database-url>`
- `ALLOWED_HOSTS=<your-domain>`

### Using Docker
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment
1. Set up PostgreSQL database
2. Configure environment variables
3. Run migrations: `alembic upgrade head`
4. Start with Gunicorn: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`
5. Set up Nginx as reverse proxy

## 📝 Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `SECRET_KEY` - Application secret key
- `DATABASE_URL` - Database connection string
- `SMTP_*` - Email configuration
- `GOOGLE_CLIENT_ID/SECRET` - OAuth credentials
- `TESSERACT_CMD` - Path to Tesseract binary

## 🐛 Troubleshooting

### Tesseract not found
```bash
# Check if installed
tesseract --version

# Set path in .env
TESSERACT_CMD=/usr/local/bin/tesseract  # macOS
TESSERACT_CMD=/usr/bin/tesseract        # Linux
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe  # Windows
```

### Database connection errors
```bash
# SQLite: Check file permissions
chmod 644 ocr_app.db

# PostgreSQL: Test connection
psql -h localhost -U ocr_user -d ocr_database
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📄 License

MIT License - See LICENSE file for details

## 👥 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📞 Support

For issues and questions:
- GitHub Issues: <repository-url>/issues
- Email: support@pdfocr.com

## 🎯 Roadmap

- [ ] Document history and search
- [ ] Batch processing
- [ ] Multiple language support UI
- [ ] Export to DOCX/PDF
- [ ] API rate limiting tiers
- [ ] Admin dashboard
- [ ] Webhook notifications
