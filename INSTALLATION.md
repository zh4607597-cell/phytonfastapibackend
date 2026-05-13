# CRM + ERP Integrated System - Installation Guide

## 1. Prerequisites
- **Python 3.9+**
- **Node.js 16+**
- **MySQL / MariaDB** (Current database system detected)
- **reportlab** (For PDF generation)
- **python-docx** (For Contract generation)
- **APScheduler** (For Recurring Invoice tasks)

## 2. Backend Setup
1. Navigate to `crm-backend/`.
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy pymysql reportlab python-docx apscheduler
   ```
3. Run the ERP migration scripts:
   ```bash
   # Add new columns to existing lead table
   python add_erp_cols_to_lead.py
   # Create new ERP tables (products, invoices, contracts, etc.)
   python migrate_erp.py
   ```
4. Start the backend:
   ```bash
   uvicorn app.main:app --reload
   ```

## 3. Frontend Setup
1. Navigate to `ERPSYSTEM/`.
2. Install dependencies:
   ```bash
   npm install axios react-icons react-router-dom
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## 4. Features & Usage
### Lead Management
- Access the enhanced CRM view via `/leads/crm/:id`.
- Tabs:
  - **Overview**: View lead details and notes.
  - **Products**: Dynamically add/remove products with real-time tax/discount calculations.
  - **Invoices**: Generate one-time or recurring invoices. Download as PDF.
  - **Contracts**: Generate DOCX contracts from templates with auto-filled placeholders.
  - **Activity**: Full timeline of all actions taken on the lead.

### Product Catalog
- Manage your global product/service list at `/products`.

### Invoices & Contracts
- Centralized management at `/invoices` and `/contracts`.
- Automated monthly recurring invoice generation (configured in `app/scheduler.py`).

## 5. Directory Structure
- `app/models/erp_models.py`: Database schemas for ERP modules.
- `app/services/erp_service.py`: Core business logic and document generation.
- `app/routes/erp_routes.py`: API endpoints for ERP integration.
- `app/scheduler.py`: Background tasks for recurring invoicing.
- `storage/`: Local filesystem storage for invoices, contracts, and templates.
