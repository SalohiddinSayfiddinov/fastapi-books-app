# FastAPI Books App

A FastAPI application for managing books, authors, categories, and vendors with user authentication.

## Features

- User authentication with email verification
- Password reset functionality
- JWT token-based authentication
- PostgreSQL database integration
- RESTful API endpoints

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL (with SQLite for development)
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens
- **Password Hashing**: bcrypt
- **Migrations**: Alembic

## Local Development Setup

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd fastapi-books-app
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
# Run migrations
alembic upgrade head

# Or use the setup script
python setup_database.py
```

5. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

## Environment Variables

Create a `.env` file in the root directory:

```env
# Database URL (for production)
DATABASE_URL=postgresql://username:password@host:port/database_name

# JWT Secret Key (change this in production)
SECRET_KEY=your-secret-key-here
```

## Deployment on Render.com

### 1. Database Setup

1. Create a new PostgreSQL database on Render.com
2. Copy the database URL from Render dashboard
3. Add it as an environment variable in your web service

### 2. Web Service Setup

1. Connect your GitHub repository to Render
2. Configure the service:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     - `DATABASE_URL`: Your PostgreSQL database URL from Render

### 3. Database Migration

After deployment, run database migrations:

```bash
# In Render shell or locally with DATABASE_URL set
alembic upgrade head
```

## API Endpoints

### Authentication

- `POST /auth/signup` - Register a new user
- `POST /auth/verify` - Verify email with OTP
- `POST /auth/login` - Login user
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/verify-password-reset-otp` - Verify password reset OTP
- `POST /auth/reset-password` - Reset password

## Database Schema

### Users Table

- `id`: Primary key
- `email`: Unique email address
- `name`: User's full name
- `hashed_password`: Encrypted password
- `is_verified`: Email verification status
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp 