# 📘 Learning & Wellbeing Hub – Backend API

The **Learning & Wellbeing Hub** backend is a Django REST Framework API that powers user authentication, resource management, wellbeing tools, and secure communication with the frontend.  
It is designed with scalability, clean architecture, and production‑ready deployment in mind.

---

## 🚀 Project Overview

This backend provides the core logic and data services for the Learning & Wellbeing Hub platform.  
It includes:

- Secure JWT authentication  
- User registration and profile management  
- Admin‑level user controls  
- Resource (books/materials) management  
- Centralized API documentation  
- Deployment‑ready configuration (Render/Railway/Heroku)

The API integrates seamlessly with the React frontend.

---

## 🧩 Core Functionalities

### 🔐 Authentication & Authorization
- Register new users  
- Login with JWT access + refresh tokens  
- Refresh expired access tokens  
- Role support (student, admin, etc.)  
- Protected endpoints for authenticated users  
- Admin‑only permissions for sensitive operations  

### 👤 User Account Management
- Update email  
- Change password  
- Retrieve authenticated user profile  
- Admin CRUD operations on users  

### 📚 Resource Management
- List available learning resources  
- Add, update, or delete resources (admin only)  
- Clean serializer + viewset architecture  

### 📝 API Documentation
Generated automatically using **drf-spectacular**:

- OpenAPI schema  
- Swagger UI  
- Redoc UI  
- Example requests for every endpoint  

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django, Django REST Framework |
| Auth | JWT (SimpleJWT) |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Docs | drf-spectacular |
| Deployment | Render / Railway / Heroku |
| Tools | Git, VS Code, Virtualenv |

---

## 📁 Project Structure

## 👤 Author

**Patrick Asamoah Adjei**  
ALX Africa – Back-End Development Program  
Focused on building secure, scalable, and production‑ready backend systems.
