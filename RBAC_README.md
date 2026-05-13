# RBAC & User Permissions System

This document outlines the Role-Based Access Control (RBAC) architecture implemented in the CRM Backend. The system provides granular control over what functional areas (Features) different Roles or specific Users can access and modify.

## 🔑 Core Concepts

### 1. Roles
Roles are logical groupings of users (e.g., `Administrator`, `Agent`, `Manager`).
- **Storage**: `roles` table.
- **Attributes**: `role_name`, `description`.

### 2. Features
Features represent functional modules or pages in the application (e.g., `Leads`, `Customers`, `Invoices`).
- **Storage**: `features` table.
- **Attributes**: `feature_name`, `feature_key` (slug used for frontend checks), `path`, `icon`.

### 3. Permissions (Role-Based)
Defines what a **Role** can do with a **Feature**.
- **Storage**: `permissions` table.
- **Actions**:
  - `can_view`: Read access.
  - `can_create`: Permission to add new records.
  - `can_update`: Permission to edit existing records.
  - `can_delete`: Permission to remove records.

### 4. User Permissions (User-Specific)
Provides granular overrides or direct assignments for a **specific User** on a per-feature basis. This is useful for temporary access or unique responsibilities that don't fit a standard role.
- **Storage**: `user_permissions` table.

---

## 🚀 API Endpoints

All RBAC management endpoints are prefixed with `/rbac`.

### Roles Management
- `GET /rbac/roles` - List all roles.
- `POST /rbac/roles` - Create a new role.
- `PUT /rbac/roles/{id}` - Update role details.
- `DELETE /rbac/roles/{id}` - Delete a role.

### Features Management
- `GET /rbac/features` - List all available features.
- `POST /rbac/features` - Add a new feature module.
- `PUT /rbac/features/{id}` - Update feature metadata.

### Permissions Management
- `GET /rbac/permissions` - List all role-feature mappings.
- `POST /rbac/permissions` - Assign permissions to a role.
- `PUT /rbac/permissions/{id}` - Update existing role permissions.

### User Overrides
- `GET /rbac/user-permissions/user/{user_id}` - Get specific permissions for a user.
- `POST /rbac/user-permissions` - Assign specific permissions to a user.

---

## 🛠 Database Schema

The system uses SQLAlchemy models defined in `app/models/rbac_models.py`:

```python
# Permission structure example
{
    "role_id": 1,
    "feature_id": 5,
    "can_view": True,
    "can_create": True,
    "can_update": False,
    "can_delete": False
}
```

## 💡 Frontend Integration
The `feature_key` (e.g., `leads_management`) should be used by the frontend to conditionally render sidebars, buttons, or route guards based on the current user's permission set.
