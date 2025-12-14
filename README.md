# Learning and Wellbeing Hub

## 📌 Project Overview
The **Learning and Wellbeing Hub** is a full‑stack application designed to provide resources, tools, and support for learners. It combines a Django backend with a React frontend, secured by JWT authentication, and aims to deliver a seamless user experience for managing educational and wellbeing resources.

---

## ✅ Progress So Far

### Backend (Django)
- Initialized project repository and configured backend environment.
- Designed Django models with audit fields and relationships.
- Applied migrations successfully and ensured smooth database integration.
- Built core API endpoints for:
  - User authentication (login, refresh, logout).
  - Resource management (books/resources listing).
- Implemented JWT authentication with access and refresh tokens.

### Frontend (React)
- Set up React environment and project structure.
- Built core components:
  - **Login** – handles authentication and token storage.
  - **Navbar** – provides logout functionality and navigation.
  - **BookList** – displays resources fetched from backend.
- Integrated frontend with backend services using a centralized API layer.
- Implemented conditional rendering for authenticated vs. unauthenticated states.
- Debugged blank page and JSX errors by cleaning up `App.js` and wrapping in `BrowserRouter`.

### API Layer (`services/api.js`)
- Created a **global fetch wrapper (`apiFetch`)** that:
  - Automatically attaches JWT tokens from `localStorage`.
  - Refreshes expired tokens using the refresh token.
  - Retries failed requests after refresh.
- Centralized API calls (`getBooks`, `addBook`, `login`, `logout`) for cleaner code.

---

## ⚡ Challenges and Solutions
- **Migration Errors:** Fixed by reviewing models, correcting field types, and re‑running migrations.
- **Token Handling:** Standardized token storage (`access_token`, `refresh_token`) and centralized logic in `apiFetch`.
- **Frontend Rendering Errors:** Resolved blank page issues by cleaning JSX, updating `App.js`, and adding error boundaries.
- **API Consistency:** Reduced duplication by implementing a global fetch wrapper.

---

## 🚀 Next Steps (Week 5 – Final Week)
- Complete remaining API endpoints for full functionality of the Learning and Wellbeing Hub.
- Expand frontend features:
  - Resource creation, editing, and management.
- Implement **Private Routes** in React Router for authenticated access.
- Add error boundaries and user‑friendly messages.
- Write unit tests for backend models and API endpoints.
- Polish UI/UX for professional presentation.
- Prepare final documentation and README updates.

---

## 🛠️ Tech Stack
- **Backend:** Django, Django REST Framework
- **Frontend:** React, JSX
- **Authentication:** JWT (Access + Refresh tokens)
- **Database:** SQLite/PostgreSQL (depending on deployment)
- **Tools:** ESLint, Prettier, Git/GitHub

---

## 👤 Author
**Patrick Asamoah Adjei**  
ALX Africa – Back-End Development Program  
Montreal, Canada (Remote)

---
