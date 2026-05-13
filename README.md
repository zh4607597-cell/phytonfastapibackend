# CRM Backend

This is the backend API for the CRM System, built with FastAPI and SQLAlchemy.

## 🚀 Getting Started

### Installation
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server
```bash
python -m uvicorn app.main:app --reload
```

## 🔐 Key Features

### Role-Based Access Control (RBAC)
The system features a robust RBAC implementation for managing user permissions across different features of the CRM.
- **Documentation**: See [RBAC_README.md](./RBAC_README.md) for detailed information on Roles, Features, and Permissions.

### API Documentation
Once the server is running, you can access the interactive API docs at:
- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`
