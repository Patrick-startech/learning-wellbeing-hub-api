# 🌱 Learning and Wellbeing Hub API

The **Learning and Wellbeing Hub** is a backend API built with **Django** and **Django REST Framework**.  
It integrates **academic learning tools** (resources, quizzes, mentorship) with **wellbeing features** (mood tracking, journaling, peer support) to provide a holistic platform for students, mentors, and administrators.

---

## 🚀 Features

### 📚 Learning
- **Resources Management (CRUD)**: Upload, update, and browse learning materials.
- **Quizzes & Assessments**: Create quizzes, submit answers, and view results.
- **Mentorship**: Students can request mentorship; mentors/admins can manage requests.

### 🌟 Wellbeing
- **Mood Tracking**: Log daily moods and view history.
- **Journaling**: Write and retrieve personal journal entries.
- **Growth Dashboard**: Combined analytics of academic progress and wellbeing.
- **Peer Support Forum**: Create and join discussions with peers.

### 🔑 Authentication & Roles
- **JWT Authentication** for secure login.
- **Role-Based Access**:
  - **Admin** → full control over users, resources, and forum moderation.
  - **Mentor** → can manage resources, quizzes, and mentorship requests.
  - **Student** → can access resources, take quizzes, log wellbeing activities, and borrow support.

---

## 🛠 Tech Stack
- **Backend**: Django, Django REST Framework
- **Auth**: djangorestframework-simplejwt (JWT)
- **Database**: PostgreSQL
- **Environment Management**: python-dotenv
- **Deployment**: Heroku / PythonAnywhere

---

## 📂 Project Structure
