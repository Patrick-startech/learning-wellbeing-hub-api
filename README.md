# 🌱 Learning & Wellbeing Hub – Full‑Stack Project

The **Learning & Wellbeing Hub** is a full‑stack platform designed to support learners with curated educational resources, wellbeing tools, and personalized user experiences.  
This project includes both the **Django REST Framework backend** and the **React frontend**, working together to deliver a seamless, secure, and scalable application.

---

## 🚀 Project Overview

The Hub provides a centralized space where learners can:

- Access learning materials  
- Explore wellbeing resources  
- Manage their accounts  
- Track progress (future feature)  
- Interact with a clean, modern UI  

The system is built with a **modular architecture**, separating backend and frontend into independent but integrated services.

---

# 🧩 System Architecture

The backend exposes REST endpoints, while the frontend consumes them through a centralized API service layer.

---

# 🔐 Backend Features (Django REST Framework)

### ✔ Authentication & Authorization
- JWT login & token refresh  
- Secure user registration  
- Role-based access (admin, student, etc.)  
- Protected routes for authenticated users  

### ✔ User Account Management
- Update email  
- Change password  
- View authenticated user profile  
- Admin CRUD operations on users  

### ✔ Resource Management
- List learning resources  
- Add/edit/delete resources (admin only)  
- Serializer-driven validation  
- Clean API response structure  

### ✔ API Documentation
- Auto-generated OpenAPI schema  
- Swagger UI & Redoc via **drf-spectacular**  
- Example requests for every endpoint  

### ✔ Deployment Ready
- `runtime.txt`  
- `build.sh`  
- `.env` support  
- Production settings separation  

---

# 🎨 Frontend Features (React)

### ✔ Authentication UI
- Login form  
- Token storage (localStorage)  
- Auto-refresh token logic  
- Protected routes  

### ✔ User Interface
- Dashboard layout  
- Navbar with logout  
- Conditional rendering for authenticated users  
- Clean component structure  

### ✔ Resource Display
- Fetch books/resources from backend  
- Display in responsive UI  
- Future: search, filter, categories  

### ✔ API Integration
- Centralized `apiFetch` wrapper  
- Automatic token refresh  
- Error handling & fallback UI  

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the repository
```bash
git clone https://github.com/Patrick-startech/learning-wellbeing-hub.git
cd learning-wellbeing-hub

## 👤 Author

**Patrick Asamoah Adjei**  
ALX Africa – Back-End Development Program  
Focused on building secure, scalable, and production‑ready backend and frontend systems.


---
